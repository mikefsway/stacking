"""
Streamlit UI components for the revenue stacking tool
"""

import streamlit as st
from typing import List, Dict, Optional
from utils.descriptions import get_service_description, get_field_explanation


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
