"""
Automatic Calculation of Valuation Assumptions
Calculates WACC, Tax Rate, Terminal Growth automatically from company data
"""

import requests
from typing import Dict, Tuple
import statistics


class AssumptionCalculator:
    """Automatically calculate valuation assumptions"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.financialdatasets.ai"
        self.headers = {"X-API-KEY": api_key}

    def calculate_all_assumptions(self, ticker: str) -> Dict:
        """
        Calculate all valuation assumptions automatically

        Returns:
            {
                'wacc': float,
                'tax_rate': float,
                'terminal_growth': float,
                'details': {...}  # Calculation details
            }
        """
        print(f"📊 Calculating assumptions for {ticker}...")

        # Get all required data
        income_stmt = self._get_income_statement(ticker, limit=5)
        balance_sheet = self._get_balance_sheet(ticker, limit=2)
        cash_flow = self._get_cash_flow(ticker, limit=5)
        price_data = self._get_price_snapshot(ticker)

        # Calculate each assumption
        tax_rate = self._calculate_effective_tax_rate(income_stmt)
        wacc = self._calculate_wacc(ticker, income_stmt, balance_sheet, price_data, tax_rate)
        terminal_growth = self._calculate_terminal_growth(income_stmt, ticker)

        return {
            'wacc': wacc['wacc'],
            'tax_rate': tax_rate['effective_tax_rate'],
            'terminal_growth': terminal_growth['terminal_growth'],
            'details': {
                'wacc_details': wacc,
                'tax_details': tax_rate,
                'growth_details': terminal_growth
            }
        }

    def _get_income_statement(self, ticker: str, limit: int = 5) -> Dict:
        """Fetch income statement data"""
        url = f"{self.base_url}/financials/income-statements/"
        params = {"ticker": ticker, "period": "annual", "limit": limit}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def _get_balance_sheet(self, ticker: str, limit: int = 2) -> Dict:
        """Fetch balance sheet data"""
        url = f"{self.base_url}/financials/balance-sheets/"
        params = {"ticker": ticker, "period": "annual", "limit": limit}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def _get_cash_flow(self, ticker: str, limit: int = 5) -> Dict:
        """Fetch cash flow statement data"""
        url = f"{self.base_url}/financials/cash-flow-statements/"
        params = {"ticker": ticker, "period": "annual", "limit": limit}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def _get_price_snapshot(self, ticker: str) -> Dict:
        """Fetch current price and market data"""
        url = f"{self.base_url}/prices/snapshot/"
        params = {"ticker": ticker}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def _calculate_effective_tax_rate(self, income_stmt: Dict) -> Dict:
        """
        Calculate effective tax rate from income statement

        Formula: Tax Expense / Pre-tax Income
        """
        statements = income_stmt.get('income_statements', [])

        if not statements:
            return {
                'effective_tax_rate': 0.21,  # Default US corporate rate
                'method': 'default',
                'note': 'Using default US corporate tax rate (21%)'
            }

        tax_rates = []
        for stmt in statements[:3]:  # Use last 3 years
            tax_expense = stmt.get('income_tax_expense', 0)
            net_income = stmt.get('net_income', 0)
            pretax_income = net_income + tax_expense

            if pretax_income > 0 and tax_expense >= 0:
                tax_rate = tax_expense / pretax_income
                if 0 <= tax_rate <= 0.50:  # Sanity check
                    tax_rates.append(tax_rate)

        if tax_rates:
            avg_tax_rate = statistics.mean(tax_rates)
            return {
                'effective_tax_rate': round(avg_tax_rate, 4),
                'method': 'calculated',
                'note': f'Average effective tax rate from last {len(tax_rates)} years',
                'yearly_rates': tax_rates
            }
        else:
            return {
                'effective_tax_rate': 0.21,
                'method': 'default',
                'note': 'Insufficient data, using default US corporate tax rate (21%)'
            }

    def _calculate_wacc(self, ticker: str, income_stmt: Dict, balance_sheet: Dict,
                        price_data: Dict, tax_rate_info: Dict) -> Dict:
        """
        Calculate Weighted Average Cost of Capital (WACC)

        WACC = (E/V × Re) + (D/V × Rd × (1-T))

        Where:
        E = Market value of equity
        D = Market value of debt
        V = E + D
        Re = Cost of equity (using CAPM)
        Rd = Cost of debt
        T = Tax rate
        """
        # Get latest balance sheet
        balance_sheets = balance_sheet.get('balance_sheets', [])
        if not balance_sheets:
            return self._default_wacc(ticker)

        latest_bs = balance_sheets[0]

        # Get debt and equity values
        total_debt = latest_bs.get('total_debt', 0)
        shareholders_equity = latest_bs.get('shareholders_equity', 0)

        # Market value of equity (shares outstanding × price)
        shares_outstanding = latest_bs.get('outstanding_shares', 0)
        snapshot = price_data.get('snapshot', {})
        current_price = snapshot.get('price', 0)

        if shares_outstanding > 0 and current_price > 0:
            market_cap = shares_outstanding * current_price
        else:
            market_cap = shareholders_equity  # Use book value as fallback

        # Calculate cost of debt
        cost_of_debt = self._calculate_cost_of_debt(income_stmt, total_debt)

        # Calculate cost of equity (simplified CAPM)
        cost_of_equity = self._calculate_cost_of_equity(ticker, market_cap)

        # Calculate WACC
        total_value = market_cap + total_debt

        if total_value > 0:
            equity_weight = market_cap / total_value
            debt_weight = total_debt / total_value

            tax_rate = tax_rate_info.get('effective_tax_rate', 0.21)

            wacc = (equity_weight * cost_of_equity) + \
                   (debt_weight * cost_of_debt * (1 - tax_rate))

            return {
                'wacc': round(wacc, 4),
                'method': 'calculated',
                'components': {
                    'cost_of_equity': round(cost_of_equity, 4),
                    'cost_of_debt': round(cost_of_debt, 4),
                    'equity_weight': round(equity_weight, 4),
                    'debt_weight': round(debt_weight, 4),
                    'market_cap': market_cap,
                    'total_debt': total_debt
                },
                'note': 'Calculated using CAPM and market data'
            }
        else:
            return self._default_wacc(ticker)

    def _calculate_cost_of_debt(self, income_stmt: Dict, total_debt: float) -> float:
        """
        Calculate cost of debt

        Formula: Interest Expense / Total Debt
        """
        statements = income_stmt.get('income_statements', [])
        if not statements or total_debt <= 0:
            return 0.04  # Default 4%

        latest = statements[0]
        interest_expense = latest.get('interest_expense', 0)

        if interest_expense > 0 and total_debt > 0:
            cost_of_debt = interest_expense / total_debt
            return min(cost_of_debt, 0.15)  # Cap at 15%
        else:
            return 0.04  # Default 4%

    def _calculate_cost_of_equity(self, ticker: str, market_cap: float) -> float:
        """
        Calculate cost of equity using simplified CAPM

        Re = Rf + β(Rm - Rf)

        Where:
        Rf = Risk-free rate (10-year Treasury: ~4.5%)
        β = Beta (estimated based on company size/industry)
        Rm - Rf = Market risk premium (~6%)
        """
        # Risk-free rate (current 10-year Treasury approximation)
        risk_free_rate = 0.045

        # Market risk premium
        market_risk_premium = 0.06

        # Estimate beta based on market cap (simplified)
        if market_cap > 500e9:  # Mega cap
            beta = 1.0
        elif market_cap > 100e9:  # Large cap
            beta = 1.1
        elif market_cap > 10e9:  # Mid cap
            beta = 1.2
        else:  # Small cap
            beta = 1.3

        cost_of_equity = risk_free_rate + (beta * market_risk_premium)

        return cost_of_equity

    def _default_wacc(self, ticker: str) -> Dict:
        """Return default WACC when calculation not possible"""
        return {
            'wacc': 0.10,
            'method': 'default',
            'note': 'Using default WACC (10%) - insufficient data for calculation'
        }

    def _calculate_terminal_growth(self, income_stmt: Dict, ticker: str) -> Dict:
        """
        Calculate terminal growth rate

        Methods:
        1. Historical revenue growth (capped)
        2. GDP growth + inflation (~2.5%)
        3. Industry-specific adjustments
        """
        statements = income_stmt.get('income_statements', [])

        if len(statements) < 3:
            return {
                'terminal_growth': 0.025,
                'method': 'default',
                'note': 'Using default GDP growth rate (2.5%)'
            }

        # Calculate historical revenue growth
        growth_rates = []
        for i in range(len(statements) - 1):
            current_rev = statements[i].get('revenue', 0)
            prior_rev = statements[i + 1].get('revenue', 0)

            if prior_rev > 0:
                growth = (current_rev - prior_rev) / prior_rev
                if -0.5 < growth < 0.5:  # Sanity check
                    growth_rates.append(growth)

        if growth_rates:
            avg_growth = statistics.mean(growth_rates)

            # Cap terminal growth at GDP + inflation
            # High-growth companies can't grow faster than economy forever
            capped_growth = min(avg_growth, 0.04)

            # Floor at 1% (assume some growth)
            terminal_growth = max(capped_growth, 0.01)

            return {
                'terminal_growth': round(terminal_growth, 4),
                'method': 'calculated',
                'note': f'Based on {len(growth_rates)}-year avg growth, capped at GDP+inflation',
                'historical_avg_growth': round(avg_growth, 4),
                'yearly_growth_rates': [round(g, 4) for g in growth_rates]
            }
        else:
            return {
                'terminal_growth': 0.025,
                'method': 'default',
                'note': 'Using default GDP growth rate (2.5%)'
            }


def format_assumption_summary(assumptions: Dict) -> str:
    """Format assumptions for display"""
    details = assumptions.get('details', {})

    summary = f"""
## 🎯 Automatically Calculated Assumptions

### WACC (Discount Rate): {assumptions['wacc']:.1%}
{details.get('wacc_details', {}).get('note', '')}

**Components:**
- Cost of Equity: {details.get('wacc_details', {}).get('components', {}).get('cost_of_equity', 0):.1%}
- Cost of Debt: {details.get('wacc_details', {}).get('components', {}).get('cost_of_debt', 0):.1%}
- Equity Weight: {details.get('wacc_details', {}).get('components', {}).get('equity_weight', 0):.1%}
- Debt Weight: {details.get('wacc_details', {}).get('components', {}).get('debt_weight', 0):.1%}

### Tax Rate: {assumptions['tax_rate']:.1%}
{details.get('tax_details', {}).get('note', '')}

### Terminal Growth: {assumptions['terminal_growth']:.1%}
{details.get('growth_details', {}).get('note', '')}
"""

    return summary
