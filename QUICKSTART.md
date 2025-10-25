# Quick Start Guide

Get up and running with IP valuation in 5 minutes.

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Get Your API Key

1. Visit https://www.financialdatasets.ai
2. Sign up for an account
3. Copy your API key

## Step 3: Run Your First Valuation

Create a file called `my_valuation.py`:

```python
from ip_valuation_engine import IPValuationEngine, IPAsset

# Your API key
API_KEY = "0a799aee-ff2b-40a2-903c-f8737226d148"

# Initialize engine
engine = IPValuationEngine(api_key=API_KEY)

# Define the IP asset you want to value
face_id_patent = IPAsset(
    id='PAT-FACEID-001',
    type='patent',
    description='Face ID facial recognition technology',
    related_segments=[
        {'name': 'iPhone', 'attribution_pct': 0.15},  # Face ID = 15% of iPhone value
    ],
    royalty_rate=0.045,  # 4.5% royalty rate for biometric tech
    valuation_method='relief_from_royalty'
)

# Value it!
result = engine.value_ip_asset(
    ticker='AAPL',              # Apple stock ticker
    ip_asset=face_id_patent,
    wacc=0.095,                 # 9.5% discount rate
    tax_rate=0.21               # 21% corporate tax
)

# Print results
print(f"\nIP Asset: {result['description']}")
print(f"Total Value: ${result['total_value']:,.0f}")
print(f"\nSegment Breakdown:")
for seg in result['segment_valuations']:
    print(f"  {seg['segment']}: ${seg['total_value']:,.0f}")
```

Run it:
```bash
python my_valuation.py
```

## Step 4: Understand the Output

```
IP Asset: Face ID facial recognition technology
Total Value: $1,350,000,000

Segment Breakdown:
  iPhone: $1,350,000,000
```

This means the Face ID patent is worth approximately $1.35 billion based on its contribution to iPhone revenue.

## Step 5: Try Different Scenarios

### Scenario A: Value a Trademark

```python
iphone_trademark = IPAsset(
    id='TM-IPHONE-001',
    type='trademark',
    description='iPhone brand and trademark',
    related_segments=[
        {'name': 'iPhone', 'attribution_pct': 0.25}  # Brand = 25% of value
    ],
    royalty_rate=0.06,  # 6% for strong brands
    valuation_method='relief_from_royalty'
)

result = engine.value_ip_asset(ticker='AAPL', ip_asset=iphone_trademark)
print(f"Trademark Value: ${result['total_value']:,.0f}")
```

### Scenario B: Multi-Segment Patent

```python
chip_patent = IPAsset(
    id='PAT-CHIP-001',
    type='patent',
    description='M1 chip architecture',
    related_segments=[
        {'name': 'Mac', 'attribution_pct': 0.20},
        {'name': 'iPad', 'attribution_pct': 0.15}
    ],
    royalty_rate=0.05,
    valuation_method='relief_from_royalty'
)

result = engine.value_ip_asset(ticker='AAPL', ip_asset=chip_patent)
print(f"Chip Patent Total: ${result['total_value']:,.0f}")
for seg in result['segment_valuations']:
    print(f"  {seg['segment']}: ${seg['total_value']:,.0f}")
```

### Scenario C: Entire Portfolio

```python
portfolio = [face_id_patent, iphone_trademark, chip_patent]

portfolio_value = engine.value_ip_portfolio(
    ticker='AAPL',
    ip_portfolio=portfolio
)

print(f"\nTotal Portfolio Value: ${portfolio_value['total_portfolio_value']:,.0f}")
```

## Common Questions

### Q: How do I know what royalty rate to use?

**A:** Research comparable licenses in your industry:
- Patents: 1-5% for utility patents, 3-10% for key technology
- Trademarks: 0.5-3% for standard brands, 5-10% for premium brands
- Software: 5-15% depending on criticality
- Pharma: 8-15% for blockbuster drugs

Sources: RoyaltyRange.com, ktMINE, comparable transactions

### Q: How do I determine attribution percentage?

**A:** Several approaches:
1. **Customer surveys** - Ask customers to rank importance of features
2. **Expert judgment** - Consult with product managers
3. **Competitive analysis** - Compare to products without the IP
4. **Financial analysis** - Estimate incremental revenue from IP

Start conservative (10-15%) unless you have strong evidence for higher attribution.

### Q: Which valuation method should I use?

**A:**
- **Relief from Royalty**: Best for patents and trademarks with comparable licenses
- **Excess Earnings**: Best for trade secrets and unique processes
- **Technology Factor**: Best for patents where quality varies significantly

When in doubt, use Relief from Royalty - it's the most widely accepted.

### Q: What if my company isn't public?

**A:** Use a comparable public company:
1. Find similar company in same industry
2. Use their segment data as proxy
3. Adjust for size/profitability differences
4. Document your comparability assumptions

### Q: How accurate is this?

**A:** Accuracy depends on:
- Quality of segment data (better for large-cap tech/pharma)
- Accuracy of attribution (requires good market research)
- Appropriateness of royalty rate (use industry data)

Expect +/- 30% variance. Use ranges, not point estimates.

### Q: Can I use this for tax/legal purposes?

**A:** These valuations can serve as a starting point, but:
- Tax valuations require IRS-compliant methodology
- Litigation requires Daubert-standard expert reports
- Financial reporting requires GAAP/IFRS compliance

Always consult with qualified valuation professionals for official purposes.

## Next Steps

1. **Read the full framework:** `IP_VALUATION_FRAMEWORK.md`
2. **Explore examples:** `python examples.py`
3. **Customize for your needs:** Modify `ip_valuation_engine.py`
4. **Validate your results:** Compare to market transactions

## Troubleshooting

**Error: "Unable to fetch data for AAPL"**
- Check your API key is correct
- Verify you have internet connection
- Ensure ticker symbol is valid

**Error: "No segment found: iPhone"**
- Segment names are case-sensitive
- Check what segments are available:
  ```python
  data = engine.client.get_segmented_revenues('AAPL')
  print(data)
  ```

**Values seem too high/low**
- Check your attribution percentage (most common issue)
- Verify royalty rate is appropriate for industry
- Ensure WACC is reasonable (8-12% for most companies)

## Example Output

Running the main example script:

```bash
python ip_valuation_engine.py
```

Should produce output like:

```
================================================================================
IP PORTFOLIO VALUATION: AAPL
================================================================================

Total Portfolio Value: $15,234,567,890
Number of Assets Valued: 3

Assumptions:
  - WACC: 9.5%
  - Tax Rate: 21.0%
  - Terminal Growth: 2.5%

================================================================================
INDIVIDUAL ASSET VALUATIONS
================================================================================

Face ID facial recognition technology
  ID: PAT-FACEID-001
  Type: patent
  Total Value: $1,350,000,000
  Segments:
    - iPhone: $1,215,000,000
      Method: Relief from Royalty
      Attribution: 12%
    - iPad: $135,000,000
      Method: Relief from Royalty
      Attribution: 8%

[... more assets ...]
```

## Tips for Better Valuations

1. **Use latest financial data** - Refresh data quarterly
2. **Multiple methods** - Cross-validate with 2-3 approaches
3. **Sensitivity analysis** - Test key assumptions
4. **Document everything** - Keep detailed notes on assumptions
5. **Peer review** - Have others challenge your attribution %
6. **Update regularly** - IP value changes as business evolves

## Ready to Go!

You now have everything you need to start valuing IP assets using financial segmentation.

Happy valuing!
