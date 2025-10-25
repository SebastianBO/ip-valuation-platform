"""
IP Valuation Engine with Financial Segmentation
Uses Financial Datasets API to perform segment-level IP valuations
"""

import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
import json


@dataclass
class IPAsset:
    """Represents an intellectual property asset"""
    id: str
    type: str  # 'patent', 'trademark', 'trade_secret', 'copyright'
    description: str
    related_segments: List[Dict[str, any]]  # [{'name': 'iPhone', 'attribution_pct': 0.6}]
    royalty_rate: float
    valuation_method: str = 'relief_from_royalty'

    # Optional fields for specific methods
    innovation_score: Optional[float] = None
    commercial_score: Optional[float] = None
    legal_strength_score: Optional[float] = None
    remaining_life_years: Optional[int] = None
    total_patent_life: int = 20


class FinancialDatasetsClient:
    """Client for Financial Datasets API"""

    def __init__(self, api_key: str, demo_mode: bool = False):
        self.api_key = api_key
        self.base_url = "https://api.financialdatasets.ai"
        self.headers = {"X-API-KEY": api_key}
        self.demo_mode = demo_mode

    def get_segmented_revenues(self, ticker: str, period: str = "annual", limit: int = 5) -> Dict:
        """
        Fetch segmented revenue data for a ticker

        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            period: 'annual' or 'quarterly'
            limit: Number of periods to retrieve

        Returns:
            JSON response with segmented revenue data
        """
        # Check demo mode first
        if self.demo_mode:
            from demo_data import get_demo_data
            demo = get_demo_data(ticker)
            if demo:
                return {'segmented_revenues': demo['segmented_revenues']}
            return {}

        url = f"{self.base_url}/financials/segmented-revenues/"
        params = {"ticker": ticker, "period": period, "limit": limit}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Check for insufficient credits error
            if isinstance(data, dict) and 'error' in data:
                if 'Insufficient credits' in data.get('message', ''):
                    print(f"⚠️ API credits exhausted. Switching to demo mode for {ticker}...")
                    self.demo_mode = True
                    from demo_data import get_demo_data
                    demo = get_demo_data(ticker)
                    if demo:
                        return {'segmented_revenues': demo['segmented_revenues']}

            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching segmented revenues: {e}")
            return {}

    def get_income_statement(self, ticker: str, period: str = "annual", limit: int = 5) -> Dict:
        """
        Fetch income statement data for a ticker

        Args:
            ticker: Stock ticker symbol
            period: 'annual' or 'quarterly'
            limit: Number of periods to retrieve

        Returns:
            JSON response with income statement data
        """
        # Check demo mode first
        if self.demo_mode:
            from demo_data import get_demo_data
            demo = get_demo_data(ticker)
            if demo:
                return {'income_statements': demo['income_statements']}
            return {}

        url = f"{self.base_url}/financials/income-statements/"
        params = {"ticker": ticker, "period": period, "limit": limit}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            # Check for insufficient credits error
            if isinstance(data, dict) and 'error' in data:
                if 'Insufficient credits' in data.get('message', ''):
                    print(f"⚠️ API credits exhausted. Switching to demo mode for {ticker}...")
                    self.demo_mode = True
                    from demo_data import get_demo_data
                    demo = get_demo_data(ticker)
                    if demo:
                        return {'income_statements': demo['income_statements']}

            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching income statement: {e}")
            return {}

    def get_all_statements(self, ticker: str, period: str = "annual", limit: int = 5) -> Dict:
        """
        Fetch all financial statements for a ticker

        Args:
            ticker: Stock ticker symbol
            period: 'annual' or 'quarterly'
            limit: Number of periods to retrieve

        Returns:
            JSON response with all financial statements
        """
        url = f"{self.base_url}/financials/all-financial-statements/"
        params = {"ticker": ticker, "period": period, "limit": limit}

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching all statements: {e}")
            return {}


class IPValuationEngine:
    """Main engine for IP valuation with financial segmentation"""

    def __init__(self, api_key: str):
        self.client = FinancialDatasetsClient(api_key)
        self.cache = {}

    def prepare_segment_financials(
        self,
        ticker: str,
        segment_name: str,
        years: int = 5
    ) -> Dict:
        """
        Prepare comprehensive financial data for a specific segment

        Args:
            ticker: Stock ticker symbol
            segment_name: Name of the segment (e.g., 'iPhone', 'Cloud Services')
            years: Number of years of historical data

        Returns:
            Dictionary with segment financial metrics
        """
        # Check cache
        cache_key = f"{ticker}_{segment_name}_{years}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Get data from API
        seg_data = self.client.get_segmented_revenues(ticker, limit=years)
        income_data = self.client.get_income_statement(ticker, limit=years)

        if not seg_data or not income_data:
            raise ValueError(f"Unable to fetch data for {ticker}")

        # Extract segment-specific revenues
        # API returns: {segmented_revenues: [{items: [{amount, segments: [{label}]}]}]}
        segment_revenues = []
        segment_name_lower = segment_name.lower().replace(' ', '').replace('-', '')

        for period_data in seg_data.get('segmented_revenues', []):
            found = False
            for item in period_data.get('items', []):
                # Check if this item matches our segment
                for seg_info in item.get('segments', []):
                    label = seg_info.get('label', '').lower().replace(' ', '').replace('-', '')
                    if label == segment_name_lower:
                        segment_revenues.append(item.get('amount', 0))
                        found = True
                        break
                if found:
                    break

        # Validate we found segment data
        if not segment_revenues:
            available_segments = set()
            for period_data in seg_data.get('segmented_revenues', []):
                for item in period_data.get('items', []):
                    for seg_info in item.get('segments', []):
                        available_segments.add(seg_info.get('label', ''))
            raise ValueError(f"Segment '{segment_name}' not found for {ticker}. Available segments: {sorted(available_segments)}")

        # Get company-wide metrics
        total_revenues = [period.get('revenue', 0) for period in income_data.get('income_statements', [])]
        gross_profits = [period.get('gross_profit', 0) for period in income_data.get('income_statements', [])]
        rd_expenses = [period.get('research_and_development', 0) for period in income_data.get('income_statements', [])]
        operating_incomes = [period.get('operating_income', 0) for period in income_data.get('income_statements', [])]

        # Calculate segment allocation percentages
        segment_allocation = []
        for seg_rev, total_rev in zip(segment_revenues, total_revenues):
            if total_rev > 0:
                segment_allocation.append(seg_rev / total_rev)
            else:
                segment_allocation.append(0)

        # Allocate R&D to segment proportionally
        segment_rd = [rd * alloc for rd, alloc in zip(rd_expenses, segment_allocation)]

        # Estimate segment gross profit using company-wide margin
        gp_margins = []
        segment_gp = []
        for gp, rev, seg_rev in zip(gross_profits, total_revenues, segment_revenues):
            if rev > 0:
                margin = gp / rev
                gp_margins.append(margin)
                segment_gp.append(seg_rev * margin)
            else:
                gp_margins.append(0)
                segment_gp.append(0)

        # Estimate segment operating income
        op_margins = []
        segment_op_income = []
        for op_inc, rev, seg_rev in zip(operating_incomes, total_revenues, segment_revenues):
            if rev > 0:
                margin = op_inc / rev
                op_margins.append(margin)
                segment_op_income.append(seg_rev * margin)
            else:
                op_margins.append(0)
                segment_op_income.append(0)

        result = {
            'ticker': ticker,
            'segment_name': segment_name,
            'revenues': segment_revenues,
            'gross_profits': segment_gp,
            'gp_margins': gp_margins,
            'rd_expenses': segment_rd,
            'operating_incomes': segment_op_income,
            'operating_margins': op_margins,
            'allocation_pct': segment_allocation,
            'years': len(segment_revenues)
        }

        # Cache result
        self.cache[cache_key] = result

        return result

    def relief_from_royalty(
        self,
        segment_revenues: List[float],
        royalty_rate: float,
        tax_rate: float,
        wacc: float,
        attribution_pct: float = 1.0,
        terminal_growth: float = 0.02
    ) -> Dict:
        """
        Calculate IP value using Relief from Royalty method

        Args:
            segment_revenues: List of annual revenues for the segment
            royalty_rate: Hypothetical royalty rate (e.g., 0.05 for 5%)
            tax_rate: Corporate tax rate
            wacc: Weighted average cost of capital (discount rate)
            attribution_pct: % of segment revenue attributable to this IP
            terminal_growth: Terminal growth rate for perpetuity value

        Returns:
            Dictionary with valuation results
        """
        pv_royalties = 0
        yearly_details = []

        # Present value of royalty savings during explicit forecast period
        for year, revenue in enumerate(segment_revenues, start=1):
            annual_royalty_savings = revenue * royalty_rate * (1 - tax_rate) * attribution_pct
            discount_factor = (1 + wacc) ** year
            pv = annual_royalty_savings / discount_factor
            pv_royalties += pv

            yearly_details.append({
                'year': year,
                'revenue': revenue,
                'royalty_savings': annual_royalty_savings,
                'discount_factor': discount_factor,
                'present_value': pv
            })

        # Terminal value (perpetuity)
        last_revenue = segment_revenues[-1]
        terminal_revenue = last_revenue * (1 + terminal_growth)
        terminal_royalty = terminal_revenue * royalty_rate * (1 - tax_rate) * attribution_pct
        terminal_value = terminal_royalty / (wacc - terminal_growth)
        pv_terminal = terminal_value / ((1 + wacc) ** len(segment_revenues))

        total_value = pv_royalties + pv_terminal

        return {
            'method': 'Relief from Royalty',
            'pv_explicit_period': pv_royalties,
            'pv_terminal_value': pv_terminal,
            'total_value': total_value,
            'yearly_details': yearly_details,
            'assumptions': {
                'royalty_rate': royalty_rate,
                'tax_rate': tax_rate,
                'wacc': wacc,
                'attribution_pct': attribution_pct,
                'terminal_growth': terminal_growth
            }
        }

    def multi_period_excess_earnings(
        self,
        segment_revenues: List[float],
        operating_margin: float,
        contributory_assets: Dict[str, float],
        ip_contribution_pct: float,
        wacc: float,
        tax_rate: float,
        terminal_growth: float = 0.02
    ) -> Dict:
        """
        Calculate IP value using Multi-Period Excess Earnings Method

        Args:
            segment_revenues: List of annual revenues
            operating_margin: Segment operating margin
            contributory_assets: Dict of asset types and required return rates
                e.g., {'working_capital': 0.03, 'fixed_assets': 0.12}
            ip_contribution_pct: % of excess earnings attributable to this IP
            wacc: Discount rate
            tax_rate: Corporate tax rate
            terminal_growth: Terminal growth rate

        Returns:
            Dictionary with valuation results
        """
        pv_excess_earnings = 0
        yearly_details = []

        for year, revenue in enumerate(segment_revenues, start=1):
            # Operating income for segment
            operating_income = revenue * operating_margin

            # Calculate contributory asset charges
            # Using simplified revenue-based proxy for asset values
            total_cac = 0
            for asset_type, return_rate in contributory_assets.items():
                asset_value_proxy = revenue * 0.5  # Simplified assumption
                charge = asset_value_proxy * return_rate
                total_cac += charge

            # Excess earnings after contributory asset charges
            excess_earnings = operating_income - total_cac

            # Portion attributable to this IP
            ip_earnings = excess_earnings * ip_contribution_pct

            # After-tax cash flow
            ip_cash_flow = ip_earnings * (1 - tax_rate)

            # Present value
            discount_factor = (1 + wacc) ** year
            pv = ip_cash_flow / discount_factor
            pv_excess_earnings += pv

            yearly_details.append({
                'year': year,
                'revenue': revenue,
                'operating_income': operating_income,
                'contributory_asset_charges': total_cac,
                'excess_earnings': excess_earnings,
                'ip_earnings': ip_earnings,
                'ip_cash_flow': ip_cash_flow,
                'present_value': pv
            })

        # Terminal value
        last_revenue = segment_revenues[-1]
        terminal_revenue = last_revenue * (1 + terminal_growth)
        terminal_operating_income = terminal_revenue * operating_margin
        terminal_cac = sum(contributory_assets.values()) * terminal_revenue * 0.5
        terminal_excess = terminal_operating_income - terminal_cac
        terminal_ip_cf = terminal_excess * ip_contribution_pct * (1 - tax_rate)
        terminal_value = terminal_ip_cf / (wacc - terminal_growth)
        pv_terminal = terminal_value / ((1 + wacc) ** len(segment_revenues))

        total_value = pv_excess_earnings + pv_terminal

        return {
            'method': 'Multi-Period Excess Earnings',
            'pv_explicit_period': pv_excess_earnings,
            'pv_terminal_value': pv_terminal,
            'total_value': total_value,
            'yearly_details': yearly_details,
            'assumptions': {
                'operating_margin': operating_margin,
                'contributory_assets': contributory_assets,
                'ip_contribution_pct': ip_contribution_pct,
                'wacc': wacc,
                'tax_rate': tax_rate,
                'terminal_growth': terminal_growth
            }
        }

    def technology_factor_valuation(
        self,
        segment_revenues: List[float],
        base_royalty_rate: float,
        innovation_score: float,
        commercial_score: float,
        legal_strength_score: float,
        remaining_life_years: int,
        total_patent_life: int,
        tax_rate: float,
        wacc: float
    ) -> Dict:
        """
        Value patent using Technology Factor Method
        Adjusts royalty rate based on patent quality factors

        Args:
            segment_revenues: List of annual revenues
            base_royalty_rate: Base royalty rate before adjustments
            innovation_score: 0-1 scale, novelty of invention
            commercial_score: 0-1 scale, market success
            legal_strength_score: 0-1 scale, patent strength
            remaining_life_years: Years until patent expiration
            total_patent_life: Total patent life (usually 20 years)
            tax_rate: Corporate tax rate
            wacc: Discount rate

        Returns:
            Dictionary with valuation results
        """
        # Calculate technology factor (weighted average)
        tech_factor = (
            innovation_score * 0.30 +
            commercial_score * 0.35 +
            legal_strength_score * 0.25 +
            (remaining_life_years / total_patent_life) * 0.10
        )

        # Adjusted royalty rate
        adjusted_royalty_rate = base_royalty_rate * (1 + tech_factor)

        pv_royalties = 0
        yearly_details = []

        # Limit projection to remaining patent life
        projection_years = min(len(segment_revenues), remaining_life_years)

        for year in range(1, projection_years + 1):
            if year <= len(segment_revenues):
                revenue = segment_revenues[year - 1]
            else:
                revenue = segment_revenues[-1]

            # Decay factor: patents lose value as they approach expiration
            decay = 1 - (year / (remaining_life_years * 1.5))
            decay = max(decay, 0.3)  # Minimum 30% of value maintained

            annual_royalty_savings = revenue * adjusted_royalty_rate * (1 - tax_rate) * decay
            discount_factor = (1 + wacc) ** year
            pv = annual_royalty_savings / discount_factor
            pv_royalties += pv

            yearly_details.append({
                'year': year,
                'revenue': revenue,
                'decay_factor': decay,
                'royalty_savings': annual_royalty_savings,
                'present_value': pv
            })

        return {
            'method': 'Technology Factor',
            'total_value': pv_royalties,
            'yearly_details': yearly_details,
            'assumptions': {
                'base_royalty_rate': base_royalty_rate,
                'adjusted_royalty_rate': adjusted_royalty_rate,
                'technology_factor': tech_factor,
                'innovation_score': innovation_score,
                'commercial_score': commercial_score,
                'legal_strength_score': legal_strength_score,
                'remaining_life_years': remaining_life_years,
                'tax_rate': tax_rate,
                'wacc': wacc
            }
        }

    def value_ip_asset(
        self,
        ticker: str,
        ip_asset: IPAsset,
        wacc: float = 0.10,
        tax_rate: float = 0.21,
        terminal_growth: float = 0.02,
        years: int = 5
    ) -> Dict:
        """
        Value an IP asset using the specified method and segment data

        Args:
            ticker: Stock ticker symbol
            ip_asset: IPAsset object with asset details
            wacc: Weighted average cost of capital
            tax_rate: Corporate tax rate
            terminal_growth: Terminal growth rate
            years: Number of years of historical data to use

        Returns:
            Dictionary with complete valuation results
        """
        total_value = 0
        segment_valuations = []

        # Value IP across all related segments
        for segment_info in ip_asset.related_segments:
            segment_name = segment_info['name']
            segment_attribution = segment_info['attribution_pct']

            # Get segment financial data
            try:
                segment_data = self.prepare_segment_financials(ticker, segment_name, years)
            except Exception as e:
                print(f"Error preparing segment data for {segment_name}: {e}")
                continue

            # Apply attribution percentage to revenues
            attributed_revenues = [
                rev * segment_attribution
                for rev in segment_data['revenues']
            ]

            # Select valuation method
            if ip_asset.valuation_method == 'relief_from_royalty':
                result = self.relief_from_royalty(
                    segment_revenues=attributed_revenues,
                    royalty_rate=ip_asset.royalty_rate,
                    tax_rate=tax_rate,
                    wacc=wacc,
                    attribution_pct=1.0,  # Already applied to revenues
                    terminal_growth=terminal_growth
                )

            elif ip_asset.valuation_method == 'excess_earnings':
                avg_op_margin = sum(segment_data['operating_margins']) / len(segment_data['operating_margins'])

                result = self.multi_period_excess_earnings(
                    segment_revenues=attributed_revenues,
                    operating_margin=avg_op_margin,
                    contributory_assets={
                        'working_capital': 0.02,
                        'fixed_assets': 0.10,
                        'other_intangibles': 0.12
                    },
                    ip_contribution_pct=0.50,
                    wacc=wacc,
                    tax_rate=tax_rate,
                    terminal_growth=terminal_growth
                )

            elif ip_asset.valuation_method == 'technology_factor':
                result = self.technology_factor_valuation(
                    segment_revenues=attributed_revenues,
                    base_royalty_rate=ip_asset.royalty_rate,
                    innovation_score=ip_asset.innovation_score or 0.7,
                    commercial_score=ip_asset.commercial_score or 0.7,
                    legal_strength_score=ip_asset.legal_strength_score or 0.7,
                    remaining_life_years=ip_asset.remaining_life_years or 10,
                    total_patent_life=ip_asset.total_patent_life,
                    tax_rate=tax_rate,
                    wacc=wacc
                )

            else:
                raise ValueError(f"Unknown valuation method: {ip_asset.valuation_method}")

            # Add segment context to result
            result['segment'] = segment_name
            result['segment_attribution'] = segment_attribution
            result['segment_data'] = segment_data

            segment_valuations.append(result)
            total_value += result['total_value']

        return {
            'ip_asset_id': ip_asset.id,
            'ip_type': ip_asset.type,
            'description': ip_asset.description,
            'ticker': ticker,
            'total_value': total_value,
            'segment_valuations': segment_valuations,
            'valuation_date': 'latest_available'
        }

    def value_ip_portfolio(
        self,
        ticker: str,
        ip_portfolio: List[IPAsset],
        wacc: float = 0.10,
        tax_rate: float = 0.21,
        terminal_growth: float = 0.02
    ) -> Dict:
        """
        Value entire IP portfolio for a company

        Args:
            ticker: Stock ticker symbol
            ip_portfolio: List of IPAsset objects
            wacc: Weighted average cost of capital
            tax_rate: Corporate tax rate
            terminal_growth: Terminal growth rate

        Returns:
            Dictionary with portfolio valuation results
        """
        portfolio_value = 0
        asset_valuations = []

        for ip_asset in ip_portfolio:
            try:
                valuation = self.value_ip_asset(
                    ticker=ticker,
                    ip_asset=ip_asset,
                    wacc=wacc,
                    tax_rate=tax_rate,
                    terminal_growth=terminal_growth
                )

                portfolio_value += valuation['total_value']
                asset_valuations.append(valuation)

            except Exception as e:
                print(f"Error valuing IP asset {ip_asset.id}: {e}")
                continue

        return {
            'ticker': ticker,
            'total_portfolio_value': portfolio_value,
            'asset_count': len(asset_valuations),
            'asset_valuations': asset_valuations,
            'assumptions': {
                'wacc': wacc,
                'tax_rate': tax_rate,
                'terminal_growth': terminal_growth
            }
        }


def main():
    """Example usage of the IP Valuation Engine"""

    # Initialize engine with API key
    # In production, get this from environment variables or secure storage
    import os
    api_key = os.getenv("FINANCIAL_DATASETS_API_KEY", "your_api_key_here")

    if api_key == "your_api_key_here":
        print("Please set FINANCIAL_DATASETS_API_KEY environment variable")
        return

    engine = IPValuationEngine(api_key)

    # Define example IP assets for Apple
    apple_ip_portfolio = [
        IPAsset(
            id='PAT-FACEID-001',
            type='patent',
            description='Face ID facial recognition technology',
            related_segments=[
                {'name': 'iPhone', 'attribution_pct': 0.12},
                {'name': 'iPad', 'attribution_pct': 0.08}
            ],
            royalty_rate=0.045,
            valuation_method='relief_from_royalty'
        ),
        IPAsset(
            id='TM-IPHONE-001',
            type='trademark',
            description='iPhone trademark and brand',
            related_segments=[
                {'name': 'iPhone', 'attribution_pct': 0.25}
            ],
            royalty_rate=0.06,
            valuation_method='relief_from_royalty'
        ),
        IPAsset(
            id='PAT-CHIP-001',
            type='patent',
            description='A-series chip architecture',
            related_segments=[
                {'name': 'iPhone', 'attribution_pct': 0.10},
                {'name': 'iPad', 'attribution_pct': 0.10},
                {'name': 'Mac', 'attribution_pct': 0.15}
            ],
            royalty_rate=0.05,
            innovation_score=0.92,
            commercial_score=0.88,
            legal_strength_score=0.90,
            remaining_life_years=12,
            valuation_method='technology_factor'
        )
    ]

    # Value the portfolio
    print("Valuing Apple IP Portfolio...\n")

    try:
        portfolio_result = engine.value_ip_portfolio(
            ticker='AAPL',
            ip_portfolio=apple_ip_portfolio,
            wacc=0.095,
            tax_rate=0.21,
            terminal_growth=0.025
        )

        # Print results
        print("=" * 80)
        print(f"IP PORTFOLIO VALUATION: {portfolio_result['ticker']}")
        print("=" * 80)
        print(f"\nTotal Portfolio Value: ${portfolio_result['total_portfolio_value']:,.0f}")
        print(f"Number of Assets Valued: {portfolio_result['asset_count']}")
        print(f"\nAssumptions:")
        print(f"  - WACC: {portfolio_result['assumptions']['wacc']:.1%}")
        print(f"  - Tax Rate: {portfolio_result['assumptions']['tax_rate']:.1%}")
        print(f"  - Terminal Growth: {portfolio_result['assumptions']['terminal_growth']:.1%}")

        print("\n" + "=" * 80)
        print("INDIVIDUAL ASSET VALUATIONS")
        print("=" * 80)

        for asset_val in portfolio_result['asset_valuations']:
            print(f"\n{asset_val['description']}")
            print(f"  ID: {asset_val['ip_asset_id']}")
            print(f"  Type: {asset_val['ip_type']}")
            print(f"  Total Value: ${asset_val['total_value']:,.0f}")
            print(f"  Segments:")

            for seg_val in asset_val['segment_valuations']:
                print(f"    - {seg_val['segment']}: ${seg_val['total_value']:,.0f}")
                print(f"      Method: {seg_val['method']}")
                print(f"      Attribution: {seg_val['segment_attribution']:.0%}")

        # Save results to JSON
        with open('ip_valuation_results.json', 'w') as f:
            json.dump(portfolio_result, f, indent=2, default=str)

        print("\n" + "=" * 80)
        print("Full results saved to: ip_valuation_results.json")
        print("=" * 80)

    except Exception as e:
        print(f"Error during valuation: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
