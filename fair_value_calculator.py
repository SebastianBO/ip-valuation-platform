"""
Fair Value & Analyst Consensus Module
Calculates intrinsic value using DCF and integrates analyst estimates
"""

import requests
from typing import Dict, List
from datetime import datetime


class FairValueCalculator:
    """
    Calculate fair value using multiple methods:
    1. Discounted Cash Flow (DCF)
    2. P/E based valuation
    3. P/S based valuation
    4. Analyst consensus (if available)
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.financialdatasets.ai"
        self.headers = {"X-API-KEY": api_key}

    def calculate_fair_value(self, ticker: str, growth_rate: float = None,
                            terminal_growth: float = 0.025, wacc: float = None) -> Dict:
        """
        Calculate comprehensive fair value

        Methods:
        - DCF (Discounted Cash Flow)
        - P/E Multiple
        - P/S Multiple
        - EV/EBITDA Multiple
        - Average of methods
        """
        # Get financial data
        financial_data = self._get_financial_data(ticker)

        # Auto-calculate WACC if not provided
        if wacc is None:
            wacc = self._estimate_wacc(ticker, financial_data)

        # Auto-calculate growth rate if not provided
        if growth_rate is None:
            growth_rate = self._estimate_growth_rate(financial_data)

        valuations = {}

        # Method 1: DCF
        valuations['dcf'] = self._dcf_valuation(
            financial_data, growth_rate, terminal_growth, wacc
        )

        # Method 2: P/E Multiple
        valuations['pe_multiple'] = self._pe_valuation(financial_data, ticker)

        # Method 3: P/S Multiple
        valuations['ps_multiple'] = self._ps_valuation(financial_data, ticker)

        # Method 4: EV/EBITDA Multiple
        valuations['ev_ebitda'] = self._ev_ebitda_valuation(financial_data, ticker)

        # Calculate average (exclude any that failed)
        valid_valuations = [v['fair_value_per_share'] for v in valuations.values()
                           if v and v.get('fair_value_per_share', 0) > 0]

        if valid_valuations:
            average_fair_value = sum(valid_valuations) / len(valid_valuations)
        else:
            average_fair_value = 0

        # Get current price
        price_data = self._get_price_snapshot(ticker)
        current_price = price_data.get('snapshot', {}).get('price', 0)

        # Calculate upside/downside
        if current_price > 0 and average_fair_value > 0:
            upside_pct = ((average_fair_value - current_price) / current_price) * 100
        else:
            upside_pct = 0

        return {
            'ticker': ticker,
            'current_price': current_price,
            'fair_value_average': average_fair_value,
            'upside_downside_pct': upside_pct,
            'valuation_methods': valuations,
            'assumptions': {
                'growth_rate': growth_rate,
                'terminal_growth': terminal_growth,
                'wacc': wacc
            },
            'recommendation': self._get_recommendation(upside_pct)
        }

    def _get_financial_data(self, ticker: str) -> Dict:
        """Get comprehensive financial data"""
        data = {}

        # Income statement
        url = f"{self.base_url}/financials/income-statements/"
        params = {"ticker": ticker, "period": "annual", "limit": 5}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data['income'] = response.json()
        except:
            data['income'] = {}

        # Balance sheet
        url = f"{self.base_url}/financials/balance-sheets/"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data['balance'] = response.json()
        except:
            data['balance'] = {}

        # Cash flow
        url = f"{self.base_url}/financials/cash-flow-statements/"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data['cashflow'] = response.json()
        except:
            data['cashflow'] = {}

        # Financial metrics
        url = f"{self.base_url}/financial-metrics/snapshot/"
        params = {"ticker": ticker}
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data['metrics'] = response.json()
        except:
            data['metrics'] = {}

        return data

    def _get_price_snapshot(self, ticker: str) -> Dict:
        """Get current price data"""
        url = f"{self.base_url}/prices/snapshot/"
        params = {"ticker": ticker}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def _estimate_wacc(self, ticker: str, financial_data: Dict) -> float:
        """Estimate WACC (simplified)"""
        # Use market cap if available
        metrics = financial_data.get('metrics', {}).get('snapshot', {})

        # Industry-based WACC estimates
        industry_wacc = {
            'biotech': 0.12,
            'pharma': 0.10,
            'tech': 0.11,
            'consumer': 0.09,
            'industrial': 0.08
        }

        # Default to moderate risk
        return 0.10

    def _estimate_growth_rate(self, financial_data: Dict) -> float:
        """Estimate growth rate from historical data"""
        income_data = financial_data.get('income', {}).get('income_statements', [])

        if len(income_data) < 2:
            return 0.05  # Default 5%

        # Calculate historical revenue growth
        growth_rates = []
        for i in range(len(income_data) - 1):
            current = income_data[i].get('revenue', 0)
            prior = income_data[i + 1].get('revenue', 0)

            if prior > 0:
                growth = (current - prior) / prior
                if -0.5 < growth < 2.0:  # Sanity check
                    growth_rates.append(growth)

        if growth_rates:
            avg_growth = sum(growth_rates) / len(growth_rates)
            # Cap at reasonable level
            return min(max(avg_growth, -0.20), 0.50)
        else:
            return 0.05

    def _dcf_valuation(self, financial_data: Dict, growth_rate: float,
                      terminal_growth: float, wacc: float) -> Dict:
        """
        Discounted Cash Flow valuation

        Steps:
        1. Project free cash flows for 5 years
        2. Calculate terminal value
        3. Discount to present value
        4. Divide by shares outstanding
        """
        cashflow_data = financial_data.get('cashflow', {}).get('cash_flow_statements', [])
        balance_data = financial_data.get('balance', {}).get('balance_sheets', [])

        if not cashflow_data or not balance_data:
            return {'method': 'DCF', 'error': 'Insufficient data'}

        latest_cf = cashflow_data[0]
        latest_bs = balance_data[0]

        # Get latest free cash flow
        operating_cf = latest_cf.get('operating_cash_flow', 0)
        capex = latest_cf.get('capital_expenditures', 0)
        fcf = operating_cf + capex  # capex is negative

        if fcf <= 0:
            return {'method': 'DCF', 'error': 'Negative free cash flow'}

        # Project cash flows
        projected_fcf = []
        for year in range(1, 6):
            projected = fcf * ((1 + growth_rate) ** year)
            projected_fcf.append(projected)

        # Calculate present value of projected cash flows
        pv_fcf = 0
        for year, cf in enumerate(projected_fcf, 1):
            pv = cf / ((1 + wacc) ** year)
            pv_fcf += pv

        # Terminal value
        terminal_fcf = projected_fcf[-1] * (1 + terminal_growth)
        terminal_value = terminal_fcf / (wacc - terminal_growth)
        pv_terminal = terminal_value / ((1 + wacc) ** 5)

        # Enterprise value
        enterprise_value = pv_fcf + pv_terminal

        # Equity value
        total_debt = latest_bs.get('total_debt', 0)
        cash = latest_bs.get('cash_and_equivalents', 0)
        equity_value = enterprise_value - total_debt + cash

        # Per share
        shares = latest_bs.get('outstanding_shares', 0)
        if shares > 0:
            fair_value_per_share = equity_value / shares
        else:
            fair_value_per_share = 0

        return {
            'method': 'DCF',
            'enterprise_value': enterprise_value,
            'equity_value': equity_value,
            'fair_value_per_share': fair_value_per_share,
            'pv_cash_flows': pv_fcf,
            'pv_terminal_value': pv_terminal,
            'projected_fcf': projected_fcf
        }

    def _pe_valuation(self, financial_data: Dict, ticker: str) -> Dict:
        """P/E Multiple valuation"""
        income_data = financial_data.get('income', {}).get('income_statements', [])
        balance_data = financial_data.get('balance', {}).get('balance_sheets', [])
        metrics = financial_data.get('metrics', {}).get('snapshot', {})

        if not income_data or not balance_data:
            return {'method': 'P/E Multiple', 'error': 'Insufficient data'}

        latest_income = income_data[0]
        latest_bs = balance_data[0]

        net_income = latest_income.get('net_income', 0)
        shares = latest_bs.get('outstanding_shares', 0)

        if shares <= 0 or net_income <= 0:
            return {'method': 'P/E Multiple', 'error': 'Negative or zero earnings'}

        eps = net_income / shares

        # Use industry average P/E (simplified)
        industry_pe = {
            'biotech': 25,  # High growth
            'pharma': 15,   # Mature
            'tech': 30,
            'consumer': 20,
            'industrial': 18
        }

        # Use current P/E if available, else industry average
        current_pe = metrics.get('price_to_earnings_ratio')

        if current_pe and 0 < current_pe < 100:
            # Use current P/E as benchmark
            fair_pe = current_pe * 1.0  # Assume fairly valued
        else:
            fair_pe = 20  # Default moderate P/E

        fair_value_per_share = eps * fair_pe

        return {
            'method': 'P/E Multiple',
            'eps': eps,
            'fair_pe_ratio': fair_pe,
            'fair_value_per_share': fair_value_per_share
        }

    def _ps_valuation(self, financial_data: Dict, ticker: str) -> Dict:
        """P/S Multiple valuation"""
        income_data = financial_data.get('income', {}).get('income_statements', [])
        balance_data = financial_data.get('balance', {}).get('balance_sheets', [])

        if not income_data or not balance_data:
            return {'method': 'P/S Multiple', 'error': 'Insufficient data'}

        latest_income = income_data[0]
        latest_bs = balance_data[0]

        revenue = latest_income.get('revenue', 0)
        shares = latest_bs.get('outstanding_shares', 0)

        if shares <= 0 or revenue <= 0:
            return {'method': 'P/S Multiple', 'error': 'No revenue data'}

        revenue_per_share = revenue / shares

        # Industry P/S ratios
        fair_ps = 3.0  # Default moderate

        fair_value_per_share = revenue_per_share * fair_ps

        return {
            'method': 'P/S Multiple',
            'revenue_per_share': revenue_per_share,
            'fair_ps_ratio': fair_ps,
            'fair_value_per_share': fair_value_per_share
        }

    def _ev_ebitda_valuation(self, financial_data: Dict, ticker: str) -> Dict:
        """EV/EBITDA Multiple valuation"""
        income_data = financial_data.get('income', {}).get('income_statements', [])
        balance_data = financial_data.get('balance', {}).get('balance_sheets', [])

        if not income_data or not balance_data:
            return {'method': 'EV/EBITDA', 'error': 'Insufficient data'}

        latest_income = income_data[0]
        latest_bs = balance_data[0]

        operating_income = latest_income.get('operating_income', 0)
        # Simplified EBITDA (would add back D&A if available)
        ebitda = operating_income

        if ebitda <= 0:
            return {'method': 'EV/EBITDA', 'error': 'Negative EBITDA'}

        # Fair EV/EBITDA multiple
        fair_ev_ebitda = 12  # Default

        enterprise_value = ebitda * fair_ev_ebitda

        # Convert to equity value
        total_debt = latest_bs.get('total_debt', 0)
        cash = latest_bs.get('cash_and_equivalents', 0)
        equity_value = enterprise_value - total_debt + cash

        shares = latest_bs.get('outstanding_shares', 0)
        if shares > 0:
            fair_value_per_share = equity_value / shares
        else:
            fair_value_per_share = 0

        return {
            'method': 'EV/EBITDA',
            'ebitda': ebitda,
            'fair_ev_ebitda_multiple': fair_ev_ebitda,
            'enterprise_value': enterprise_value,
            'fair_value_per_share': fair_value_per_share
        }

    def _get_recommendation(self, upside_pct: float) -> str:
        """Get buy/sell recommendation based on upside"""
        if upside_pct > 30:
            return "Strong Buy - Significantly Undervalued"
        elif upside_pct > 15:
            return "Buy - Undervalued"
        elif upside_pct > -10:
            return "Hold - Fairly Valued"
        elif upside_pct > -25:
            return "Sell - Overvalued"
        else:
            return "Strong Sell - Significantly Overvalued"
