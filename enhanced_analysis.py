"""
Enhanced EMBA-Level Financial Analysis
Integrates multiple data sources for comprehensive IP valuation context
"""

import requests
from typing import Dict, List
from datetime import datetime


class EnhancedFinancialAnalysis:
    """Advanced financial analysis for IP valuation context"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.financialdatasets.ai"
        self.headers = {"X-API-KEY": api_key}

    def get_comprehensive_analysis(self, ticker: str) -> Dict:
        """
        Get comprehensive financial analysis for EMBA-level IP valuation

        Returns all relevant metrics for understanding IP value context
        """
        analysis = {
            'ticker': ticker,
            'timestamp': datetime.now().isoformat(),
            'financial_health': {},
            'profitability_metrics': {},
            'rd_analysis': {},
            'capital_structure': {},
            'market_position': {},
            'risk_indicators': {}
        }

        # Get all required data
        financial_metrics = self._get_financial_metrics(ticker)
        balance_sheet = self._get_balance_sheet(ticker)
        income_stmt = self._get_income_statement(ticker)
        cash_flow = self._get_cash_flow(ticker)
        price_snapshot = self._get_price_snapshot(ticker)

        # Analyze financial health
        analysis['financial_health'] = self._analyze_financial_health(
            balance_sheet, income_stmt, cash_flow
        )

        # Analyze profitability (important for IP value)
        analysis['profitability_metrics'] = self._analyze_profitability(
            income_stmt, balance_sheet
        )

        # R&D analysis (critical for IP generation)
        analysis['rd_analysis'] = self._analyze_rd_investment(
            income_stmt, balance_sheet
        )

        # Capital structure (affects WACC)
        analysis['capital_structure'] = self._analyze_capital_structure(
            balance_sheet, price_snapshot
        )

        # Market position
        analysis['market_position'] = self._analyze_market_position(
            price_snapshot, income_stmt, balance_sheet
        )

        # Risk indicators
        analysis['risk_indicators'] = self._analyze_risk_factors(
            balance_sheet, income_stmt, cash_flow
        )

        return analysis

    def _get_financial_metrics(self, ticker: str) -> Dict:
        """Get financial metrics snapshot"""
        url = f"{self.base_url}/financial-metrics/snapshot/"
        params = {"ticker": ticker}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def _get_balance_sheet(self, ticker: str) -> Dict:
        """Get balance sheet"""
        url = f"{self.base_url}/financials/balance-sheets/"
        params = {"ticker": ticker, "period": "annual", "limit": 3}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def _get_income_statement(self, ticker: str) -> Dict:
        """Get income statement"""
        url = f"{self.base_url}/financials/income-statements/"
        params = {"ticker": ticker, "period": "annual", "limit": 5}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def _get_cash_flow(self, ticker: str) -> Dict:
        """Get cash flow statement"""
        url = f"{self.base_url}/financials/cash-flow-statements/"
        params = {"ticker": ticker, "period": "annual", "limit": 3}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def _get_price_snapshot(self, ticker: str) -> Dict:
        """Get current price snapshot"""
        url = f"{self.base_url}/prices/snapshot/"
        params = {"ticker": ticker}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except:
            return {}

    def _analyze_financial_health(self, balance_sheet: Dict, income_stmt: Dict,
                                  cash_flow: Dict) -> Dict:
        """
        Analyze financial health metrics

        Key indicators:
        - Current ratio
        - Quick ratio
        - Debt-to-equity
        - Interest coverage
        - Free cash flow
        """
        bs_data = balance_sheet.get('balance_sheets', [])
        income_data = income_stmt.get('income_statements', [])
        cf_data = cash_flow.get('cash_flow_statements', [])

        if not bs_data or not income_data:
            return {}

        latest_bs = bs_data[0]
        latest_income = income_data[0]

        # Current ratio
        current_assets = latest_bs.get('current_assets', 0)
        current_liabilities = latest_bs.get('current_liabilities', 0)
        current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0

        # Quick ratio (more conservative)
        cash = latest_bs.get('cash_and_equivalents', 0)
        receivables = latest_bs.get('trade_and_non_trade_receivables', 0)
        quick_ratio = (cash + receivables) / current_liabilities if current_liabilities > 0 else 0

        # Debt-to-equity
        total_debt = latest_bs.get('total_debt', 0)
        shareholders_equity = latest_bs.get('shareholders_equity', 0)
        debt_to_equity = total_debt / shareholders_equity if shareholders_equity > 0 else 0

        # Interest coverage
        operating_income = latest_income.get('operating_income', 0)
        interest_expense = latest_income.get('interest_expense', 0)
        interest_coverage = operating_income / interest_expense if interest_expense > 0 else 999

        # Free cash flow
        if cf_data:
            latest_cf = cf_data[0]
            operating_cf = latest_cf.get('operating_cash_flow', 0)
            capex = latest_cf.get('capital_expenditures', 0)
            free_cash_flow = operating_cf + capex  # capex is negative

            fcf_margin = free_cash_flow / latest_income.get('revenue', 1)
        else:
            free_cash_flow = 0
            fcf_margin = 0

        return {
            'current_ratio': round(current_ratio, 2),
            'quick_ratio': round(quick_ratio, 2),
            'debt_to_equity': round(debt_to_equity, 2),
            'interest_coverage': round(min(interest_coverage, 999), 2),
            'free_cash_flow': free_cash_flow,
            'fcf_margin': round(fcf_margin, 4),
            'assessment': self._assess_financial_health(current_ratio, debt_to_equity, interest_coverage)
        }

    def _assess_financial_health(self, current_ratio: float, debt_to_equity: float,
                                 interest_coverage: float) -> str:
        """Assess overall financial health"""
        score = 0

        if current_ratio > 1.5:
            score += 3
        elif current_ratio > 1.0:
            score += 2
        else:
            score += 1

        if debt_to_equity < 0.5:
            score += 3
        elif debt_to_equity < 1.0:
            score += 2
        else:
            score += 1

        if interest_coverage > 10:
            score += 3
        elif interest_coverage > 5:
            score += 2
        else:
            score += 1

        if score >= 8:
            return "Excellent - Strong financial position supports IP development"
        elif score >= 6:
            return "Good - Healthy balance sheet for IP investment"
        elif score >= 4:
            return "Moderate - Some financial constraints on IP spending"
        else:
            return "Weak - Financial stress may limit IP development"

    def _analyze_profitability(self, income_stmt: Dict, balance_sheet: Dict) -> Dict:
        """
        Analyze profitability metrics

        Important for IP valuation:
        - Gross margin (product economics)
        - Operating margin (operational efficiency)
        - Net margin (overall profitability)
        - ROE (return on equity)
        - ROA (return on assets)
        """
        income_data = income_stmt.get('income_statements', [])
        bs_data = balance_sheet.get('balance_sheets', [])

        if not income_data or not bs_data:
            return {}

        latest_income = income_data[0]
        latest_bs = bs_data[0]

        revenue = latest_income.get('revenue', 0)
        gross_profit = latest_income.get('gross_profit', 0)
        operating_income = latest_income.get('operating_income', 0)
        net_income = latest_income.get('net_income', 0)

        total_assets = latest_bs.get('total_assets', 0)
        shareholders_equity = latest_bs.get('shareholders_equity', 0)

        # Margin analysis
        gross_margin = gross_profit / revenue if revenue > 0 else 0
        operating_margin = operating_income / revenue if revenue > 0 else 0
        net_margin = net_income / revenue if revenue > 0 else 0

        # Returns
        roe = net_income / shareholders_equity if shareholders_equity > 0 else 0
        roa = net_income / total_assets if total_assets > 0 else 0

        # Calculate trend (if multiple years available)
        if len(income_data) >= 3:
            trends = self._calculate_profitability_trends(income_data)
        else:
            trends = {}

        return {
            'gross_margin': round(gross_margin, 4),
            'operating_margin': round(operating_margin, 4),
            'net_margin': round(net_margin, 4),
            'roe': round(roe, 4),
            'roa': round(roa, 4),
            'trends': trends,
            'ip_insight': self._profitability_ip_insight(gross_margin, operating_margin)
        }

    def _calculate_profitability_trends(self, income_data: List[Dict]) -> Dict:
        """Calculate profitability trends over time"""
        gross_margins = []
        operating_margins = []

        for stmt in income_data[:3]:
            revenue = stmt.get('revenue', 0)
            if revenue > 0:
                gm = stmt.get('gross_profit', 0) / revenue
                om = stmt.get('operating_income', 0) / revenue
                gross_margins.append(gm)
                operating_margins.append(om)

        return {
            'gross_margin_trend': 'improving' if len(gross_margins) >= 2 and gross_margins[0] > gross_margins[1] else 'declining',
            'operating_margin_trend': 'improving' if len(operating_margins) >= 2 and operating_margins[0] > operating_margins[1] else 'declining'
        }

    def _profitability_ip_insight(self, gross_margin: float, operating_margin: float) -> str:
        """Provide insight on what profitability means for IP value"""
        if gross_margin > 0.6:
            return "High gross margins suggest strong IP/brand pricing power"
        elif gross_margin > 0.4:
            return "Healthy margins indicate IP contributing to competitive advantage"
        else:
            return "Lower margins may indicate IP is less differentiated"

    def _analyze_rd_investment(self, income_stmt: Dict, balance_sheet: Dict) -> Dict:
        """
        Analyze R&D investment patterns

        Critical for IP generation:
        - R&D as % of revenue
        - R&D trend
        - R&D per employee (if available)
        - R&D efficiency
        """
        income_data = income_stmt.get('income_statements', [])

        if not income_data:
            return {}

        rd_intensity = []
        rd_amounts = []

        for stmt in income_data:
            revenue = stmt.get('revenue', 0)
            rd = stmt.get('research_and_development', 0)

            rd_amounts.append(rd)

            if revenue > 0 and rd > 0:
                intensity = rd / revenue
                rd_intensity.append(intensity)

        avg_intensity = sum(rd_intensity) / len(rd_intensity) if rd_intensity else 0
        latest_rd = rd_amounts[0] if rd_amounts else 0

        # Calculate R&D growth
        if len(rd_amounts) >= 2:
            rd_growth = (rd_amounts[0] - rd_amounts[1]) / rd_amounts[1] if rd_amounts[1] > 0 else 0
        else:
            rd_growth = 0

        return {
            'rd_intensity': round(avg_intensity, 4),
            'latest_rd_spend': latest_rd,
            'rd_growth_rate': round(rd_growth, 4),
            'rd_amounts_history': rd_amounts[:5],
            'ip_generation_potential': self._assess_ip_potential(avg_intensity, rd_growth)
        }

    def _assess_ip_potential(self, rd_intensity: float, rd_growth: float) -> str:
        """Assess IP generation potential based on R&D"""
        if rd_intensity > 0.15:
            if rd_growth > 0.10:
                return "Excellent - Heavy R&D investment with growth suggests strong IP pipeline"
            else:
                return "Good - Significant R&D spend indicates active IP development"
        elif rd_intensity > 0.08:
            return "Moderate - Average R&D investment for IP generation"
        else:
            return "Low - Limited R&D suggests less IP-intensive business model"

    def _analyze_capital_structure(self, balance_sheet: Dict, price_snapshot: Dict) -> Dict:
        """
        Analyze capital structure

        Relevant for WACC and IP financing:
        - Debt levels
        - Equity value
        - Leverage ratios
        """
        bs_data = balance_sheet.get('balance_sheets', [])
        snapshot = price_snapshot.get('snapshot', {})

        if not bs_data:
            return {}

        latest_bs = bs_data[0]

        total_debt = latest_bs.get('total_debt', 0)
        shareholders_equity = latest_bs.get('shareholders_equity', 0)
        total_assets = latest_bs.get('total_assets', 0)

        market_cap = snapshot.get('market_cap', 0)

        # Calculate ratios
        debt_to_assets = total_debt / total_assets if total_assets > 0 else 0
        debt_to_equity = total_debt / shareholders_equity if shareholders_equity > 0 else 0
        equity_to_assets = shareholders_equity / total_assets if total_assets > 0 else 0

        # Market-to-book
        market_to_book = market_cap / shareholders_equity if shareholders_equity > 0 else 0

        return {
            'total_debt': total_debt,
            'shareholders_equity': shareholders_equity,
            'market_cap': market_cap,
            'debt_to_assets': round(debt_to_assets, 4),
            'debt_to_equity': round(debt_to_equity, 4),
            'equity_to_assets': round(equity_to_assets, 4),
            'market_to_book': round(market_to_book, 2),
            'leverage_assessment': self._assess_leverage(debt_to_equity)
        }

    def _assess_leverage(self, debt_to_equity: float) -> str:
        """Assess leverage level"""
        if debt_to_equity < 0.3:
            return "Conservative - Low debt supports IP investment flexibility"
        elif debt_to_equity < 0.7:
            return "Moderate - Balanced capital structure"
        elif debt_to_equity < 1.5:
            return "Elevated - Higher debt may constrain IP spending"
        else:
            return "High - Significant leverage limits financial flexibility"

    def _analyze_market_position(self, price_snapshot: Dict, income_stmt: Dict,
                                 balance_sheet: Dict) -> Dict:
        """
        Analyze market position

        Relevant metrics:
        - Market cap
        - Enterprise value
        - P/E ratio
        - EV/Revenue
        - EV/EBITDA
        """
        snapshot = price_snapshot.get('snapshot', {})
        income_data = income_stmt.get('income_statements', [])
        bs_data = balance_sheet.get('balance_sheets', [])

        if not snapshot or not income_data or not bs_data:
            return {}

        market_cap = snapshot.get('market_cap', 0)
        price = snapshot.get('price', 0)

        latest_income = income_data[0]
        latest_bs = bs_data[0]

        net_income = latest_income.get('net_income', 0)
        revenue = latest_income.get('revenue', 0)
        ebitda = latest_income.get('operating_income', 0)  # Simplified

        total_debt = latest_bs.get('total_debt', 0)
        cash = latest_bs.get('cash_and_equivalents', 0)

        # Calculate enterprise value
        enterprise_value = market_cap + total_debt - cash

        # Valuation multiples
        shares = latest_bs.get('outstanding_shares', 0)
        eps = net_income / shares if shares > 0 else 0
        pe_ratio = price / eps if eps > 0 else 0

        ev_revenue = enterprise_value / revenue if revenue > 0 else 0
        ev_ebitda = enterprise_value / ebitda if ebitda > 0 else 0

        return {
            'market_cap': market_cap,
            'enterprise_value': enterprise_value,
            'price': price,
            'pe_ratio': round(pe_ratio, 2) if pe_ratio < 1000 else 999,
            'ev_revenue': round(ev_revenue, 2),
            'ev_ebitda': round(ev_ebitda, 2) if ev_ebitda < 1000 else 999,
            'market_insight': self._market_position_insight(ev_revenue, pe_ratio)
        }

    def _market_position_insight(self, ev_revenue: float, pe_ratio: float) -> str:
        """Provide insight on market position"""
        if ev_revenue > 10:
            return "Premium valuation suggests market values IP/intangibles highly"
        elif ev_revenue > 5:
            return "Above-average valuation indicates IP contributes to market value"
        else:
            return "Standard valuation multiples"

    def _analyze_risk_factors(self, balance_sheet: Dict, income_stmt: Dict,
                              cash_flow: Dict) -> Dict:
        """
        Analyze risk factors affecting IP value

        Risks:
        - Liquidity risk
        - Solvency risk
        - Volatility
        - Concentration risk
        """
        bs_data = balance_sheet.get('balance_sheets', [])
        income_data = income_stmt.get('income_statements', [])
        cf_data = cash_flow.get('cash_flow_statements', [])

        if not bs_data or not income_data:
            return {}

        latest_bs = bs_data[0]
        latest_income = income_data[0]

        # Liquidity: Can they pay bills?
        cash = latest_bs.get('cash_and_equivalents', 0)
        current_liabilities = latest_bs.get('current_liabilities', 0)
        cash_to_liabilities = cash / current_liabilities if current_liabilities > 0 else 0

        # Solvency: Long-term viability
        total_assets = latest_bs.get('total_assets', 0)
        total_liabilities = latest_bs.get('total_liabilities', 0)
        solvency_ratio = (total_assets - total_liabilities) / total_assets if total_assets > 0 else 0

        # Revenue volatility
        if len(income_data) >= 3:
            revenues = [stmt.get('revenue', 0) for stmt in income_data[:3]]
            revenue_volatility = self._calculate_volatility(revenues)
        else:
            revenue_volatility = 0

        return {
            'cash_to_liabilities': round(cash_to_liabilities, 2),
            'solvency_ratio': round(solvency_ratio, 4),
            'revenue_volatility': round(revenue_volatility, 4),
            'risk_assessment': self._overall_risk_assessment(cash_to_liabilities, solvency_ratio)
        }

    def _calculate_volatility(self, values: List[float]) -> float:
        """Calculate simple volatility measure"""
        if len(values) < 2:
            return 0

        changes = []
        for i in range(len(values) - 1):
            if values[i+1] > 0:
                change = abs((values[i] - values[i+1]) / values[i+1])
                changes.append(change)

        return sum(changes) / len(changes) if changes else 0

    def _overall_risk_assessment(self, liquidity: float, solvency: float) -> str:
        """Overall risk assessment"""
        if liquidity > 0.5 and solvency > 0.3:
            return "Low Risk - Strong financial position supports IP value stability"
        elif liquidity > 0.3 and solvency > 0.2:
            return "Moderate Risk - Adequate financial cushion"
        else:
            return "Higher Risk - Financial constraints may affect IP development/value"
