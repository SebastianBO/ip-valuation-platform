"""
IP Asset Discovery Module
Automatically identifies and suggests IP assets based on company segments
"""

from typing import List, Dict
from ip_valuation_engine import IPAsset


class IPAssetDiscovery:
    """Automatically discover and suggest IP assets for a company"""

    def __init__(self):
        # Industry-specific royalty rates
        self.royalty_rates = {
            'software': 0.08,
            'hardware': 0.04,
            'pharmaceutical': 0.12,
            'consumer_brand': 0.06,
            'technology': 0.05,
            'services': 0.07,
            'biotech': 0.15,
            'semiconductor': 0.05,
            'telecommunications': 0.04,
            'automotive': 0.03
        }

        # Segment-to-IP type mapping
        self.segment_ip_mapping = {
            'iphone': ['patent', 'trademark', 'design'],
            'ipad': ['patent', 'trademark', 'design'],
            'mac': ['patent', 'trademark', 'design'],
            'services': ['copyright', 'trade_secret', 'trademark'],
            'cloud': ['trade_secret', 'patent'],
            'software': ['copyright', 'trade_secret'],
            'wearables': ['patent', 'design', 'trademark'],
        }

    def discover_ip_assets(self, ticker: str, segments: List[str], company_info: Dict = None) -> List[IPAsset]:
        """
        Automatically discover potential IP assets for a company

        Args:
            ticker: Stock ticker symbol
            segments: List of business segment names
            company_info: Optional company metadata

        Returns:
            List of suggested IPAsset objects
        """
        discovered_assets = []

        for segment in segments:
            segment_lower = segment.lower().replace(' ', '').replace('-', '')

            # Generate potential IP assets for this segment
            assets = self._generate_segment_ip(ticker, segment, segment_lower)
            discovered_assets.extend(assets)

        return discovered_assets

    def _generate_segment_ip(self, ticker: str, segment_name: str, segment_lower: str) -> List[IPAsset]:
        """Generate IP assets for a specific segment"""
        assets = []

        # Brand/Trademark (always generate for product segments)
        if not any(x in segment_lower for x in ['service', 'other', 'corporate']):
            trademark = self._create_trademark(ticker, segment_name, segment_lower)
            if trademark:
                assets.append(trademark)

        # Technology Patents
        if any(x in segment_lower for x in ['phone', 'pad', 'mac', 'watch', 'technology', 'hardware']):
            patents = self._create_technology_patents(ticker, segment_name, segment_lower)
            assets.extend(patents)

        # Software/Trade Secrets
        if any(x in segment_lower for x in ['service', 'software', 'cloud', 'platform']):
            trade_secrets = self._create_trade_secrets(ticker, segment_name, segment_lower)
            assets.extend(trade_secrets)

        return assets

    def _create_trademark(self, ticker: str, segment_name: str, segment_lower: str) -> IPAsset:
        """Create trademark asset for a segment"""
        # Determine attribution based on brand strength
        attribution = 0.25  # Default: strong brand

        if 'iphone' in segment_lower:
            attribution = 0.25  # Very strong brand
        elif 'ipad' in segment_lower or 'mac' in segment_lower:
            attribution = 0.20
        elif 'watch' in segment_lower or 'wearable' in segment_lower:
            attribution = 0.15
        else:
            attribution = 0.12

        return IPAsset(
            id=f'TM-{segment_name.upper()}-001',
            type='trademark',
            description=f'{segment_name} brand and trademark',
            related_segments=[{'name': segment_name, 'attribution_pct': attribution}],
            royalty_rate=self.royalty_rates.get('consumer_brand', 0.06),
            valuation_method='relief_from_royalty'
        )

    def _create_technology_patents(self, ticker: str, segment_name: str, segment_lower: str) -> List[IPAsset]:
        """Create technology patent assets"""
        patents = []

        # Determine if this is a hardware product
        is_hardware = any(x in segment_lower for x in ['phone', 'pad', 'mac', 'watch', 'pod'])

        if is_hardware:
            # Core technology patent
            core_patent = IPAsset(
                id=f'PAT-{segment_name.upper()}-CORE-001',
                type='patent',
                description=f'{segment_name} core technology patents',
                related_segments=[{'name': segment_name, 'attribution_pct': 0.15}],
                royalty_rate=self.royalty_rates.get('technology', 0.05),
                innovation_score=0.80,
                commercial_score=0.85,
                legal_strength_score=0.80,
                remaining_life_years=10,
                valuation_method='technology_factor'
            )
            patents.append(core_patent)

            # Design patents
            design_patent = IPAsset(
                id=f'PAT-{segment_name.upper()}-DESIGN-001',
                type='patent',
                description=f'{segment_name} industrial design patents',
                related_segments=[{'name': segment_name, 'attribution_pct': 0.08}],
                royalty_rate=0.03,
                innovation_score=0.85,
                commercial_score=0.90,
                legal_strength_score=0.75,
                remaining_life_years=12,
                valuation_method='technology_factor'
            )
            patents.append(design_patent)

        return patents

    def _create_trade_secrets(self, ticker: str, segment_name: str, segment_lower: str) -> List[IPAsset]:
        """Create trade secret/software assets"""
        trade_secrets = []

        # Software/algorithms
        if any(x in segment_lower for x in ['service', 'cloud', 'software', 'platform']):
            trade_secret = IPAsset(
                id=f'TS-{segment_name.upper()}-001',
                type='trade_secret',
                description=f'{segment_name} proprietary algorithms and software',
                related_segments=[{'name': segment_name, 'attribution_pct': 0.30}],
                royalty_rate=self.royalty_rates.get('software', 0.08),
                valuation_method='relief_from_royalty'
            )
            trade_secrets.append(trade_secret)

        return trade_secrets

    def suggest_shared_ip(self, segments: List[str]) -> List[IPAsset]:
        """
        Suggest IP assets that are shared across multiple segments

        Args:
            segments: List of segment names

        Returns:
            List of shared IP assets
        """
        shared_assets = []

        # Look for patterns indicating shared technology
        hardware_segments = [s for s in segments if any(x in s.lower() for x in ['phone', 'pad', 'mac', 'watch'])]

        if len(hardware_segments) >= 2:
            # Suggest processor/chip IP
            chip_segments = [{'name': seg, 'attribution_pct': 0.12} for seg in hardware_segments]

            chip_patent = IPAsset(
                id='PAT-CHIP-SHARED-001',
                type='patent',
                description='Proprietary processor/chip architecture',
                related_segments=chip_segments,
                royalty_rate=0.05,
                innovation_score=0.92,
                commercial_score=0.88,
                legal_strength_score=0.90,
                remaining_life_years=12,
                valuation_method='technology_factor'
            )
            shared_assets.append(chip_patent)

            # Operating system
            os_segments = [{'name': seg, 'attribution_pct': 0.10} for seg in hardware_segments]

            os_asset = IPAsset(
                id='TS-OS-SHARED-001',
                type='trade_secret',
                description='Operating system and software platform',
                related_segments=os_segments,
                royalty_rate=0.08,
                valuation_method='relief_from_royalty'
            )
            shared_assets.append(os_asset)

        return shared_assets

    def get_industry_insights(self, ticker: str, segments: List[str]) -> Dict:
        """
        Provide industry-specific insights and recommendations

        Args:
            ticker: Stock ticker
            segments: List of segments

        Returns:
            Dictionary with insights
        """
        insights = {
            'primary_ip_types': [],
            'key_focus_areas': [],
            'competitive_considerations': [],
            'valuation_approach': ''
        }

        # Analyze segment mix
        has_hardware = any(x in ' '.join(segments).lower() for x in ['phone', 'computer', 'device', 'watch'])
        has_services = any(x in ' '.join(segments).lower() for x in ['service', 'cloud', 'subscription'])
        has_software = any(x in ' '.join(segments).lower() for x in ['software', 'platform', 'app'])

        if has_hardware:
            insights['primary_ip_types'].extend(['Patents', 'Design Rights', 'Trademarks'])
            insights['key_focus_areas'].append('Hardware innovation and industrial design')
            insights['competitive_considerations'].append('Patent portfolio strength vs. competitors')

        if has_services:
            insights['primary_ip_types'].extend(['Trade Secrets', 'Copyrights'])
            insights['key_focus_areas'].append('Platform ecosystem and network effects')
            insights['competitive_considerations'].append('Customer lock-in and switching costs')

        if has_software:
            insights['primary_ip_types'].extend(['Copyrights', 'Trade Secrets'])
            insights['key_focus_areas'].append('Algorithm efficiency and user experience')

        # Recommend valuation approach
        if has_hardware and has_services:
            insights['valuation_approach'] = 'Hybrid: Technology Factor for patents, Relief from Royalty for brand/platform'
        elif has_hardware:
            insights['valuation_approach'] = 'Technology-focused: Emphasize patent quality and innovation'
        elif has_services:
            insights['valuation_approach'] = 'Platform-focused: Value network effects and recurring revenue'
        else:
            insights['valuation_approach'] = 'Standard Relief from Royalty method'

        return insights

    def estimate_attribution(self, segment_name: str, ip_type: str, company_context: Dict = None) -> float:
        """
        Estimate attribution percentage for an IP asset

        Args:
            segment_name: Name of the segment
            ip_type: Type of IP (patent, trademark, etc.)
            company_context: Additional company information

        Returns:
            Estimated attribution percentage
        """
        segment_lower = segment_name.lower()

        # Attribution estimates based on IP type and segment
        if ip_type == 'trademark':
            if 'iphone' in segment_lower:
                return 0.25  # Strong brand premium
            elif any(x in segment_lower for x in ['ipad', 'mac']):
                return 0.20
            else:
                return 0.15

        elif ip_type == 'patent':
            if 'chip' in segment_lower or 'processor' in segment_lower:
                return 0.15  # Core technology
            else:
                return 0.10  # One of many features

        elif ip_type == 'trade_secret':
            if 'service' in segment_lower or 'cloud' in segment_lower:
                return 0.30  # Critical for services
            else:
                return 0.15

        elif ip_type == 'copyright':
            return 0.20  # Software/content

        else:
            return 0.10  # Conservative default

    def suggest_royalty_rate(self, ip_type: str, industry: str = None) -> float:
        """
        Suggest appropriate royalty rate

        Args:
            ip_type: Type of IP
            industry: Industry context

        Returns:
            Suggested royalty rate
        """
        # Base rates by IP type
        base_rates = {
            'patent': 0.05,
            'trademark': 0.06,
            'copyright': 0.08,
            'trade_secret': 0.08,
            'design': 0.03
        }

        base_rate = base_rates.get(ip_type, 0.05)

        # Adjust for industry
        if industry:
            industry_lower = industry.lower()
            if 'pharma' in industry_lower or 'biotech' in industry_lower:
                base_rate *= 2.0  # Pharma has higher rates
            elif 'software' in industry_lower:
                base_rate *= 1.3
            elif 'consumer' in industry_lower:
                base_rate *= 1.2

        return base_rate
