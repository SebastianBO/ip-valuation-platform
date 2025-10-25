# IP Valuation with Financial Segmentation

A comprehensive framework for valuing intellectual property assets using segmented financial data from publicly traded companies.

## Overview

This framework combines traditional IP valuation methodologies (Relief from Royalty, Multi-Period Excess Earnings, Technology Factor) with granular financial segment data from the Financial Datasets API. By mapping IP assets to specific revenue segments, we achieve more accurate and defensible valuations.

## Key Innovation

**Traditional Problem:** IP valuations often use company-wide metrics that don't reflect the specific economic contribution of individual IP assets.

**Our Solution:** Map IP assets to specific business segments (product lines, geographies) and use segment-level financial data for precise valuations.

### Example

Instead of valuing a Face ID patent against Apple's entire $394B revenue:
- Identify relevant segments: iPhone ($200B), iPad ($30B)
- Apply attribution: 15% of iPhone value, 10% of iPad value
- Result: More realistic $1.3B valuation vs. unrealistic $12B

## Features

- **Multiple Valuation Methods:**
  - Relief from Royalty (RfR)
  - Multi-Period Excess Earnings Method (MPEEM)
  - Technology Factor Method
  - Incremental Income Method

- **Segment-Level Analysis:**
  - Product/service segments
  - Geographic segments
  - Business unit segments

- **Automated Data Integration:**
  - Direct API integration with Financial Datasets
  - Automatic revenue allocation
  - Gross profit margin calculation
  - R&D expense attribution

- **Portfolio Valuation:**
  - Value multiple IP assets simultaneously
  - Cross-segment IP analysis
  - Portfolio-level reporting

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Basic IP Valuation

```python
from ip_valuation_engine import IPValuationEngine, IPAsset

# Initialize engine
engine = IPValuationEngine(api_key="your_api_key_here")

# Define IP asset
my_patent = IPAsset(
    id='PAT-001',
    type='patent',
    description='Face ID technology',
    related_segments=[
        {'name': 'iPhone', 'attribution_pct': 0.15}
    ],
    royalty_rate=0.045
)

# Value the asset
result = engine.value_ip_asset(
    ticker='AAPL',
    ip_asset=my_patent,
    wacc=0.095,
    tax_rate=0.21
)

print(f"IP Value: ${result['total_value']:,.0f}")
```

### 2. Portfolio Valuation

```python
# Define multiple IP assets
portfolio = [
    IPAsset(id='PAT-001', ...),
    IPAsset(id='TM-001', ...),
    IPAsset(id='TS-001', ...)
]

# Value entire portfolio
portfolio_value = engine.value_ip_portfolio(
    ticker='AAPL',
    ip_portfolio=portfolio
)

print(f"Total Portfolio: ${portfolio_value['total_portfolio_value']:,.0f}")
```

### 3. Run Examples

```bash
python examples.py
```

## File Structure

```
ipsegmentation/
├── README.md                      # This file
├── IP_VALUATION_FRAMEWORK.md      # Detailed methodology documentation
├── ip_valuation_engine.py         # Core valuation engine
├── examples.py                    # Usage examples
├── requirements.txt               # Python dependencies
└── ip_valuation_results.json     # Output from valuations
```

## API Configuration

You need a Financial Datasets API key. Get one at: https://www.financialdatasets.ai

Set your API key when initializing the engine:

```python
engine = IPValuationEngine(api_key="your_api_key_here")
```

## Valuation Methods Explained

### Relief from Royalty (RfR)

Values IP based on hypothetical royalty payments saved by owning vs. licensing the asset.

**Best for:** Patents, trademarks, licensed technologies

**Formula:**
```
Value = PV(Revenue × Royalty_Rate × (1 - Tax_Rate))
```

### Multi-Period Excess Earnings (MPEEM)

Isolates cash flows attributable to the IP after deducting returns on other assets.

**Best for:** Trade secrets, customer relationships, proprietary processes

**Formula:**
```
Value = PV(Operating_Income - Contributory_Asset_Charges) × IP_Attribution
```

### Technology Factor Method

Adjusts royalty rate based on patent quality factors (innovation, commercial success, legal strength).

**Best for:** Patents with varying quality/strength characteristics

**Formula:**
```
Adjusted_Royalty = Base_Royalty × (1 + Technology_Factor)
Technology_Factor = f(Innovation, Commercial, Legal, Remaining_Life)
```

## Segment Attribution

How to determine what % of segment value comes from your IP:

1. **Direct Attribution (100%):** IP exclusively used in one segment
   - Example: "iPhone" trademark → iPhone segment

2. **Partial Attribution (10-50%):** IP is one of several value drivers
   - Example: Face ID → 15% of iPhone value

3. **Shared Attribution:** IP used across multiple segments
   - Example: A-series chip → iPhone 40%, iPad 30%, Watch 20%

4. **Methods to Estimate:**
   - Conjoint analysis (customer surveys)
   - Expert judgment (product managers)
   - Comparable transactions
   - Economic modeling

## Use Cases

### 1. M&A Due Diligence
- Value target company's IP portfolio
- Identify key IP assets by segment
- Justify acquisition price allocation

### 2. Licensing Negotiations
- Determine fair royalty rates
- Segment-specific licensing terms
- Geographic licensing strategies

### 3. IP Portfolio Management
- Identify high-value vs. low-value IP
- Prioritize R&D investments
- Decide which patents to maintain/abandon

### 4. Transfer Pricing
- Intercompany IP licensing
- Geographic profit allocation
- Tax-compliant IP valuations

### 5. Financial Reporting
- ASC 350 impairment testing
- Purchase price allocation
- Goodwill vs. identifiable intangibles

### 6. Litigation Support
- Patent infringement damages
- Trademark dilution
- Trade secret misappropriation

## Advanced Features

### Sensitivity Analysis

Test how value changes with different assumptions:

```python
# Test different royalty rates
for rate in [0.03, 0.05, 0.07]:
    my_patent.royalty_rate = rate
    result = engine.value_ip_asset(ticker='AAPL', ip_asset=my_patent)
    print(f"Rate {rate:.0%}: ${result['total_value']:,.0f}")
```

### Geographic Segmentation

Value IP differently by region:

```python
china_patent = IPAsset(
    id='PAT-CN-001',
    description='China-specific patent',
    related_segments=[
        {'name': 'Greater China', 'attribution_pct': 0.25}
    ],
    royalty_rate=0.04
)
```

### Time-Series Analysis

Track IP value over time as segments grow/decline:

```python
# Get 10 years of data instead of 5
segment_data = engine.prepare_segment_financials(
    ticker='AAPL',
    segment_name='iPhone',
    years=10
)
```

## Best Practices

1. **Use Multiple Methods**
   - Cross-validate with 2-3 different approaches
   - Average results or use range

2. **Document Assumptions**
   - Royalty rate sources
   - Attribution rationale
   - Discount rate calculations

3. **Segment Consistency**
   - Ensure segment definitions are consistent across periods
   - Handle segment reclassifications

4. **Validation**
   - Compare to market transactions
   - Industry benchmarks
   - Third-party valuations

5. **Update Regularly**
   - Refresh with quarterly/annual data
   - Monitor segment performance
   - Adjust attribution as products evolve

## Limitations & Considerations

1. **Data Availability**
   - Not all companies report detailed segments
   - Segment profitability rarely disclosed
   - Must use proxies/estimates

2. **Attribution Subjectivity**
   - Difficult to precisely quantify IP contribution
   - Requires expert judgment
   - Should be validated with market research

3. **Method Selection**
   - Different methods yield different results
   - Industry norms matter
   - Purpose of valuation affects choice

4. **Market Conditions**
   - Valuations reflect current market conditions
   - Technology obsolescence risk
   - Competitive landscape changes

## Support & Resources

- **Framework Documentation:** See `IP_VALUATION_FRAMEWORK.md`
- **API Documentation:** https://docs.financialdatasets.ai
- **Examples:** Run `python examples.py`

## License

This framework is provided for reference and educational purposes.

## Contributing

To improve this framework:
1. Test with additional industries
2. Validate against real transactions
3. Refine attribution methodologies
4. Add new valuation methods

## Contact

For questions or collaboration opportunities, please reach out through GitHub issues.
