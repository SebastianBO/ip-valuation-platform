"""
IP Valuation GUI Application
Streamlit-based interface for automatic IP discovery and valuation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from ip_valuation_engine import IPValuationEngine, FinancialDatasetsClient
from ip_discovery import IPAssetDiscovery
from auto_assumptions import AssumptionCalculator, format_assumption_summary
from enhanced_analysis import EnhancedFinancialAnalysis

# Page configuration
st.set_page_config(
    page_title="IP Valuation Platform",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'valuation_results' not in st.session_state:
    st.session_state.valuation_results = None
if 'discovered_assets' not in st.session_state:
    st.session_state.discovered_assets = []
if 'segments' not in st.session_state:
    st.session_state.segments = []

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    # Try to get API key from secrets (for production)
    try:
        default_key = st.secrets.get("FINANCIAL_DATASETS_API_KEY", "")
    except:
        default_key = ""

    # Show input field (will be empty if no secret set)
    api_key = st.text_input(
        "Financial Datasets API Key",
        value=default_key,
        type="password",
        help="Get your API key from financialdatasets.ai"
    )

    if not api_key:
        st.warning("⚠️ Please enter your Financial Datasets API key to continue")
        st.info("Get your API key at: https://www.financialdatasets.ai")
        st.stop()

    st.markdown("---")
    st.markdown("### 🎯 Valuation Assumptions")

    use_auto_calc = st.checkbox("🤖 Auto-Calculate Assumptions", value=True,
                                help="Automatically calculate WACC, Tax Rate, and Terminal Growth from company data")

    if use_auto_calc:
        st.info("💡 Assumptions will be calculated automatically from financial data")
        wacc = None
        tax_rate = None
        terminal_growth = None
    else:
        wacc = st.slider("WACC (Discount Rate)", 0.05, 0.20, 0.095, 0.005,
                         help="Weighted Average Cost of Capital")
        tax_rate = st.slider("Corporate Tax Rate", 0.10, 0.35, 0.21, 0.01)
        terminal_growth = st.slider("Terminal Growth Rate", 0.01, 0.05, 0.025, 0.005,
                                    help="Long-term growth rate for perpetuity value")

    st.markdown("---")
    st.markdown("### 📊 Display Options")

    show_yearly_details = st.checkbox("Show Yearly Cash Flows", value=False)
    show_assumptions = st.checkbox("Show All Assumptions", value=True)
    show_segment_data = st.checkbox("Show Segment Financial Data", value=False)

# Main content
st.markdown('<p class="main-header">💎 IP Valuation Platform</p>', unsafe_allow_html=True)
st.markdown("**Automated IP discovery and valuation using segment-level financial data**")

# Company search section
col1, col2 = st.columns([2, 1])

with col1:
    ticker = st.text_input(
        "🔍 Enter Company Ticker Symbol",
        value="AAPL",
        placeholder="e.g., AAPL, MSFT, GOOGL",
        help="Enter the stock ticker symbol of the company you want to analyze"
    ).upper()

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_button = st.button("🚀 Analyze Company", type="primary", use_container_width=True)

# Analysis workflow
if analyze_button and ticker:
    with st.spinner(f"🔍 Discovering IP assets for {ticker}..."):
        try:
            # Initialize engines
            engine = IPValuationEngine(api_key=api_key)
            discovery = IPAssetDiscovery()
            assumption_calc = AssumptionCalculator(api_key=api_key)
            enhanced_analysis = EnhancedFinancialAnalysis(api_key=api_key)

            # Check if we're using demo mode
            from demo_data import is_demo_mode_available, get_available_demo_tickers
            if is_demo_mode_available(ticker):
                st.info(f"ℹ️ **Demo Mode:** Using cached data for {ticker}. For live data, please add credits to your API account.")
                available_demos = get_available_demo_tickers()
                st.caption(f"Demo data available for: {', '.join(available_demos)}")

            # Step 1: Fetch segment data
            st.markdown("---")
            st.markdown('<p class="sub-header">📈 Step 1: Discovering Business Segments</p>', unsafe_allow_html=True)

            seg_data = engine.client.get_segmented_revenues(ticker, limit=1)

            if not seg_data or 'segmented_revenues' not in seg_data:
                st.error(f"❌ Could not fetch segment data for {ticker}. Please check the ticker symbol.")
                st.stop()

            # Extract segments
            segments = set()
            for period in seg_data['segmented_revenues']:
                for item in period.get('items', []):
                    for seg_info in item.get('segments', []):
                        label = seg_info.get('label', '')
                        if label and label not in ['Product', 'Service']:  # Skip generic categories
                            segments.add(label)

            segments = sorted(list(segments))
            st.session_state.segments = segments

            if segments:
                st.success(f"✅ Found {len(segments)} business segments")

                # Display segments in a nice grid
                cols = st.columns(min(4, len(segments)))
                for idx, segment in enumerate(segments):
                    with cols[idx % len(cols)]:
                        st.markdown(f"**{segment}**")
            else:
                st.warning("⚠️ No specific product segments found. Using company-wide analysis.")
                st.stop()

            # Step 2: Auto-discover IP assets
            st.markdown('<p class="sub-header">🔍 Step 2: Discovering IP Assets</p>', unsafe_allow_html=True)

            discovered_assets = discovery.discover_ip_assets(ticker, segments)
            shared_assets = discovery.suggest_shared_ip(segments)
            all_assets = discovered_assets + shared_assets

            st.session_state.discovered_assets = all_assets

            st.success(f"✅ Discovered {len(all_assets)} potential IP assets")

            # Display discovered assets
            asset_df = pd.DataFrame([
                {
                    'ID': asset.id,
                    'Type': asset.type.title(),
                    'Description': asset.description,
                    'Segments': ', '.join([s['name'] for s in asset.related_segments]),
                    'Method': asset.valuation_method.replace('_', ' ').title()
                }
                for asset in all_assets
            ])

            st.dataframe(asset_df, use_container_width=True, hide_index=True)

            # Step 3: Auto-calculate assumptions (if enabled)
            if use_auto_calc:
                st.markdown('<p class="sub-header">🤖 Step 3: Auto-Calculating Valuation Assumptions</p>', unsafe_allow_html=True)

                try:
                    assumptions = assumption_calc.calculate_all_assumptions(ticker)

                    wacc = assumptions['wacc']
                    tax_rate = assumptions['tax_rate']
                    terminal_growth = assumptions['terminal_growth']

                    # Display calculated assumptions
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("WACC (Calculated)", f"{wacc:.1%}",
                                 help=assumptions['details']['wacc_details'].get('note', ''))

                    with col2:
                        st.metric("Tax Rate (Calculated)", f"{tax_rate:.1%}",
                                 help=assumptions['details']['tax_details'].get('note', ''))

                    with col3:
                        st.metric("Terminal Growth (Calculated)", f"{terminal_growth:.1%}",
                                 help=assumptions['details']['growth_details'].get('note', ''))

                    # Show detailed breakdown in expander
                    with st.expander("📊 View Calculation Details"):
                        st.markdown("### WACC Components")
                        wacc_comp = assumptions['details']['wacc_details'].get('components', {})
                        if wacc_comp:
                            comp_df = pd.DataFrame([
                                {'Component': 'Cost of Equity', 'Value': f"{wacc_comp.get('cost_of_equity', 0):.2%}"},
                                {'Component': 'Cost of Debt', 'Value': f"{wacc_comp.get('cost_of_debt', 0):.2%}"},
                                {'Component': 'Equity Weight', 'Value': f"{wacc_comp.get('equity_weight', 0):.2%}"},
                                {'Component': 'Debt Weight', 'Value': f"{wacc_comp.get('debt_weight', 0):.2%}"},
                                {'Component': 'Market Cap', 'Value': f"${wacc_comp.get('market_cap', 0)/1e9:.2f}B"},
                                {'Component': 'Total Debt', 'Value': f"${wacc_comp.get('total_debt', 0)/1e9:.2f}B"}
                            ])
                            st.dataframe(comp_df, use_container_width=True, hide_index=True)

                        st.markdown("### Tax Rate History")
                        tax_history = assumptions['details']['tax_details'].get('yearly_rates', [])
                        if tax_history:
                            st.write(f"Yearly rates: {', '.join([f'{r:.1%}' for r in tax_history])}")

                        st.markdown("### Growth Rate Analysis")
                        growth_hist = assumptions['details']['growth_details'].get('yearly_growth_rates', [])
                        if growth_hist:
                            st.write(f"Historical growth rates: {', '.join([f'{r:.1%}' for r in growth_hist])}")
                            st.write(f"Average: {assumptions['details']['growth_details'].get('historical_avg_growth', 0):.1%}")
                            st.write(f"Terminal (capped): {terminal_growth:.1%}")

                    st.success("✅ Assumptions calculated from company financials")

                except Exception as e:
                    st.warning(f"⚠️ Could not auto-calculate assumptions: {str(e)}. Using defaults.")
                    wacc = 0.095
                    tax_rate = 0.21
                    terminal_growth = 0.025

            # Step 4: Enhanced financial analysis
            st.markdown('<p class="sub-header">📊 Step 4: Financial Health Analysis</p>', unsafe_allow_html=True)

            try:
                financial_analysis = enhanced_analysis.get_comprehensive_analysis(ticker)

                # Display key metrics
                col1, col2, col3, col4 = st.columns(4)

                prof_metrics = financial_analysis.get('profitability_metrics', {})
                health_metrics = financial_analysis.get('financial_health', {})
                rd_metrics = financial_analysis.get('rd_analysis', {})
                market_metrics = financial_analysis.get('market_position', {})

                with col1:
                    st.metric("Gross Margin", f"{prof_metrics.get('gross_margin', 0):.1%}",
                             help="Product/service profitability")

                with col2:
                    st.metric("Operating Margin", f"{prof_metrics.get('operating_margin', 0):.1%}",
                             help="Operational efficiency")

                with col3:
                    st.metric("R&D Intensity", f"{rd_metrics.get('rd_intensity', 0):.1%}",
                             help="R&D spend as % of revenue")

                with col4:
                    st.metric("Current Ratio", f"{health_metrics.get('current_ratio', 0):.2f}",
                             help="Short-term liquidity")

                # Show insights
                col1, col2 = st.columns(2)

                with col1:
                    st.info(f"**Profitability:** {prof_metrics.get('ip_insight', 'N/A')}")
                    st.info(f"**R&D Potential:** {rd_metrics.get('ip_generation_potential', 'N/A')}")

                with col2:
                    st.info(f"**Financial Health:** {health_metrics.get('assessment', 'N/A')}")
                    st.info(f"**Market Position:** {market_metrics.get('market_insight', 'N/A')}")

            except Exception as e:
                st.warning(f"⚠️ Enhanced analysis not available: {str(e)}")

            # Step 5: Get industry insights
            st.markdown('<p class="sub-header">💡 Step 5: Industry Analysis</p>', unsafe_allow_html=True)

            insights = discovery.get_industry_insights(ticker, segments)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Primary IP Types:**")
                for ip_type in insights['primary_ip_types']:
                    st.markdown(f"- {ip_type}")

                st.markdown("**Key Focus Areas:**")
                for area in insights['key_focus_areas']:
                    st.markdown(f"- {area}")

            with col2:
                st.markdown("**Competitive Considerations:**")
                for consideration in insights['competitive_considerations']:
                    st.markdown(f"- {consideration}")

                st.markdown("**Recommended Valuation Approach:**")
                st.info(insights['valuation_approach'])

            # Step 6: Run valuations
            st.markdown('<p class="sub-header">💰 Step 6: Valuing IP Portfolio</p>', unsafe_allow_html=True)

            progress_bar = st.progress(0)
            status_text = st.empty()

            results = engine.value_ip_portfolio(
                ticker=ticker,
                ip_portfolio=all_assets,
                wacc=wacc,
                tax_rate=tax_rate,
                terminal_growth=terminal_growth
            )

            progress_bar.progress(100)
            status_text.success("✅ Valuation complete!")

            st.session_state.valuation_results = results

        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
            import traceback
            with st.expander("View Error Details"):
                st.code(traceback.format_exc())
            st.stop()

# Display results if available
if st.session_state.valuation_results:
    results = st.session_state.valuation_results

    st.markdown("---")
    st.markdown('<p class="sub-header">📊 Valuation Results</p>', unsafe_allow_html=True)

    # Portfolio summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Portfolio Value",
            f"${results['total_portfolio_value']/1e9:.2f}B",
            help="Combined value of all IP assets"
        )

    with col2:
        st.metric(
            "Number of Assets",
            results['asset_count'],
            help="Total IP assets valued"
        )

    with col3:
        avg_value = results['total_portfolio_value'] / results['asset_count'] if results['asset_count'] > 0 else 0
        st.metric(
            "Average Asset Value",
            f"${avg_value/1e9:.2f}B",
            help="Average value per IP asset"
        )

    with col4:
        st.metric(
            "WACC Used",
            f"{results['assumptions']['wacc']:.1%}",
            help="Weighted Average Cost of Capital (discount rate)"
        )

    # Portfolio breakdown chart
    st.markdown("### 📊 Portfolio Breakdown")

    # Prepare data for visualization
    asset_values = []
    for asset in results['asset_valuations']:
        asset_values.append({
            'Asset': asset['description'],
            'Type': asset['ip_type'].title(),
            'Value': asset['total_value'],
            'Value_B': asset['total_value'] / 1e9
        })

    df_assets = pd.DataFrame(asset_values)

    # Create pie chart
    fig_pie = px.pie(
        df_assets,
        values='Value',
        names='Asset',
        title='IP Portfolio Value Distribution',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

    # Bar chart by type
    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(
            df_assets.sort_values('Value', ascending=False),
            x='Asset',
            y='Value_B',
            title='IP Asset Values',
            labels={'Value_B': 'Value (Billions USD)', 'Asset': ''},
            color='Type',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_bar.update_layout(showlegend=True, xaxis_tickangle=-45)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Group by type
        type_summary = df_assets.groupby('Type')['Value_B'].sum().reset_index()
        fig_type = px.bar(
            type_summary,
            x='Type',
            y='Value_B',
            title='Value by IP Type',
            labels={'Value_B': 'Value (Billions USD)', 'Type': 'IP Type'},
            color='Type',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_type, use_container_width=True)

    # Detailed asset breakdown
    st.markdown("### 🔍 Detailed Asset Analysis")

    for asset in results['asset_valuations']:
        with st.expander(f"💎 {asset['description']} - ${asset['total_value']/1e9:.2f}B"):
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"**ID:** {asset['ip_asset_id']}")
                st.markdown(f"**Type:** {asset['ip_type'].title()}")
                st.markdown(f"**Total Value:** ${asset['total_value']/1e9:.2f}B")

            with col2:
                st.markdown(f"**Ticker:** {asset['ticker']}")
                st.markdown(f"**Segments:** {len(asset['segment_valuations'])}")

            with col3:
                st.markdown(f"**Valuation Date:** {asset['valuation_date']}")

            # Segment breakdown
            if len(asset['segment_valuations']) > 1:
                st.markdown("**Segment Breakdown:**")

                seg_df = pd.DataFrame([
                    {
                        'Segment': seg['segment'],
                        'Value ($B)': seg['total_value'] / 1e9,
                        'Attribution': f"{seg['segment_attribution']:.0%}",
                        'Method': seg['method']
                    }
                    for seg in asset['segment_valuations']
                ])

                st.dataframe(seg_df, use_container_width=True, hide_index=True)

                # Segment pie chart
                fig_seg = px.pie(
                    seg_df,
                    values='Value ($B)',
                    names='Segment',
                    title=f'{asset["description"]} - Value by Segment'
                )
                st.plotly_chart(fig_seg, use_container_width=True)

            # Show assumptions
            if show_assumptions and asset['segment_valuations']:
                st.markdown("**Valuation Assumptions:**")
                assumptions = asset['segment_valuations'][0].get('assumptions', {})

                assumption_df = pd.DataFrame([
                    {'Parameter': k.replace('_', ' ').title(), 'Value': v}
                    for k, v in assumptions.items()
                ])
                st.dataframe(assumption_df, use_container_width=True, hide_index=True)

            # Show yearly details
            if show_yearly_details and asset['segment_valuations']:
                for seg_val in asset['segment_valuations']:
                    if 'yearly_details' in seg_val:
                        st.markdown(f"**Yearly Cash Flows - {seg_val['segment']}:**")

                        yearly_df = pd.DataFrame(seg_val['yearly_details'])

                        if 'revenue' in yearly_df.columns:
                            yearly_df['revenue'] = yearly_df['revenue'] / 1e9
                            yearly_df['royalty_savings'] = yearly_df['royalty_savings'] / 1e6
                            yearly_df['present_value'] = yearly_df['present_value'] / 1e6

                        st.dataframe(yearly_df, use_container_width=True, hide_index=True)

            # Show segment financial data
            if show_segment_data and asset['segment_valuations']:
                for seg_val in asset['segment_valuations']:
                    if 'segment_data' in seg_val:
                        st.markdown(f"**Financial Data - {seg_val['segment']}:**")

                        seg_data = seg_val['segment_data']

                        # Create time series chart
                        years = list(range(len(seg_data['revenues'])))

                        fig_fin = go.Figure()

                        fig_fin.add_trace(go.Scatter(
                            x=years,
                            y=[r/1e9 for r in seg_data['revenues']],
                            name='Revenue',
                            mode='lines+markers'
                        ))

                        fig_fin.add_trace(go.Scatter(
                            x=years,
                            y=[gp/1e9 for gp in seg_data['gross_profits']],
                            name='Gross Profit',
                            mode='lines+markers'
                        ))

                        fig_fin.update_layout(
                            title=f'{seg_val["segment"]} Financial Performance',
                            xaxis_title='Year (0=Latest)',
                            yaxis_title='Billions USD',
                            hovermode='x unified'
                        )

                        st.plotly_chart(fig_fin, use_container_width=True)

    # Download results
    st.markdown("---")
    st.markdown("### 💾 Export Results")

    col1, col2 = st.columns(2)

    with col1:
        # JSON download
        json_str = json.dumps(results, indent=2, default=str)
        st.download_button(
            label="📥 Download Full Results (JSON)",
            data=json_str,
            file_name=f"{ticker}_ip_valuation_results.json",
            mime="application/json"
        )

    with col2:
        # CSV summary download
        summary_data = []
        for asset in results['asset_valuations']:
            for seg_val in asset['segment_valuations']:
                summary_data.append({
                    'IP_Asset': asset['description'],
                    'IP_Type': asset['ip_type'],
                    'Segment': seg_val['segment'],
                    'Value_USD': seg_val['total_value'],
                    'Method': seg_val['method'],
                    'Attribution_Pct': seg_val.get('segment_attribution', 0)
                })

        summary_df = pd.DataFrame(summary_data)
        csv = summary_df.to_csv(index=False)

        st.download_button(
            label="📥 Download Summary (CSV)",
            data=csv,
            file_name=f"{ticker}_ip_valuation_summary.csv",
            mime="text/csv"
        )

    # Key insights
    st.markdown("---")
    st.markdown("### 💡 Key Insights")

    # Find most valuable asset
    most_valuable = max(results['asset_valuations'], key=lambda x: x['total_value'])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Most Valuable Asset:**")
        st.info(f"{most_valuable['description']}: ${most_valuable['total_value']/1e9:.2f}B ({most_valuable['total_value']/results['total_portfolio_value']*100:.1f}% of portfolio)")

        # Portfolio concentration
        top_3_value = sum(sorted([a['total_value'] for a in results['asset_valuations']], reverse=True)[:3])
        concentration = top_3_value / results['total_portfolio_value'] * 100

        st.markdown("**Portfolio Concentration:**")
        if concentration > 75:
            st.warning(f"Top 3 assets represent {concentration:.1f}% of value - highly concentrated portfolio")
        else:
            st.success(f"Top 3 assets represent {concentration:.1f}% of value - well-diversified portfolio")

    with col2:
        # Type breakdown
        type_values = {}
        for asset in results['asset_valuations']:
            ip_type = asset['ip_type']
            type_values[ip_type] = type_values.get(ip_type, 0) + asset['total_value']

        st.markdown("**Value by IP Type:**")
        for ip_type, value in sorted(type_values.items(), key=lambda x: x[1], reverse=True):
            pct = value / results['total_portfolio_value'] * 100
            st.markdown(f"- **{ip_type.title()}:** ${value/1e9:.2f}B ({pct:.1f}%)")

else:
    # Welcome screen
    st.markdown("---")
    st.markdown("### 👋 Welcome to the IP Valuation Platform")

    st.markdown("""
    This platform automatically discovers and values intellectual property assets using:

    - **🔍 Automatic IP Discovery:** Identifies patents, trademarks, and trade secrets based on business segments
    - **📊 Segment-Level Analysis:** Uses actual financial data from specific product lines
    - **🎯 Multiple Valuation Methods:** Relief from Royalty, Technology Factor, and more
    - **💡 Industry Insights:** Tailored recommendations based on company characteristics

    #### How to Use:
    1. Enter a company ticker symbol (e.g., AAPL, MSFT, GOOGL)
    2. Click "Analyze Company"
    3. Review discovered IP assets and valuations
    4. Adjust assumptions in the sidebar as needed
    5. Export results for further analysis

    #### Example Companies to Try:
    - **AAPL** - Apple Inc. (consumer electronics, services)
    - **MSFT** - Microsoft (software, cloud services)
    - **GOOGL** - Alphabet (search, advertising, cloud)
    - **TSLA** - Tesla (automotive, energy)
    - **NVDA** - NVIDIA (semiconductors, AI)

    **Get started by entering a ticker symbol above!** 🚀
    """)

    # Show example visualization
    st.markdown("### 📊 Example: Apple IP Portfolio")

    example_data = pd.DataFrame({
        'Asset': ['iPhone Trademark', 'Face ID Patent', 'A-Series Chip'],
        'Value': [23.8, 9.5, 6.4],
        'Type': ['Trademark', 'Patent', 'Patent']
    })

    fig_example = px.bar(
        example_data,
        x='Asset',
        y='Value',
        color='Type',
        title='Example: Apple IP Asset Values (Billions USD)',
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    st.plotly_chart(fig_example, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>IP Valuation Platform</strong> | Powered by Financial Datasets API</p>
    <p>Using EMBA-level IP valuation methodologies with real-time financial data</p>
</div>
""", unsafe_allow_html=True)
