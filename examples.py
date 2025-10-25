"""
Example IP Valuation Scenarios
Demonstrates different use cases and industries
"""

from ip_valuation_engine import IPValuationEngine, IPAsset


def example_tech_company():
    """
    Example: Valuing patents and trademarks for a technology company (Apple)
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Technology Company (Apple)")
    print("=" * 80)

    engine = IPValuationEngine(api_key="0a799aee-ff2b-40a2-903c-f8737226d148")

    # Apple's Face ID patent
    faceid_patent = IPAsset(
        id='PAT-FACEID-001',
        type='patent',
        description='Face ID biometric authentication system',
        related_segments=[
            {'name': 'iPhone', 'attribution_pct': 0.15},  # 15% of iPhone value from Face ID
            {'name': 'iPad', 'attribution_pct': 0.10}     # 10% of iPad value
        ],
        royalty_rate=0.045,  # 4.5% royalty for biometric tech
        innovation_score=0.88,
        commercial_score=0.92,
        legal_strength_score=0.85,
        remaining_life_years=10,
        valuation_method='technology_factor'
    )

    result = engine.value_ip_asset(
        ticker='AAPL',
        ip_asset=faceid_patent,
        wacc=0.095,
        tax_rate=0.21
    )

    print(f"\nIP Asset: {result['description']}")
    print(f"Total Value: ${result['total_value']:,.0f}")
    for seg_val in result['segment_valuations']:
        print(f"  {seg_val['segment']}: ${seg_val['total_value']:,.0f}")


def example_pharma_company():
    """
    Example: Valuing a blockbuster drug patent for pharmaceutical company
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Pharmaceutical Company")
    print("=" * 80)

    engine = IPValuationEngine(api_key="0a799aee-ff2b-40a2-903c-f8737226d148")

    # Hypothetical oncology drug patent
    drug_patent = IPAsset(
        id='PAT-ONCO-001',
        type='patent',
        description='Novel oncology drug compound',
        related_segments=[
            {'name': 'Oncology', 'attribution_pct': 0.80}  # Drug drives 80% of oncology segment
        ],
        royalty_rate=0.12,  # Higher royalty for pharma
        innovation_score=0.95,
        commercial_score=0.90,
        legal_strength_score=0.92,
        remaining_life_years=8,
        valuation_method='technology_factor'
    )

    # Note: This would need the actual ticker symbol
    print("\nDrug Patent Example:")
    print(f"  Description: {drug_patent.description}")
    print(f"  Royalty Rate: {drug_patent.royalty_rate:.1%}")
    print(f"  Remaining Life: {drug_patent.remaining_life_years} years")
    print(f"  Innovation Score: {drug_patent.innovation_score:.0%}")
    print("\n  This patent would be valued against the Oncology segment revenues")
    print("  using the technology factor method to account for high innovation")


def example_consumer_brand():
    """
    Example: Valuing a consumer brand trademark
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Consumer Brand Valuation")
    print("=" * 80)

    engine = IPValuationEngine(api_key="0a799aee-ff2b-40a2-903c-f8737226d148")

    # Nike Air Jordan trademark
    jordan_brand = IPAsset(
        id='TM-JORDAN-001',
        type='trademark',
        description='Air Jordan brand and trademark',
        related_segments=[
            {'name': 'Jordan Brand', 'attribution_pct': 0.90}  # Brand is 90% of segment value
        ],
        royalty_rate=0.08,  # Strong consumer brand royalty
        valuation_method='relief_from_royalty'
    )

    print("\nBrand Trademark Example:")
    print(f"  Brand: {jordan_brand.description}")
    print(f"  Royalty Rate: {jordan_brand.royalty_rate:.1%}")
    print(f"  Attribution: {jordan_brand.related_segments[0]['attribution_pct']:.0%}")
    print("\n  This trademark represents the premium consumers pay for the Jordan brand")
    print("  Relief from Royalty method calculates the value of owning vs. licensing")


def example_software_trade_secret():
    """
    Example: Valuing trade secrets and proprietary software
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Software Trade Secret")
    print("=" * 80)

    engine = IPValuationEngine(api_key="0a799aee-ff2b-40a2-903c-f8737226d148")

    # Cloud infrastructure software
    cloud_software = IPAsset(
        id='TS-CLOUD-001',
        type='trade_secret',
        description='Proprietary cloud orchestration algorithms',
        related_segments=[
            {'name': 'Cloud Services', 'attribution_pct': 0.40},
            {'name': 'Enterprise Software', 'attribution_pct': 0.30}
        ],
        royalty_rate=0.10,  # Higher for software/services
        valuation_method='excess_earnings'
    )

    print("\nTrade Secret Example:")
    print(f"  Asset: {cloud_software.description}")
    print(f"  Segments: {len(cloud_software.related_segments)}")
    print(f"  Method: {cloud_software.valuation_method}")
    print("\n  Trade secrets valued using Excess Earnings Method")
    print("  Isolates the cash flow generated specifically by the proprietary algorithms")


def example_multi_segment_patent():
    """
    Example: Patent used across multiple product lines
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Multi-Segment Patent Portfolio")
    print("=" * 80)

    engine = IPValuationEngine(api_key="0a799aee-ff2b-40a2-903c-f8737226d148")

    # Chip architecture used in multiple products
    chip_patent = IPAsset(
        id='PAT-CHIP-M1',
        type='patent',
        description='M1 Chip Architecture',
        related_segments=[
            {'name': 'Mac', 'attribution_pct': 0.25},
            {'name': 'iPad', 'attribution_pct': 0.15},
            {'name': 'iPhone', 'attribution_pct': 0.08}
        ],
        royalty_rate=0.05,
        innovation_score=0.95,
        commercial_score=0.90,
        legal_strength_score=0.88,
        remaining_life_years=15,
        valuation_method='relief_from_royalty'
    )

    result = engine.value_ip_asset(
        ticker='AAPL',
        ip_asset=chip_patent,
        wacc=0.095,
        tax_rate=0.21
    )

    print(f"\nChip Patent: {result['description']}")
    print(f"Total Value (All Segments): ${result['total_value']:,.0f}")
    print("\nBreakdown by Segment:")
    for seg_val in result['segment_valuations']:
        print(f"  {seg_val['segment']}: ${seg_val['total_value']:,.0f} "
              f"({seg_val['segment_attribution']:.0%} attribution)")


def example_geographic_segmentation():
    """
    Example: Valuing IP with geographic segment analysis
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Geographic IP Valuation")
    print("=" * 80)

    # Conceptual example - would need geographic revenue segments
    print("\nGeographic Segmentation Concept:")
    print("\n  When IP has different values in different regions:")
    print("    - Patents: May only be protected in certain countries")
    print("    - Trademarks: Brand strength varies by market")
    print("    - Trade Secrets: Enforcement differs by jurisdiction")
    print("\n  Example: iPhone trademark")
    print("    Americas: Full protection, 95% attribution")
    print("    Europe: Full protection, 90% attribution")
    print("    China: Complex landscape, 60% attribution")
    print("\n  Use Financial Datasets API geographic segments:")
    print("    GET /financials/segmented-revenues/tickers/AAPL")
    print("    Filter by geographic segment labels")


def example_portfolio_analysis():
    """
    Example: Complete IP portfolio valuation with multiple asset types
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Complete IP Portfolio Analysis")
    print("=" * 80)

    engine = IPValuationEngine(api_key="0a799aee-ff2b-40a2-903c-f8737226d148")

    # Build a diversified IP portfolio
    portfolio = [
        # Core technology patent
        IPAsset(
            id='PAT-001',
            type='patent',
            description='Core technology patent',
            related_segments=[{'name': 'iPhone', 'attribution_pct': 0.20}],
            royalty_rate=0.05,
            valuation_method='relief_from_royalty'
        ),
        # Brand trademark
        IPAsset(
            id='TM-001',
            type='trademark',
            description='Product brand trademark',
            related_segments=[{'name': 'iPhone', 'attribution_pct': 0.30}],
            royalty_rate=0.06,
            valuation_method='relief_from_royalty'
        ),
        # Software copyright
        IPAsset(
            id='CR-001',
            type='copyright',
            description='Operating system software',
            related_segments=[
                {'name': 'iPhone', 'attribution_pct': 0.15},
                {'name': 'iPad', 'attribution_pct': 0.15}
            ],
            royalty_rate=0.08,
            valuation_method='excess_earnings'
        )
    ]

    try:
        result = engine.value_ip_portfolio(
            ticker='AAPL',
            ip_portfolio=portfolio,
            wacc=0.095,
            tax_rate=0.21
        )

        print(f"\nTotal Portfolio Value: ${result['total_portfolio_value']:,.0f}")
        print(f"Number of Assets: {result['asset_count']}")
        print("\nPortfolio Breakdown:")

        for asset_val in result['asset_valuations']:
            print(f"\n  {asset_val['description']}")
            print(f"    Type: {asset_val['ip_type']}")
            print(f"    Value: ${asset_val['total_value']:,.0f}")

    except Exception as e:
        print(f"\nError: {e}")
        print("Note: This requires active API access")


def example_sensitivity_analysis():
    """
    Example: Sensitivity analysis for key assumptions
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 8: Sensitivity Analysis")
    print("=" * 80)

    print("\nKey Value Drivers to Test:")
    print("\n1. Royalty Rate Sensitivity")
    print("   Base: 5%  →  Low: 3%  →  High: 7%")
    print("   Impact: ±40% value change")

    print("\n2. Attribution Percentage")
    print("   Base: 20%  →  Low: 15%  →  High: 25%")
    print("   Impact: ±25% value change")

    print("\n3. Discount Rate (WACC)")
    print("   Base: 10%  →  Low: 8%  →  High: 12%")
    print("   Impact: ±15% value change")

    print("\n4. Terminal Growth Rate")
    print("   Base: 2%  →  Low: 1%  →  High: 3%")
    print("   Impact: ±10% value change")

    print("\n5. Revenue Growth")
    print("   Base: Historical  →  Low: -50%  →  High: +50%")
    print("   Impact: Proportional to revenue assumptions")

    print("\nRun multiple scenarios to establish valuation range:")
    print("  - Best Case: Optimistic assumptions → Upper bound")
    print("  - Base Case: Realistic assumptions → Most likely value")
    print("  - Worst Case: Conservative assumptions → Lower bound")


def comparison_of_methods():
    """
    Compare different valuation methods for the same asset
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 9: Comparison of Valuation Methods")
    print("=" * 80)

    print("\nSame IP Asset Valued Using Different Methods:")
    print("\nAsset: Proprietary algorithm patent")
    print("Segment: Cloud Services")
    print("Revenue: $50B annually\n")

    print("Method 1: Relief from Royalty")
    print("  Royalty Rate: 8%")
    print("  Attribution: 30%")
    print("  Estimated Value: ~$1.2B")
    print("  Pros: Simple, market-based, widely accepted")
    print("  Cons: Requires comparable royalty rates")

    print("\nMethod 2: Multi-Period Excess Earnings")
    print("  Operating Margin: 40%")
    print("  IP Contribution: 50% of excess earnings")
    print("  Estimated Value: ~$1.5B")
    print("  Pros: Isolates IP-specific cash flows")
    print("  Cons: Complex, many assumptions")

    print("\nMethod 3: Technology Factor")
    print("  Base Royalty: 6%")
    print("  Tech Factor Adjustment: 1.3x")
    print("  Estimated Value: ~$1.35B")
    print("  Pros: Adjusts for IP quality")
    print("  Cons: Subjective scoring")

    print("\nRecommendation:")
    print("  Use multiple methods and average the results")
    print("  Weight methods based on data availability and industry norms")
    print("  Document all assumptions for defensibility")


def main():
    """Run all examples"""
    print("\n")
    print("*" * 80)
    print("IP VALUATION FRAMEWORK - USAGE EXAMPLES")
    print("*" * 80)

    # Run examples
    example_tech_company()
    example_pharma_company()
    example_consumer_brand()
    example_software_trade_secret()
    example_multi_segment_patent()
    example_geographic_segmentation()
    example_portfolio_analysis()
    example_sensitivity_analysis()
    comparison_of_methods()

    print("\n" + "=" * 80)
    print("For more details, see IP_VALUATION_FRAMEWORK.md")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
