"""
Streamlit UI components for the revenue stacking tool
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
from utils.descriptions import get_service_description, get_field_explanation, get_glossary, get_faqs_by_category


def render_header():
    """Render the app header"""
    st.title("🔋 UK Energy Revenue Stacking Explorer")
    st.markdown("*Discover compatible flexibility services and maximize your revenue opportunities*")
    st.markdown("---")


def render_service_selector(services: List[str], key: str = "service_selector") -> List[str]:
    """
    Render multi-service selector

    Args:
        services: List of available services
        key: Unique key for the widget

    Returns:
        List of selected services
    """
    st.subheader("🎯 Select Services to Compare")

    st.info("💡 **Multi-Service Comparison**: Select 2 or more services to check if they can be stacked together. "
            "The tool will analyze all possible combinations and provide plain English explanations for any conflicts.")

    selected = st.multiselect(
        "Choose services (you can select multiple):",
        options=services,
        key=key,
        help="Select at least 2 services to compare their compatibility"
    )

    return selected


def render_compatibility_badge(value: str) -> str:
    """
    Determine compatibility status and return badge emoji

    Args:
        value: Compatibility value from data

    Returns:
        Emoji representing status
    """
    if not value:
        return "❓"
    elif "Explicit Yes" in value:
        return "✅"
    elif "Explicit No" in value:
        return "❌"
    elif "No Data" in value:
        return "❓"
    elif "N/A" in value:
        return "⚠️"
    else:
        return "❓"


def render_compatibility_results(results: Dict, service1: str, service2: str):
    """
    Render compatibility results for a service pair

    Args:
        results: Dictionary with codelivery, splitting, jumping results
        service1: First service name
        service2: Second service name
    """
    st.markdown(f"### Compatibility: **{service1}** ↔️ **{service2}**")

    col1, col2, col3 = st.columns(3)

    # Co-delivery
    with col1:
        codelivery = results.get('codelivery', {})
        badge = render_compatibility_badge(codelivery.get('value'))
        st.markdown(f"#### {badge} Co-delivery")
        value = codelivery.get('value', 'No data available')
        st.markdown(f"*Same MW, same time, same direction*")
        if "Explicit Yes" in value:
            st.success(value)
        elif "Explicit No" in value:
            st.error(value)
        elif "No Data" in value:
            st.warning(value)
        else:
            st.info(value)

    # Splitting
    with col2:
        splitting = results.get('splitting', {})
        badge = render_compatibility_badge(splitting.get('value'))
        st.markdown(f"#### {badge} Splitting")
        value = splitting.get('value', 'No data available')
        st.markdown(f"*Different MW, same asset, same time*")
        if "Explicit Yes" in value:
            st.success(value)
        elif "Explicit No" in value:
            st.error(value)
        elif "No Data" in value:
            st.warning(value)
        else:
            st.info(value)

    # Jumping
    with col3:
        jumping = results.get('jumping', {})
        badge = render_compatibility_badge(jumping.get('value'))
        st.markdown(f"#### {badge} Jumping")
        value = jumping.get('value', 'No data available')
        st.markdown(f"*Same asset, different times*")
        if "Explicit Yes" in value:
            st.success(value)
        elif "Explicit No" in value:
            st.error(value)
        elif "No Data" in value:
            st.warning(value)
        else:
            st.info(value)

    st.markdown("---")


def render_multi_service_compatibility(all_results: Dict):
    """
    Render compatibility results for multiple service pairs

    Args:
        all_results: Dictionary with all pair-wise compatibility results
    """
    st.subheader("📊 Compatibility Results")

    for pair_key, results in all_results.items():
        service1, service2 = pair_key.split('|')
        render_compatibility_results(results, service1, service2)


def render_service_details(service_name: str, tech_requirements: Dict, max_fields: int = 8):
    """
    Render technical details for a service

    Args:
        service_name: Name of the service
        tech_requirements: Dictionary of technical requirements
        max_fields: Maximum number of fields to display
    """
    st.markdown(f"### 📋 {service_name}")

    # Show service description if available
    description = get_service_description(service_name)
    if description:
        st.info(f"💡 {description}")

    # Show technical requirements
    if tech_requirements:
        st.markdown("**Technical Requirements:**")

        fields = list(tech_requirements.items())[:max_fields]

        for key, value in fields:
            # Split category and name
            if '|' in key:
                category, name = key.split('|', 1)
            else:
                name = key

            # Get explanation if available
            explanation = get_field_explanation(name)

            # Create expandable section with explanation
            with st.expander(f"**{name}**" + (" ℹ️" if explanation else "")):
                if explanation:
                    st.caption(f"*{explanation}*")
                st.write(value)
    else:
        st.warning("No technical requirements available for this service")

    st.markdown("---")


def render_asset_specifications():
    """
    Render optional asset specifications input section

    Returns:
        Dictionary with capacity, response_time, duration
    """
    with st.expander("⚙️ My Asset Specifications (Optional)", expanded=False):
        st.markdown("*Enter your asset specifications to get personalized recommendations*")

        col1, col2, col3 = st.columns(3)

        with col1:
            capacity = st.number_input(
                "Capacity (MW)",
                min_value=0.0,
                step=0.1,
                help="The maximum power capacity of your asset"
            )

        with col2:
            response_time = st.number_input(
                "Response Time (minutes)",
                min_value=0.0,
                step=0.5,
                help="How quickly your asset can respond to instructions"
            )

        with col3:
            duration = st.number_input(
                "Available Duration (hours)",
                min_value=0.0,
                step=0.5,
                help="How long your asset can sustain its response"
            )

        return {
            'capacity': capacity,
            'response_time': response_time,
            'duration': duration
        }


def render_compatibility_matrix(services: List[str], data_loader, mode: str = 'codelivery'):
    """
    Render a compatibility matrix for visualization

    Args:
        services: List of services to include
        data_loader: StackingDataLoader instance
        mode: 'codelivery', 'splitting', or 'jumping'
    """
    st.subheader(f"📊 {mode.capitalize()} Compatibility Matrix")

    # Create matrix data
    matrix_data = []
    for service1 in services[:12]:  # Limit to first 12 for readability
        row = {'Service': service1[:20]}  # Truncate long names
        for service2 in services[:12]:
            result = data_loader.get_compatibility(service1, service2, mode)
            badge = render_compatibility_badge(result.get('value'))
            row[service2[:20]] = badge
        matrix_data.append(row)

    # Display as dataframe
    import pandas as pd
    df = pd.DataFrame(matrix_data)
    df.set_index('Service', inplace=True)

    st.dataframe(df, use_container_width=True)

    st.caption("✅ = Compatible | ❌ = Incompatible | ❓ = No Data | ⚠️ = Not Applicable")


def render_info_box(title: str, content: str, icon: str = "ℹ️"):
    """
    Render an information box

    Args:
        title: Box title
        content: Box content
        icon: Icon to display
    """
    st.info(f"{icon} **{title}**\n\n{content}")


def render_sidebar_info(metadata: Dict):
    """
    Render sidebar with app information

    Args:
        metadata: Metadata about the dataset
    """
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/streamlit/streamlit/develop/docs/_static/favicon.png",
                 width=50)
        st.title("About")

        st.markdown(f"""
        **{metadata.get('title', 'Revenue Stacking Tool')}**

        Version: {metadata.get('version', 'N/A')}

        Source: {metadata.get('source', 'ENA Open Networks')}

        Date: {metadata.get('date', 'N/A')}
        """)

        st.markdown("---")

        st.markdown("""
        ### How to Use

        1. **Select Services**: Choose 2 or more services to compare
        2. **Check Compatibility**: View results for co-delivery, splitting, and jumping
        3. **Review Details**: Explore technical requirements with helpful tooltips
        4. **(Optional)** Enter asset specs for recommendations

        ### Terminology

        - **Co-delivery**: Same MW, same time, same direction
        - **Splitting**: Different MW splits, same asset, same time
        - **Jumping**: Same asset, different time periods
        """)

        st.markdown("---")

        st.markdown("""
        ### Need Help?

        Hover over ℹ️ icons throughout the app for explanations of technical terms.
        """)


# ============================================================================
# NEW COMPONENTS FOR V2.0
# ============================================================================

def render_hero_section():
    """Render hero section for Overview tab"""

    st.markdown("""
    # Unlock More Value from Your Energy Flexibility

    Use your assets more smartly—shift when you use power to cut costs, open potential revenue
    pathways, and de-risk participation in UK flexibility services. No energy market expertise required.
    """)

    # Primary and secondary CTAs
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        # This button will be handled in the main app to switch tabs
        if st.button("🎯 Estimate Your Value", type="primary", use_container_width=True):
            st.session_state['navigate_to'] = 'Value Estimator'
            log_analytics_event('hero_cta_click', {'cta': 'estimate_value'})

    with col2:
        if st.button("🔍 Check Compatibility", use_container_width=True):
            st.session_state['navigate_to'] = 'Check Compatibility'
            log_analytics_event('hero_cta_click', {'cta': 'check_compatibility'})

    # Trust strip
    st.markdown("---")
    st.caption(
        "📊 Based on **ENA Open Networks** (V1.0, Jan 2025) and "
        "**NESO/DSO** technical requirements (Dec 2024)"
    )


def render_what_is_flexibility():
    """Render 'What is Energy Flexibility' section"""

    st.markdown("---")
    st.subheader("What is Energy Flexibility?")

    st.markdown("""
    Energy flexibility is your ability to shift or shape when devices use electricity—like precooling,
    delaying EV charging, or dispatching a battery at peak times. Used well, it can reduce bills,
    earn incentives where available, and improve resilience.
    """)


def render_routes_to_value():
    """Render 'Routes to Value' section"""

    st.markdown("---")
    st.subheader("Routes to Value")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### 💰 Cut Costs
        Avoid peak electricity prices and demand charges where applicable. Simple scheduling can reduce your energy bill.
        """)

    with col2:
        st.markdown("""
        ### 💷 Potential New Revenue
        Some UK programs may reward flexible demand. Check eligibility and compatibility before committing.
        """)

    with col3:
        st.markdown("""
        ### 🌱 Operational Value
        Smoother operations, improved resilience, and potential for lower carbon emissions claims.
        """)


def render_how_tool_helps():
    """Render 'How This Tool Helps' section"""

    st.markdown("---")
    st.subheader("How This Tool Helps")

    steps = [
        ("1. Estimate Value", "Get an indicative range of potential savings and revenue based on your assets"),
        ("2. Check Compatibility", "See which flexibility services can be 'stacked' (used together)"),
        ("3. Understand Requirements", "Plain-English explanations of technical terms and program requirements"),
        ("4. Find Your Path", "Use case cards for common assets (EV fleets, batteries, HVAC, manufacturing)")
    ]

    for step, description in steps:
        st.markdown(f"**{step}**: {description}")


def render_use_case_cards():
    """Render use case cards for common assets"""

    st.header("Use Cases by Asset Type")

    st.markdown("Find your asset type below to see quick wins and considerations.")

    # Use case 1: EV Fleet Charging
    with st.expander("🚗 EV Fleet Charging", expanded=False):
        st.markdown("""
        **How it helps**: Delay or ramp charging to avoid peak prices; align with cheaper periods or renewable availability.

        **What it takes**: Charger control + basic schedules; optional dynamic price feed.

        **Quick wins**:
        - Night-time charging policies
        - Fleet stagger to avoid simultaneous peaks
        - Simple price thresholds (e.g., charge only when price < 20p/kWh)

        **Watch-outs**:
        - Driver needs (charge windows)
        - Duty cycles and vehicle availability
        - Depot power limits
        - Range anxiety for operational requirements
        """)

    # Use case 2: Battery Energy Storage
    with st.expander("🔋 Battery Energy Storage", expanded=False):
        st.markdown("""
        **How it helps**: Charge when prices are low, discharge at peaks; provide rapid grid services for additional revenue.

        **What it takes**: Battery control system; half-hourly or faster metering; pre-qualification for some services.

        **Quick wins**:
        - Time-of-use arbitrage (charge cheap, discharge expensive)
        - Peak shaving for demand charge reduction
        - Dynamic Containment (if qualified and meets 1 MW minimum)

        **Watch-outs**:
        - Cycling limits and battery degradation
        - Minimum capacity requirements (1 MW for many services)
        - Contract lock-in periods
        - Balancing multiple revenue streams
        """)

    # Use case 3: HVAC
    with st.expander("🏢 HVAC (Heating, Ventilation, Air Conditioning)", expanded=False):
        st.markdown("""
        **How it helps**: Precool/preheat during off-peak hours; reduce load during peak periods while maintaining comfort.

        **What it takes**: Building management system (BMS) or smart thermostat; understanding of thermal mass and comfort constraints.

        **Quick wins**:
        - Setback schedules for nights/weekends
        - Precooling before demand peaks
        - Avoiding peak pricing windows (4-7pm)

        **Watch-outs**:
        - Occupant comfort and complaints
        - Building thermal properties (insulation, thermal mass)
        - Weather variability and forecasting
        - Rebound peaks after setback periods
        """)

    # Use case 4: Industrial/Manufacturing
    with st.expander("🏭 Industrial / Manufacturing Processes", expanded=False):
        st.markdown("""
        **How it helps**: Shift non-critical loads (pumps, compressors, cold storage) to off-peak; reduce demand charges.

        **What it takes**: Process flexibility analysis; control systems; sometimes buffer storage (thermal, material).

        **Quick wins**:
        - Schedule batch processes overnight
        - Stagger motor starts to reduce peak demand
        - Optimize compressed air and cooling timing

        **Watch-outs**:
        - Production schedules and deadlines
        - Quality constraints and process windows
        - Shift patterns and labor availability
        - Safety interlocks and critical processes
        """)


def render_faq_glossary_tab():
    """Render FAQ & Glossary tab"""

    st.header("FAQ & Glossary")

    # Create sub-tabs for FAQ and Glossary
    faq_tab, glossary_tab = st.tabs(["❓ Frequently Asked Questions", "📖 Glossary"])

    with faq_tab:
        st.subheader("Frequently Asked Questions")

        # Get FAQs organized by category
        faqs_by_category = get_faqs_by_category()

        # Display by category
        for category, faqs in faqs_by_category.items():
            st.markdown(f"### {category}")

            for faq in faqs:
                with st.expander(f"**{faq['question']}**"):
                    st.markdown(faq['answer'])

            st.markdown("---")

    with glossary_tab:
        st.subheader("Glossary of Terms")

        st.markdown("Click on any term below to see its definition and an example.")

        glossary = get_glossary()

        # Display glossary alphabetically
        for term in sorted(glossary.keys()):
            details = glossary[term]
            with st.expander(f"**{term}**"):
                st.markdown(f"**Definition**: {details['definition']}")
                if 'example' in details:
                    st.markdown(f"**Example**: {details['example']}")


def render_contact_form():
    """Render contact/lead capture form"""

    st.header("Get in Touch")

    st.markdown("""
    Interested in unlocking value from your energy flexibility? Have questions about compatibility or next steps?

    Fill in the form below and we'll respond within 2 working days.
    """)

    with st.form("contact_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input(
                "Name *",
                help="Your full name"
            )

            email = st.text_input(
                "Email *",
                help="We'll use this to respond to you"
            )

        with col2:
            org = st.text_input(
                "Organization",
                help="Company or organization name (optional)"
            )

            asset_type = st.selectbox(
                "Asset Type",
                options=[
                    "Not sure / General inquiry",
                    "EV Fleet",
                    "Battery Storage",
                    "HVAC / Building",
                    "Industrial / Manufacturing",
                    "Solar PV",
                    "Combined (Multiple assets)",
                    "Other"
                ],
                help="What type of flexible asset do you have?"
            )

        message = st.text_area(
            "Message",
            height=150,
            help="Tell us about your situation or question"
        )

        # Privacy note
        st.caption(
            "🔒 **Privacy**: We'll only use your contact details to respond to your inquiry. "
            "We do not share your information with third parties."
        )

        # Submit button
        submitted = st.form_submit_button("Send Message", type="primary", use_container_width=True)

        if submitted:
            # Validate required fields
            if not name or not email:
                st.error("❌ Please fill in all required fields (Name and Email)")
            elif "@" not in email:
                st.error("❌ Please enter a valid email address")
            else:
                # Save to leads.csv
                success = save_lead(name, email, org, asset_type, message)

                if success:
                    st.success(
                        "✅ **Thank you!** Your message has been received. "
                        "We'll be in touch within 2 working days."
                    )
                    log_analytics_event('lead_form_submit_success', {
                        'asset_type': asset_type,
                        'has_message': bool(message)
                    })
                else:
                    st.error(
                        "❌ **Oops!** Something went wrong. Please try again or email us directly."
                    )
                    log_analytics_event('lead_form_submit_error', {})


def save_lead(name: str, email: str, org: str, asset_type: str, message: str) -> bool:
    """Save lead to CSV file"""

    try:
        import os
        from pathlib import Path

        # Ensure data directory exists
        Path('data').mkdir(exist_ok=True)

        # Create lead record
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        lead_data = {
            'timestamp': [timestamp],
            'name': [name],
            'email': [email],
            'organization': [org],
            'asset_type': [asset_type],
            'message': [message]
        }

        df = pd.DataFrame(lead_data)

        # Append to CSV (create if doesn't exist)
        file_path = 'data/leads.csv'
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, mode='w', header=True, index=False)

        return True

    except Exception as e:
        print(f"Error saving lead: {e}")
        return False


def log_analytics_event(event_name: str, event_data: Dict):
    """Log analytics event to console and optional CSV"""

    # Check if user consented to analytics
    if st.session_state.get('analytics_consent', True):  # Default True for local logging
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[ANALYTICS] {timestamp} | {event_name} | {event_data}")

        # Optional: append to CSV
        try:
            import os
            from pathlib import Path

            Path('data').mkdir(exist_ok=True)
            file_path = 'data/events_log.csv'

            event_df = pd.DataFrame([{
                'timestamp': timestamp,
                'event': event_name,
                'data': str(event_data)
            }])

            if os.path.exists(file_path):
                event_df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                event_df.to_csv(file_path, mode='w', header=True, index=False)

        except Exception as e:
            # Silent fail - analytics should never break the app
            pass


def render_analytics_consent():
    """Render analytics consent in sidebar"""

    with st.sidebar:
        st.markdown("---")

        with st.expander("📊 Analytics & Privacy"):
            st.markdown("""
            **Optional Analytics**

            We log basic usage events (page views, button clicks) locally for improving the tool.
            No third-party trackers. No personal data shared.
            """)

            consent = st.checkbox(
                "I'm okay with local event logging",
                value=st.session_state.get('analytics_consent', True),
                key='analytics_consent'
            )


def render_enhanced_sidebar(metadata: Dict):
    """Enhanced sidebar with value statement and quick access"""

    with st.sidebar:
        st.title("UK Energy Flexibility Tool")

        st.markdown("""
        Cut costs and open new revenue pathways by shifting when you use power—no energy market expertise required.
        """)

        st.markdown("---")

        # Data sources expander
        with st.expander("📊 Methodology & Sources"):
            st.markdown(f"""
            **Data Sources**

            This tool is based on:
            - **ENA Open Networks Revenue Stacking Assessment Tool V1.0** (January 2025)
            - **NESO and DSO All Product Technical Requirements** (December 2024)

            Version: {metadata.get('version', 'N/A')}

            Date: {metadata.get('date', 'N/A')}

            All compatibility data reflects current rules as of January 2025. Program terms may change—always verify with the relevant service operator.
            """)

        # Quick glossary
        with st.expander("📖 Quick Glossary"):
            st.markdown("""
            **Quick Definitions**

            - **Flexibility**: Shifting when you use power
            - **Stacking**: Combining multiple services for more value
            - **Co-delivery**: Same capacity, same time
            - **Splitting**: Divide capacity between services
            - **Jumping**: Switch services at different times

            See the FAQ & Glossary tab for full definitions.
            """)

        st.markdown("---")

        # How to use
        st.markdown("""
        ### How to Use

        1. **Overview**: Understand the value proposition
        2. **Estimate Value**: Get indicative savings/revenue
        3. **Check Compatibility**: See which services stack
        4. **Review Use Cases**: Find your asset type
        5. **Contact**: Get help with next steps

        ### Need Help?

        Visit the **Contact** tab to get in touch.
        """)

        # Analytics consent
        render_analytics_consent()
