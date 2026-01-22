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


# ============================================================================
# NEW COMPONENTS FOR V3.0 - VALUE STACKING FOCUSED
# ============================================================================

def render_stacking_explainer():
    """Render detailed explanation of the three stacking modes"""

    st.markdown("### Three Ways to Stack Services")

    # Co-delivery
    st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">🔄</div>
            <div class="mode-title">Co-delivery</div>
            <div class="mode-description">
                <strong>What it is:</strong> Use the same megawatt (MW) capacity for multiple services
                at the same time, in the same direction.<br><br>

                <strong>Example:</strong> A battery providing 2 MW of frequency response while also
                enrolled in the Capacity Market. Both services count the same 2 MW simultaneously.<br><br>

                <strong>When to use:</strong> When services have compatible technical requirements and
                don't conflict in their delivery obligations. This is the "holy grail" of stacking—
                getting paid twice for the same capacity.<br><br>

                <strong>Key requirement:</strong> Service rules must explicitly allow co-delivery,
                or at minimum not prohibit it.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Splitting
    st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">✂️</div>
            <div class="mode-title">Splitting</div>
            <div class="mode-description">
                <strong>What it is:</strong> Divide your asset's capacity between different services
                at the same time.<br><br>

                <strong>Example:</strong> A 5 MW battery split into 3 MW for Dynamic Containment
                and 2 MW for a local flexibility service. Both run simultaneously but use different
                portions of the battery.<br><br>

                <strong>When to use:</strong> When co-delivery isn't allowed but you have enough
                capacity to meet minimum requirements for multiple services. Common with large
                batteries or flexible industrial loads.<br><br>

                <strong>Key requirement:</strong> You must have sufficient capacity to meet the
                minimum size requirements for each service (e.g., many services require 1 MW minimum).
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Jumping
    st.markdown("""
        <div class="mode-card">
            <div class="mode-icon">⚡</div>
            <div class="mode-title">Jumping</div>
            <div class="mode-description">
                <strong>What it is:</strong> Switch the same asset between different services at
                different times of day or different days of the week.<br><br>

                <strong>Example:</strong> Using a battery for peak reduction during weekday afternoons
                (4-7pm), then switching to frequency response service during nights and weekends.<br><br>

                <strong>When to use:</strong> When services operate at different times or have
                different delivery windows. This is often the easiest form of stacking since there's
                no conflict—you're simply scheduling different activities.<br><br>

                <strong>Key requirement:</strong> Services must not require 24/7 availability, and
                you must have operational flexibility to switch modes. Contract terms should allow
                partial availability or scheduled participation.
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_educational_content():
    """Render educational content about value stacking strategies"""

    st.markdown("---")
    st.markdown("### Why Value Stacking Matters")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **The Challenge:**

        Individual flexibility services often provide modest returns. A single service might
        cover only 10-30% of the capital cost of a battery, or provide limited savings for
        industrial load shifting.

        Without stacking, many projects struggle to achieve commercial viability.
        """)

    with col2:
        st.markdown("""
        **The Opportunity:**

        By combining compatible services, you can:
        - Increase revenue by 2-5x compared to a single service
        - Improve project ROI and payback periods
        - De-risk investments by diversifying revenue streams
        - Make better use of existing assets
        """)

    st.markdown("---")
    st.markdown("### Getting Started with Stacking")

    with st.expander("Step 1: Understand Your Asset's Capabilities"):
        st.markdown("""
        Before exploring stacking opportunities, you need to know:

        - **Capacity:** How many MW can your asset provide?
        - **Response time:** How quickly can it react to signals? (seconds, minutes, hours)
        - **Duration:** How long can it sustain its response? (30 minutes, 2 hours, 4+ hours)
        - **Availability:** When is it available? (24/7, weekdays only, specific hours)
        - **Operational constraints:** What limits your flexibility? (production schedules, comfort requirements, battery cycling)

        This information determines which services you're technically eligible for and which
        stacking strategies are feasible.
        """)

    with st.expander("Step 2: Identify Compatible Services"):
        st.markdown("""
        Use the **Compatibility Tool** to check which services can be combined.

        Start with 2-3 services that seem relevant to your asset type:
        - **Batteries:** Dynamic Containment, Demand Flexibility Service, local DNO services
        - **EV Fleets:** Demand Flexibility Service, Triad avoidance, local flexibility
        - **HVAC/Buildings:** Peak reduction, Demand Flexibility Service
        - **Industrial:** Load shifting, local constraint management, peak reduction

        The tool will show you which combinations work for co-delivery, splitting, and jumping.
        """)

    with st.expander("Step 3: Evaluate Commercial Viability"):
        st.markdown("""
        Not all technically compatible combinations make commercial sense.

        Consider:
        - **Revenue potential:** Will the added complexity justify the extra revenue?
        - **Contract terms:** Lock-in periods, penalties, minimum commitments
        - **Operational complexity:** Can your team manage multiple service obligations?
        - **Technology requirements:** Do you need new control systems or metering?
        - **Risk:** What happens if you fail to deliver on one service?

        Start simple—often 2-3 well-chosen services provide 80% of the benefit with 20% of the complexity.
        """)

    with st.expander("Step 4: Plan Your Implementation"):
        st.markdown("""
        **Phased approach works best:**

        1. **Phase 1 (Months 1-3):** Start with one "anchor" service that provides stable,
           predictable revenue (e.g., Capacity Market, ToU optimization)

        2. **Phase 2 (Months 4-6):** Add a second compatible service using jumping
           (easiest to manage, no conflict risk)

        3. **Phase 3 (Months 7-12):** Explore splitting or co-delivery once you've built
           operational confidence

        **Key success factors:**
        - Strong control systems and automation
        - Clear operational procedures and fallback plans
        - Good relationships with service operators
        - Regular performance monitoring and optimization
        """)

    st.markdown("---")
    st.markdown("### Common Stacking Combinations")

    st.markdown("""
    Based on current UK market rules, here are some commonly viable stacking strategies:
    """)

    combo_col1, combo_col2 = st.columns(2)

    with combo_col1:
        st.markdown("""
        **For Large Batteries (>1 MW):**
        - Dynamic Containment + Capacity Market (co-delivery possible)
        - DC/DM + DNO services (splitting or jumping)
        - Wholesale trading + frequency services (jumping)

        **For Smaller Batteries (<1 MW):**
        - ToU arbitrage + Demand Flexibility Service (jumping)
        - Peak shaving + local flexibility services (co-delivery may be possible)
        """)

    with combo_col2:
        st.markdown("""
        **For EV Fleets:**
        - Smart charging + Demand Flexibility Service (jumping)
        - Triad avoidance + ToU optimization (co-delivery)

        **For Industrial/Commercial Sites:**
        - Peak reduction + HVAC flexibility (splitting)
        - Demand Flexibility Service + ToU shifting (co-delivery)
        - Local DNO services + Triad avoidance (jumping)
        """)

    st.info("""
    💡 **Important:** Market rules change frequently. Always verify current compatibility
    rules with NESO, your DNO, and service operators before committing to a stacking strategy.
    This tool reflects rules as of January 2025.
    """)


def render_simple_faq():
    """Render simplified FAQ focused on value stacking"""

    st.markdown("### Frequently Asked Questions")

    with st.expander("What is value stacking in energy flexibility?"):
        st.markdown("""
        Value stacking means combining revenue from multiple flexibility services
        to maximize the value of your energy asset.

        Instead of participating in just one program (e.g., only Capacity Market),
        you layer multiple revenue streams by carefully selecting compatible services.

        For example, a battery might earn revenue from:
        1. Capacity Market payments (for being available)
        2. Frequency response services (for rapid power adjustments)
        3. Local network support (for helping your DNO manage constraints)

        All using the same asset, at the same or different times.
        """)

    with st.expander("How do I know if services are compatible?"):
        st.markdown("""
        Use the **Compatibility Tool** tab to check specific service combinations.

        The tool is based on official ENA guidance and shows three compatibility modes:
        - **Co-delivery:** Can you use the same MW for both services simultaneously?
        - **Splitting:** Can you divide your asset between services?
        - **Jumping:** Can you switch between services at different times?

        If all three show "Explicit No," the services can't be stacked.
        If any show "Explicit Yes," there's a stacking opportunity.
        """)

    with st.expander("What's the difference between co-delivery, splitting, and jumping?"):
        st.markdown("""
        **Co-delivery (🔄):** The most valuable form. You get paid by multiple services
        for the *same* capacity at the *same* time. Example: Earning from both Capacity
        Market and Dynamic Containment with the same 2 MW battery.

        **Splitting (✂️):** You divide your capacity. Example: 3 MW for one service,
        2 MW for another, using a 5 MW battery. Both run simultaneously.

        **Jumping (⚡):** Time-based switching. Example: Frequency response at night,
        peak reduction during the day. Same asset, different times.

        See the "Learn About Stacking" tab for detailed explanations and examples.
        """)

    with st.expander("Do I need special equipment to stack services?"):
        st.markdown("""
        It depends on the services and your asset:

        **Minimum requirements:**
        - Smart metering (usually half-hourly settlement)
        - Some form of remote control or automation
        - Monitoring and reporting capability

        **For advanced stacking:**
        - Sophisticated control systems that can manage multiple obligations
        - Fast communication (especially for frequency services)
        - Battery management systems (for storage)
        - Building management systems (for HVAC/demand response)

        Start simple—jumping between services typically requires less sophisticated
        tech than co-delivery or splitting.
        """)

    with st.expander("What are the risks of value stacking?"):
        st.markdown("""
        **Operational risks:**
        - Conflicting obligations if compatibility rules change
        - Complexity in managing multiple service requirements
        - Performance penalties if you fail to deliver

        **Commercial risks:**
        - Contract lock-in periods that reduce flexibility
        - Market price changes reducing revenue expectations
        - Added costs for technology and operational management

        **How to mitigate:**
        - Start with 2-3 compatible services, not 5-6
        - Choose jumping over co-delivery initially (simpler, lower risk)
        - Build in contingency plans and "fail-safe" modes
        - Keep good records and monitor performance closely
        - Maintain relationships with service operators
        """)

    with st.expander("How much revenue can I expect from stacking?"):
        st.markdown("""
        Revenue varies widely based on:
        - Asset type, size, and capabilities
        - Which services you can access
        - Market conditions and auction results
        - Your operational flexibility and performance

        **Rough benchmarks (as of 2025):**
        - Battery (1 MW, 1 hour): £50k-150k/year for single service → £100k-300k/year with stacking
        - EV fleet (500 kW flexible load): £10k-30k/year savings/revenue
        - Industrial demand response (2 MW): £20k-80k/year

        These are indicative only. Actual results depend heavily on specific circumstances.

        **This tool does not provide value estimates** - it focuses on compatibility.
        Consult with service operators or energy consultants for project-specific revenue forecasts.
        """)

    with st.expander("Where should I start?"):
        st.markdown("""
        **1. Understand your asset** - Know your capacity, response time, duration, and operational constraints

        **2. Use the Compatibility Tool** - Check which services you could technically combine

        **3. Research service terms** - Visit NESO, your DNO, and service aggregator websites to
        understand eligibility, minimum sizes, and contract terms

        **4. Start simple** - Pick 1-2 compatible services for your first attempt. Jumping is
        usually easier than splitting or co-delivery.

        **5. Seek expert help** - Many aggregators and consultants offer free initial assessments.
        They can help navigate the complexity and handle the commercial arrangements.

        Use the **Contact** tab if you'd like to discuss your specific situation.
        """)


def render_simple_contact_form():
    """Render simplified contact form focused on value stacking questions"""

    st.markdown("""
    Have questions about value stacking or compatibility results?
    We typically respond within 2 working days.
    """)

    with st.form("simple_contact_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name *")
            email = st.text_input("Email *")

        with col2:
            org = st.text_input("Organization (optional)")
            asset_type = st.selectbox(
                "Primary Interest",
                options=[
                    "General question about value stacking",
                    "Battery storage project",
                    "EV fleet management",
                    "Industrial/commercial demand response",
                    "HVAC/building flexibility",
                    "Aggregator/service provider",
                    "Academic/research",
                    "Other"
                ]
            )

        message = st.text_area(
            "Your Question or Message",
            height=120,
            placeholder="E.g., 'I have a 2 MW battery in the Midlands and want to understand stacking options...'"
        )

        submitted = st.form_submit_button("Send Message", type="primary", use_container_width=True)

        if submitted:
            if not name or not email:
                st.error("Please fill in name and email")
            elif "@" not in email:
                st.error("Please enter a valid email address")
            else:
                success = save_lead(name, email, org, asset_type, message)

                if success:
                    st.success("✅ Message sent! We'll respond within 2 working days.")
                    log_analytics_event('contact_form_submit', {'interest': asset_type})
                else:
                    st.error("Something went wrong. Please try again or email us directly.")

    st.caption("🔒 We only use your details to respond to your inquiry. No spam, no third-party sharing.")
