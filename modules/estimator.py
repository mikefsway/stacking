"""
Value Estimator - Calculate potential savings and revenue from energy flexibility
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from typing import Dict, List, Tuple


# ============================================================================
# CALCULATION FUNCTIONS (Pure Python - no external APIs)
# ============================================================================

def calculate_cost_savings(
    capacity_kw: float,
    flex_hours_per_day: float,
    peak_rate_p: float,
    offpeak_rate_p: float,
    participation_rate_low: float,
    participation_rate_high: float
) -> Tuple[float, float]:
    """
    Calculate annual cost savings from time-shifting

    Returns: (savings_low, savings_high) in £
    """
    # Convert p/kWh to £/kWh
    peak_rate = peak_rate_p / 100
    offpeak_rate = offpeak_rate_p / 100

    # Daily kWh shifted
    kwh_per_day = capacity_kw * flex_hours_per_day

    # Daily savings per kWh shifted
    savings_per_kwh = peak_rate - offpeak_rate

    # Annual savings range
    savings_low = kwh_per_day * savings_per_kwh * (participation_rate_low / 100) * 365
    savings_high = kwh_per_day * savings_per_kwh * (participation_rate_high / 100) * 365

    return (max(0, savings_low), max(0, savings_high))


def calculate_incentives(
    capacity_kw: float,
    service_types: List[str],
    availability_hours_low: int,
    availability_hours_high: int,
    participation_rate_low: float,
    participation_rate_high: float
) -> Tuple[float, float]:
    """
    Calculate potential incentive revenue from flexibility services

    Returns: (incentives_low, incentives_high) in £
    """
    # Service rate mapping (£ per kW per hour of availability)
    # These are indicative rates based on recent market data
    service_rates = {
        "Dynamic Containment (DC)": 0.020,  # £20/MW/h = £0.020/kW/h
        "Dynamic Moderation (DM)": 0.015,
        "Dynamic Regulation (DR)": 0.018,
        "Demand Flexibility Service (DFS)": 0.50,  # Per kWh delivered (higher)
        "Peak load reduction (PR)": 0.010,
        "Balancing Reserve (BR)": 0.012,
        "Quick Reserve (QR)": 0.015,
        "Static Firm Frequency Response (SFFR)": 0.010,
    }

    # Calculate weighted average rate based on selected services
    if not service_types:
        return (0, 0)

    applicable_rates = [service_rates.get(s, 0.005) for s in service_types]
    avg_rate = sum(applicable_rates) / len(applicable_rates)

    # Calculate incentive range
    incentives_low = capacity_kw * avg_rate * availability_hours_low * (participation_rate_low / 100)
    incentives_high = capacity_kw * avg_rate * availability_hours_high * (participation_rate_high / 100)

    return (max(0, incentives_low), max(0, incentives_high))


def calculate_co2_savings(
    capacity_kw: float,
    flex_hours_per_day: float,
    peak_emission_factor: float,
    offpeak_emission_factor: float,
    participation_rate_avg: float
) -> float:
    """
    Calculate annual CO2 savings from shifting to lower-carbon periods

    Returns: CO2 savings in kg/year
    """
    # Daily kWh shifted
    kwh_per_day = capacity_kw * flex_hours_per_day

    # Emission reduction per kWh shifted
    emission_reduction = peak_emission_factor - offpeak_emission_factor

    # Annual CO2 savings
    co2_savings = kwh_per_day * emission_reduction * (participation_rate_avg / 100) * 365

    return max(0, co2_savings)


# ============================================================================
# STREAMLIT UI COMPONENTS
# ============================================================================

def render_estimator_tab():
    """Render the complete Value Estimator tab"""

    st.header("Flexibility Value Estimator")

    # Disclaimer at top
    st.warning(
        "⚠️ **Important**: These are estimates based on your inputs and general assumptions, "
        "not advice. Actual outcomes depend on your tariff, operations, and eligibility for "
        "specific programs. Always verify with NESO and your DNO before making commercial decisions."
    )

    # Create tabs within the page
    input_tab, results_tab, assumptions_tab, methodology_tab = st.tabs([
        "📝 Inputs",
        "📊 Results",
        "🔍 Assumptions",
        "📖 Methodology"
    ])

    with input_tab:
        render_estimator_inputs()

    with results_tab:
        render_estimator_results()

    with assumptions_tab:
        render_estimator_assumptions()

    with methodology_tab:
        render_estimator_methodology()


def render_estimator_inputs():
    """Render input form for estimator"""

    st.subheader("Enter Your Details")

    # Use st.form to group inputs and reduce reruns
    with st.form("estimator_form"):

        # Asset details
        st.markdown("#### 1. Asset Details")

        col1, col2 = st.columns(2)

        with col1:
            capacity_kw = st.number_input(
                "Shiftable Capacity (kW)",
                min_value=1.0,
                max_value=10000.0,
                value=100.0,
                step=10.0,
                help="Maximum power that can be shifted or controlled"
            )

            flex_hours = st.slider(
                "Flexibility Hours per Day",
                min_value=0.5,
                max_value=24.0,
                value=4.0,
                step=0.5,
                help="How many hours per day can you shift your electricity use?"
            )

        with col2:
            # Flexibility window
            st.markdown("**Flexibility Window**")
            window_col1, window_col2 = st.columns(2)
            with window_col1:
                window_start = st.time_input("Earliest Start", value=None, help="Earliest time you can start shifting")
            with window_col2:
                window_end = st.time_input("Latest Finish", value=None, help="Latest time shifting must be complete")

        # Tariff details
        st.markdown("#### 2. Electricity Tariff")

        col3, col4 = st.columns(2)

        with col3:
            baseline_rate = st.number_input(
                "Baseline Rate (p/kWh)",
                min_value=5.0,
                max_value=50.0,
                value=15.0,
                step=0.5,
                help="Your off-peak or average electricity rate"
            )

        with col4:
            peak_rate = st.number_input(
                "Peak Rate (p/kWh)",
                min_value=10.0,
                max_value=80.0,
                value=35.0,
                step=0.5,
                help="Your peak electricity rate (typically 4-7pm)"
            )

        # Participation rates
        st.markdown("#### 3. Realistic Usage")

        col5, col6 = st.columns(2)

        with col5:
            participation_low = st.slider(
                "Participation Rate - Low (%)",
                min_value=10,
                max_value=100,
                value=30,
                step=5,
                help="Conservative estimate: % of days/hours you'll actually use flexibility"
            )

        with col6:
            participation_high = st.slider(
                "Participation Rate - High (%)",
                min_value=10,
                max_value=100,
                value=80,
                step=5,
                help="Optimistic estimate: % of days/hours you'll actually use flexibility"
            )

        # Optional: Flexibility services
        st.markdown("#### 4. Potential Programs (Optional)")

        show_incentives = st.checkbox(
            "Programs may be available in my area",
            value=False,
            help="Show potential revenue from flexibility services. Availability varies by location and eligibility."
        )

        if show_incentives:
            # Service selection (from compatibility tool)
            services_list = [
                "Dynamic Containment (DC)",
                "Dynamic Moderation (DM)",
                "Dynamic Regulation (DR)",
                "Demand Flexibility Service (DFS)",
                "Peak load reduction (PR)",
                "Balancing Reserve (BR)",
                "Quick Reserve (QR)",
                "Static Firm Frequency Response (SFFR)",
            ]

            selected_services = st.multiselect(
                "Relevant Services for Your Asset",
                options=services_list,
                help="Select services your asset might qualify for (check technical requirements)"
            )

            col7, col8 = st.columns(2)
            with col7:
                availability_low = st.number_input(
                    "Availability Hours/Year (Low)",
                    min_value=100,
                    max_value=8760,
                    value=2000,
                    step=100,
                    help="Conservative: hours per year available for dispatch"
                )
            with col8:
                availability_high = st.number_input(
                    "Availability Hours/Year (High)",
                    min_value=100,
                    max_value=8760,
                    value=4000,
                    step=100,
                    help="Optimistic: hours per year available for dispatch"
                )
        else:
            selected_services = []
            availability_low = 0
            availability_high = 0

        # Optional: CO2 tracking
        st.markdown("#### 5. CO₂ Estimate (Optional)")

        show_co2 = st.checkbox(
            "Show carbon savings estimate",
            value=False,
            help="Estimate CO₂ avoided by shifting from peak to off-peak periods"
        )

        if show_co2:
            col9, col10 = st.columns(2)
            with col9:
                peak_emission = st.number_input(
                    "Peak Emission Factor (kg CO₂/kWh)",
                    min_value=0.1,
                    max_value=0.5,
                    value=0.25,
                    step=0.01,
                    help="Carbon intensity during peak hours"
                )
            with col10:
                offpeak_emission = st.number_input(
                    "Off-peak Emission Factor (kg CO₂/kWh)",
                    min_value=0.05,
                    max_value=0.3,
                    value=0.15,
                    step=0.01,
                    help="Carbon intensity during off-peak (more renewables)"
                )
        else:
            peak_emission = 0.25
            offpeak_emission = 0.15

        # Submit button
        submitted = st.form_submit_button("Calculate Value", type="primary", use_container_width=True)

        if submitted:
            # Store in session state
            st.session_state['estimator_inputs'] = {
                'capacity_kw': capacity_kw,
                'flex_hours': flex_hours,
                'window_start': window_start,
                'window_end': window_end,
                'baseline_rate': baseline_rate,
                'peak_rate': peak_rate,
                'participation_low': participation_low,
                'participation_high': participation_high,
                'show_incentives': show_incentives,
                'selected_services': selected_services,
                'availability_low': availability_low,
                'availability_high': availability_high,
                'show_co2': show_co2,
                'peak_emission': peak_emission,
                'offpeak_emission': offpeak_emission,
                'timestamp': datetime.now()
            }

            st.success("✅ Calculation complete! View results in the 'Results' tab.")

            # Log analytics event
            log_analytics_event("estimator_submit", {
                'capacity_kw': capacity_kw,
                'flex_hours': flex_hours,
                'show_incentives': show_incentives
            })


def render_estimator_results():
    """Render calculation results"""

    if 'estimator_inputs' not in st.session_state:
        st.info("👈 Enter your details in the 'Inputs' tab and click 'Calculate Value' to see results.")
        return

    inputs = st.session_state['estimator_inputs']

    st.subheader("Your Estimated Value")

    # Calculate results
    savings_low, savings_high = calculate_cost_savings(
        inputs['capacity_kw'],
        inputs['flex_hours'],
        inputs['peak_rate'],
        inputs['baseline_rate'],
        inputs['participation_low'],
        inputs['participation_high']
    )

    # Display cost savings
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Annual Cost Savings (Low)",
            f"£{savings_low:,.0f}",
            help="Conservative estimate based on minimum participation"
        )

    with col2:
        st.metric(
            "Annual Cost Savings (High)",
            f"£{savings_high:,.0f}",
            help="Optimistic estimate based on maximum participation"
        )

    with col3:
        st.metric(
            "Savings Range",
            f"£{savings_low:,.0f} - £{savings_high:,.0f}",
            help="Expected range of annual cost savings"
        )

    # Incentives (if enabled)
    if inputs.get('show_incentives') and inputs.get('selected_services'):
        st.markdown("---")
        st.markdown("### Potential Incentive Revenue")
        st.caption("⚠️ **If available** in your area and if eligible. Not guaranteed.")

        incentives_low, incentives_high = calculate_incentives(
            inputs['capacity_kw'],
            inputs['selected_services'],
            inputs['availability_low'],
            inputs['availability_high'],
            inputs['participation_low'],
            inputs['participation_high']
        )

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric(
                "Potential Incentives (Low)",
                f"£{incentives_low:,.0f}",
                help="Conservative revenue from selected services"
            )

        with col5:
            st.metric(
                "Potential Incentives (High)",
                f"£{incentives_high:,.0f}",
                help="Optimistic revenue from selected services"
            )

        with col6:
            total_low = savings_low + incentives_low
            total_high = savings_high + incentives_high
            st.metric(
                "Total Value Range",
                f"£{total_low:,.0f} - £{total_high:,.0f}",
                help="Combined savings + potential incentives"
            )
    else:
        incentives_low = 0
        incentives_high = 0

    # CO2 savings (if enabled)
    if inputs.get('show_co2'):
        st.markdown("---")
        st.markdown("### Carbon Savings Estimate")

        participation_avg = (inputs['participation_low'] + inputs['participation_high']) / 2
        co2_savings = calculate_co2_savings(
            inputs['capacity_kw'],
            inputs['flex_hours'],
            inputs['peak_emission'],
            inputs['offpeak_emission'],
            participation_avg
        )

        col7, col8 = st.columns(2)

        with col7:
            st.metric(
                "Estimated CO₂ Savings",
                f"{co2_savings:,.0f} kg/year",
                help="CO₂ avoided by shifting from peak to off-peak"
            )

        with col8:
            st.metric(
                "Equivalent to",
                f"{co2_savings / 1000:.1f} tonnes/year",
                help="Annual carbon reduction in tonnes"
            )

    # Visualization
    st.markdown("---")
    st.markdown("### Value Breakdown")

    # Create stacked bar chart
    fig = go.Figure()

    categories = ['Low Estimate', 'High Estimate']

    fig.add_trace(go.Bar(
        name='Cost Savings',
        x=categories,
        y=[savings_low, savings_high],
        marker_color='#667eea',
        text=[f'£{savings_low:,.0f}', f'£{savings_high:,.0f}'],
        textposition='inside'
    ))

    if inputs.get('show_incentives') and inputs.get('selected_services'):
        fig.add_trace(go.Bar(
            name='Potential Incentives',
            x=categories,
            y=[incentives_low, incentives_high],
            marker_color='#f093fb',
            text=[f'£{incentives_low:,.0f}', f'£{incentives_high:,.0f}'],
            textposition='inside'
        ))

    fig.update_layout(
        barmode='stack',
        title='Annual Value Estimate',
        yaxis_title='Annual Value (£)',
        height=400,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # Export button
    st.markdown("---")
    if st.button("📥 Export Results to CSV", use_container_width=True):
        csv_data = export_results_to_csv(inputs, savings_low, savings_high, incentives_low, incentives_high)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=f"flexibility_value_estimate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        log_analytics_event("result_export", {})


def render_estimator_assumptions():
    """Show transparent assumptions"""

    st.subheader("Assumptions & Transparency")

    st.markdown("""
    All calculations use transparent, editable assumptions. Here's what we assume:

    ### Cost Savings Calculation

    **Formula**:
    ```
    Annual Savings = (kWh shifted per day) × (Peak rate - Off-peak rate) × Participation rate × 365
    ```

    **Assumptions**:
    - Simple time-of-use tariff (two rates: peak and off-peak)
    - Consistent price differential throughout the year
    - No demand charges (add separately if applicable)
    - No additional costs for control systems
    - Linear scaling (no diminishing returns)

    **Limitations**:
    - Real tariffs may have multiple time bands
    - Actual participation depends on operations, weather, constraints
    - Does not account for rebound effects or efficiency losses
    - Network charges not included

    ---

    ### Incentive Revenue Calculation

    **Formula**:
    ```
    Annual Incentives = Capacity (kW) × Availability hours × Rate per kW-hour × Participation rate
    ```

    **Assumptions**:
    - You are eligible for selected services
    - Asset meets minimum technical requirements
    - Pre-qualification completed
    - Rates based on recent auction/tender results

    **Limitations**:
    - **Incentives are NOT guaranteed**—availability varies by location
    - Eligibility requirements must be verified
    - Competitive auctions—not all applicants accepted
    - Historical rates may not reflect future rates
    - Assumes no conflicts with existing contracts

    ---

    ### CO₂ Savings Calculation

    **Formula**:
    ```
    Annual CO₂ Savings = (kWh shifted) × (Peak emission factor - Off-peak emission factor) × 365
    ```

    **Assumptions**:
    - Average UK grid carbon intensity by time of day
    - Off-peak has higher renewable penetration
    - Avoided emissions (not absolute reduction)

    **Limitations**:
    - Grid intensity varies by location, season, weather
    - Simplified two-band model
    - Scope 2 (operational) emissions only

    ---

    ### Default Values (All Editable)

    | Parameter | Default | Source |
    |-----------|---------|--------|
    | Peak rate | 35 p/kWh | Typical UK commercial peak |
    | Off-peak rate | 15 p/kWh | Typical UK commercial off-peak |
    | Participation (low) | 30% | Conservative industry average |
    | Participation (high) | 80% | Optimistic industry average |
    | Peak CO₂ | 0.25 kg/kWh | UK grid peak hours |
    | Off-peak CO₂ | 0.15 kg/kWh | UK grid off-peak (more renewables) |

    ---

    **Full methodology**: See `ASSUMPTIONS.md` in the repository for complete details.
    """)


def render_estimator_methodology():
    """Explain methodology and link to sources"""

    st.subheader("Methodology & Sources")

    st.markdown("""
    ### How We Calculate Estimates

    This estimator uses transparent, client-side calculations to provide **indicative ranges**
    for potential value from energy flexibility. It is designed as a first-pass filter, not precise financial advice.

    #### Our Approach

    1. **Transparency over precision**: We show our work and let you adjust assumptions
    2. **Ranges, not point estimates**: Reflects real-world uncertainty
    3. **Conservative defaults**: Better to under-promise and over-deliver
    4. **No external APIs**: All calculations are deterministic and testable

    #### Data Sources

    - **ENA Open Networks Revenue Stacking Assessment Tool V1.0** (January 2025)
    - **NESO and DSO All Product Technical Requirements** (December 2024)
    - **NESO auction results** (Dynamic Containment, Dynamic Moderation, Dynamic Regulation)
    - **DNO flexibility tender outcomes** (Various regional markets)
    - **Retail tariff surveys** (Ofgem, industry reports)

    #### Validation

    Calculations reviewed against:
    - Industry case studies
    - Typical flexibility project results
    - Academic literature on demand response

    #### What's NOT Included

    - Capital costs (hardware, installation)
    - Ongoing management and monitoring costs
    - Efficiency losses (battery round-trip, HVAC rebound)
    - Penalties for non-performance
    - Tax implications

    #### Updates

    Default rates updated quarterly based on:
    - Latest NESO auction results
    - DNO tender outcomes
    - Wholesale market trends

    ---

    ### Next Steps

    1. **Use the estimate as a starting point**—not a guarantee
    2. **Check compatibility** of services using the "Check Compatibility" tab
    3. **Review technical requirements** to confirm eligibility
    4. **Contact NESO/DNO** to verify program availability and rates
    5. **Get professional advice** for detailed business case and contracts

    ---

    **Questions?** Visit the Contact tab to get in touch.
    """)


def export_results_to_csv(inputs: Dict, savings_low: float, savings_high: float,
                          incentives_low: float, incentives_high: float) -> str:
    """Export results to CSV format"""

    # Calculate CO2 if applicable
    if inputs.get('show_co2'):
        participation_avg = (inputs['participation_low'] + inputs['participation_high']) / 2
        co2_savings = calculate_co2_savings(
            inputs['capacity_kw'],
            inputs['flex_hours'],
            inputs['peak_emission'],
            inputs['offpeak_emission'],
            participation_avg
        )
    else:
        co2_savings = 0

    # Create dataframe
    data = {
        'Timestamp': [inputs['timestamp'].strftime('%Y-%m-%d %H:%M:%S')],
        'Shiftable Capacity (kW)': [inputs['capacity_kw']],
        'Flexibility Hours per Day': [inputs['flex_hours']],
        'Flexibility Window Start': [inputs.get('window_start', 'Not specified')],
        'Flexibility Window End': [inputs.get('window_end', 'Not specified')],
        'Baseline Tariff (p/kWh)': [inputs['baseline_rate']],
        'Peak Rate (p/kWh)': [inputs['peak_rate']],
        'Participation Rate Low (%)': [inputs['participation_low']],
        'Participation Rate High (%)': [inputs['participation_high']],
        'Annual Cost Savings Low (£)': [f"{savings_low:.2f}"],
        'Annual Cost Savings High (£)': [f"{savings_high:.2f}"],
        'Potential Incentives Low (£)': [f"{incentives_low:.2f}"],
        'Potential Incentives High (£)': [f"{incentives_high:.2f}"],
        'Total Value Low (£)': [f"{savings_low + incentives_low:.2f}"],
        'Total Value High (£)': [f"{savings_high + incentives_high:.2f}"],
        'CO2 Savings (kg/year)': [f"{co2_savings:.2f}"],
        'Selected Services': [', '.join(inputs.get('selected_services', []))],
        'Notes': ['']
    }

    df = pd.DataFrame(data)
    return df.to_csv(index=False)


def log_analytics_event(event_name: str, event_data: Dict):
    """Log analytics event (console + optional CSV)"""

    # Check if user consented to analytics
    if st.session_state.get('analytics_consent', False):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[ANALYTICS] {timestamp} | {event_name} | {event_data}")

        # Optional: append to CSV (if file exists)
        try:
            import os
            if os.path.exists('data/events_log.csv'):
                event_df = pd.DataFrame([{
                    'timestamp': timestamp,
                    'event': event_name,
                    'data': str(event_data)
                }])
                event_df.to_csv('data/events_log.csv', mode='a', header=False, index=False)
        except Exception as e:
            # Silent fail - analytics should never break the app
            pass
