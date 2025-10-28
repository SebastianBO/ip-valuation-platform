"""
Biotech/Pharma IP Valuation Module
Specialized analysis for drug patents, gene therapies, and clinical pipelines
"""

import requests
from typing import Dict, List
from datetime import datetime, timedelta


class BiotechIPAnalyzer:
    """
    Specialized IP analyzer for biotech/pharma companies

    Key IP Types:
    - Drug patents (small molecule, biologics)
    - Gene therapy IP
    - Clinical trial data exclusivity
    - Orphan drug exclusivity
    - Manufacturing process patents
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.financialdatasets.ai"
        self.headers = {"X-API-KEY": api_key}

    def analyze_biotech_ip(self, ticker: str, company_name: str = None) -> Dict:
        """
        Comprehensive biotech IP analysis

        For companies like Sarepta Therapeutics (SRPT), analyzes:
        - Drug pipeline (approved + in development)
        - Patent portfolio value
        - Market exclusivity periods
        - Revenue concentration by drug
        - Patent cliff risks
        """
        analysis = {
            'ticker': ticker,
            'company_name': company_name or ticker,
            'drug_portfolio': {},
            'patent_analysis': {},
            'risk_assessment': {},
            'valuation_breakdown': {},
            'competitive_moat': {}
        }

        # Get financial data
        financial_data = self._get_financial_data(ticker)

        # Identify revenue-generating drugs
        analysis['drug_portfolio'] = self._identify_drug_products(ticker, financial_data)

        # Analyze patent protection
        analysis['patent_analysis'] = self._analyze_patent_protection(
            ticker, analysis['drug_portfolio']
        )

        # Risk assessment (patent expiration, competition)
        analysis['risk_assessment'] = self._assess_biotech_risks(
            analysis['drug_portfolio'], analysis['patent_analysis']
        )

        # Value breakdown by drug/indication
        analysis['valuation_breakdown'] = self._value_drug_portfolio(
            ticker, analysis['drug_portfolio'], financial_data
        )

        # Competitive moat strength
        analysis['competitive_moat'] = self._assess_competitive_moat(
            ticker, analysis['patent_analysis']
        )

        return analysis

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

        # Segmented revenues (if available)
        url = f"{self.base_url}/financials/segmented-revenues/"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            data['segments'] = response.json()
        except:
            data['segments'] = {}

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

    def _identify_drug_products(self, ticker: str, financial_data: Dict) -> Dict:
        """
        Identify key drug products and their characteristics

        For SRPT (example):
        - EXONDYS 51 (exon 51 skipping)
        - VYONDYS 53 (exon 53 skipping)
        - AMONDYS 45 (exon 45 skipping)
        - ELEVIDYS (gene therapy)
        - SRP-9003 (pipeline - LGMD)
        """
        # This would ideally pull from a drugs database or SEC filings
        # For now, we'll create a framework based on known biotech patterns

        known_drugs = {
            'SRPT': {
                'EXONDYS 51': {
                    'indication': 'Duchenne muscular dystrophy (DMD) - Exon 51',
                    'approval_date': '2016-09-19',
                    'type': 'Antisense oligonucleotide',
                    'market_exclusivity': 7,  # years (orphan drug)
                    'patent_expiry': '2031',
                    'peak_sales_estimate': 500_000_000,
                    'current_status': 'Approved & Commercial'
                },
                'VYONDYS 53': {
                    'indication': 'Duchenne muscular dystrophy (DMD) - Exon 53',
                    'approval_date': '2019-12-12',
                    'type': 'Antisense oligonucleotide',
                    'market_exclusivity': 7,
                    'patent_expiry': '2033',
                    'peak_sales_estimate': 300_000_000,
                    'current_status': 'Approved & Commercial'
                },
                'AMONDYS 45': {
                    'indication': 'Duchenne muscular dystrophy (DMD) - Exon 45',
                    'approval_date': '2021-02-25',
                    'type': 'Antisense oligonucleotide',
                    'market_exclusivity': 7,
                    'patent_expiry': '2035',
                    'peak_sales_estimate': 400_000_000,
                    'current_status': 'Approved & Commercial'
                },
                'ELEVIDYS': {
                    'indication': 'Duchenne muscular dystrophy (DMD) - Gene Therapy',
                    'approval_date': '2023-06-22',
                    'type': 'Gene therapy (AAV)',
                    'market_exclusivity': 12,  # Biologics get 12 years
                    'patent_expiry': '2040',
                    'peak_sales_estimate': 2_000_000_000,  # Blockbuster potential
                    'current_status': 'Approved & Ramping'
                },
                'SRP-9003': {
                    'indication': 'Limb-girdle muscular dystrophy (LGMD)',
                    'approval_date': None,  # In development
                    'type': 'Gene therapy',
                    'market_exclusivity': 12,
                    'patent_expiry': '2042',
                    'peak_sales_estimate': 800_000_000,
                    'current_status': 'Phase 2 Clinical Trials',
                    'approval_probability': 0.30  # Phase 2 success rate ~30%
                }
            }
        }

        return known_drugs.get(ticker, self._generic_drug_analysis(ticker, financial_data))

    def _generic_drug_analysis(self, ticker: str, financial_data: Dict) -> Dict:
        """Generic analysis for unknown biotech companies"""
        # Estimate based on revenue, R&D spend, margins
        income_data = financial_data.get('income', {}).get('income_statements', [])

        if not income_data:
            return {}

        latest = income_data[0]
        revenue = latest.get('revenue', 0)
        rd_expense = latest.get('research_and_development', 0)

        # Estimate number of products based on revenue size
        if revenue > 2_000_000_000:
            estimated_products = 4  # Large portfolio
        elif revenue > 500_000_000:
            estimated_products = 2  # Mid-size
        else:
            estimated_products = 1  # Single product or early stage

        return {
            'estimated_products': estimated_products,
            'total_revenue': revenue,
            'rd_investment': rd_expense,
            'note': 'Generic analysis - specific drug data not available'
        }

    def _analyze_patent_protection(self, ticker: str, drug_portfolio: Dict) -> Dict:
        """
        Analyze patent protection strength

        Key factors:
        - Patent expiration dates
        - Market exclusivity periods
        - Patent cliff risks
        - Generic competition timeline
        """
        patent_analysis = {
            'by_drug': {},
            'overall_risk': 'Low',
            'patent_cliff_years': [],
            'average_remaining_protection': 0
        }

        current_year = datetime.now().year
        total_protection_years = 0
        drug_count = 0

        for drug_name, drug_info in drug_portfolio.items():
            if isinstance(drug_info, dict) and 'patent_expiry' in drug_info:
                patent_expiry = int(drug_info['patent_expiry'])
                years_remaining = patent_expiry - current_year

                exclusivity_years = drug_info.get('market_exclusivity', 0)
                approval_date = drug_info.get('approval_date')

                if approval_date:
                    approval_year = int(approval_date.split('-')[0])
                    exclusivity_expiry = approval_year + exclusivity_years
                    years_until_exclusivity_ends = exclusivity_expiry - current_year
                else:
                    years_until_exclusivity_ends = exclusivity_years

                # Effective protection is the longer of patent or exclusivity
                effective_protection = max(years_remaining, years_until_exclusivity_ends)

                patent_analysis['by_drug'][drug_name] = {
                    'patent_expiry_year': patent_expiry,
                    'years_until_patent_expiry': years_remaining,
                    'exclusivity_years_remaining': years_until_exclusivity_ends,
                    'effective_protection_years': effective_protection,
                    'risk_level': self._assess_patent_risk(effective_protection)
                }

                # Check for patent cliff (multiple drugs expiring in same period)
                if effective_protection <= 5:
                    patent_analysis['patent_cliff_years'].append(current_year + effective_protection)

                total_protection_years += effective_protection
                drug_count += 1

        if drug_count > 0:
            patent_analysis['average_remaining_protection'] = total_protection_years / drug_count

        # Overall risk assessment
        if patent_analysis['average_remaining_protection'] < 5:
            patent_analysis['overall_risk'] = 'High'
        elif patent_analysis['average_remaining_protection'] < 10:
            patent_analysis['overall_risk'] = 'Moderate'
        else:
            patent_analysis['overall_risk'] = 'Low'

        # Patent cliff detection
        if len(patent_analysis['patent_cliff_years']) >= 2:
            patent_analysis['patent_cliff_warning'] = f"Multiple patents expiring around {min(patent_analysis['patent_cliff_years'])}"

        return patent_analysis

    def _assess_patent_risk(self, years_remaining: int) -> str:
        """Assess risk level based on remaining protection"""
        if years_remaining <= 3:
            return 'Critical - Generic competition imminent'
        elif years_remaining <= 5:
            return 'High - Plan for revenue decline'
        elif years_remaining <= 10:
            return 'Moderate - Monitor biosimilar development'
        else:
            return 'Low - Strong protection period'

    def _assess_biotech_risks(self, drug_portfolio: Dict, patent_analysis: Dict) -> Dict:
        """
        Comprehensive risk assessment

        Risks specific to biotech:
        - Clinical trial failures
        - Regulatory delays
        - Patent invalidation
        - Generic/biosimilar competition
        - Reimbursement pressure
        - Manufacturing issues (especially gene therapy)
        """
        risks = {
            'patent_risks': [],
            'pipeline_risks': [],
            'commercial_risks': [],
            'overall_risk_score': 0  # 0-100 scale
        }

        # Patent risks
        if patent_analysis.get('overall_risk') == 'High':
            risks['patent_risks'].append({
                'type': 'Patent Expiration',
                'severity': 'High',
                'description': 'Multiple key patents expiring within 5 years',
                'impact': 'Revenue decline from generic competition'
            })

        # Pipeline risks (for drugs in development)
        for drug_name, drug_info in drug_portfolio.items():
            if isinstance(drug_info, dict):
                status = drug_info.get('current_status', '')

                if 'Phase' in status or 'Clinical' in status:
                    prob_success = drug_info.get('approval_probability', 0.5)

                    risks['pipeline_risks'].append({
                        'drug': drug_name,
                        'type': 'Clinical Development Risk',
                        'severity': 'High' if prob_success < 0.3 else 'Moderate',
                        'probability_of_success': prob_success,
                        'impact': f"Potential loss of ${drug_info.get('peak_sales_estimate', 0)/1e6:.0f}M peak sales"
                    })

        # Commercial risks
        # Check for revenue concentration
        approved_drugs = [d for d, info in drug_portfolio.items()
                         if isinstance(info, dict) and 'Approved' in info.get('current_status', '')]

        if len(approved_drugs) <= 2:
            risks['commercial_risks'].append({
                'type': 'Revenue Concentration',
                'severity': 'High',
                'description': f'Revenue dependent on {len(approved_drugs)} product(s)',
                'impact': 'Single product failure could be catastrophic'
            })

        # Calculate overall risk score
        risk_score = 0
        risk_score += len(risks['patent_risks']) * 30
        risk_score += len(risks['pipeline_risks']) * 20
        risk_score += len(risks['commercial_risks']) * 25
        risks['overall_risk_score'] = min(risk_score, 100)

        return risks

    def _value_drug_portfolio(self, ticker: str, drug_portfolio: Dict,
                              financial_data: Dict) -> Dict:
        """
        Value each drug using probability-adjusted NPV

        Method: Risk-adjusted NPV for biotech
        - Approved drugs: Full revenue projections
        - Pipeline drugs: Success probability × NPV
        """
        valuation = {
            'by_drug': {},
            'total_portfolio_value': 0,
            'approved_products_value': 0,
            'pipeline_value': 0
        }

        # Get company metrics for discount rate
        metrics = financial_data.get('metrics', {}).get('snapshot', {})

        # Higher discount rate for biotech (riskier than average)
        base_wacc = 0.12  # 12% for biotech

        for drug_name, drug_info in drug_portfolio.items():
            if not isinstance(drug_info, dict):
                continue

            peak_sales = drug_info.get('peak_sales_estimate', 0)
            status = drug_info.get('current_status', '')

            # Probability adjustment
            if 'Approved' in status:
                probability = 1.0
            else:
                probability = drug_info.get('approval_probability', 0.3)

            # Patent protection remaining
            patent_expiry = drug_info.get('patent_expiry')
            if patent_expiry:
                years_protected = int(patent_expiry) - datetime.now().year
            else:
                years_protected = 10  # Default

            # Simple NPV calculation
            # Assume drug reaches peak sales in 3 years, maintains for patent life
            npv = 0
            for year in range(1, min(years_protected + 1, 20)):  # Cap at 20 years
                if year <= 3:
                    revenue = peak_sales * (year / 3)  # Ramp up
                elif year <= years_protected:
                    revenue = peak_sales  # Peak
                else:
                    revenue = peak_sales * 0.1  # 90% decline post-patent

                # Discount to present
                discount_factor = (1 + base_wacc) ** year
                npv += (revenue * 0.3) / discount_factor  # Assume 30% margin

            # Apply probability
            risk_adjusted_value = npv * probability

            valuation['by_drug'][drug_name] = {
                'peak_sales_estimate': peak_sales,
                'years_of_protection': years_protected,
                'probability_of_success': probability,
                'npv': npv,
                'risk_adjusted_value': risk_adjusted_value,
                'status': status
            }

            # Add to totals
            if 'Approved' in status:
                valuation['approved_products_value'] += risk_adjusted_value
            else:
                valuation['pipeline_value'] += risk_adjusted_value

        valuation['total_portfolio_value'] = (
            valuation['approved_products_value'] +
            valuation['pipeline_value']
        )

        return valuation

    def _assess_competitive_moat(self, ticker: str, patent_analysis: Dict) -> Dict:
        """
        Assess competitive moat strength

        For biotech, moat comes from:
        - Patent protection
        - Orphan drug status
        - First-mover advantage
        - Manufacturing complexity (gene therapy)
        - Clinical trial data exclusivity
        """
        moat = {
            'strength': 'Moderate',
            'duration_years': 0,
            'sources': [],
            'threats': []
        }

        avg_protection = patent_analysis.get('average_remaining_protection', 0)

        # Assess moat strength
        if avg_protection > 15:
            moat['strength'] = 'Very Strong'
            moat['sources'].append('Long patent protection (>15 years)')
        elif avg_protection > 10:
            moat['strength'] = 'Strong'
            moat['sources'].append('Solid patent protection (10-15 years)')
        elif avg_protection > 5:
            moat['strength'] = 'Moderate'
            moat['sources'].append('Moderate patent protection (5-10 years)')
        else:
            moat['strength'] = 'Weak'
            moat['threats'].append('Limited patent protection (<5 years)')

        moat['duration_years'] = int(avg_protection)

        # Additional moat sources
        moat['sources'].extend([
            'Orphan drug exclusivity (7-12 years)',
            'Clinical trial data exclusivity',
            'Rare disease focus (limited competition)',
            'Gene therapy complexity (high barriers to entry)'
        ])

        # Threats
        if patent_analysis.get('overall_risk') == 'High':
            moat['threats'].append('Patent cliff approaching')

        moat['threats'].extend([
            'Biosimilar development',
            'CRISPR/gene editing alternatives',
            'Payer reimbursement pressure',
            'Manufacturing scale-up challenges'
        ])

        return moat


def create_biotech_ip_report(ticker: str, api_key: str) -> Dict:
    """
    Generate comprehensive biotech IP valuation report

    Example for SRPT (Sarepta Therapeutics):
    - 4 approved drugs (EXONDYS, VYONDYS, AMONDYS, ELEVIDYS)
    - 1 pipeline asset (SRP-9003)
    - Focus on rare diseases (DMD, LGMD)
    - Gene therapy platform
    """
    analyzer = BiotechIPAnalyzer(api_key)

    return analyzer.analyze_biotech_ip(ticker)
