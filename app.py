"""
UK Energy Revenue Stacking Explorer - Streamlit App V2.0

Main application file with tabbed architecture and enhanced UX
"""

import streamlit as st
from utils.data_loader import StackingDataLoader
from modules.ui_components import (
    render_service_selector,
    render_multi_service_compatibility,
    render_service_details,
    render_asset_specifications,
    render_compatibility_matrix,
    render_enhanced_sidebar,
    render_hero_section,
    render_what_is_flexibility,
    render_routes_to_value,
    render_how_tool_helps,
    render_use_case_cards,
    render_faq_glossary_tab,
    render_contact_form,
    log_analytics_event
)
from modules.estimator import render_estimator_tab

# Page configuration
st.set_page_config(
    page_title="UK Energy Flexibility Tool",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling and accessibility
st.markdown("""
    <style>
    /* Improved readability and contrast */
    .stAlert {
        padding: 1rem;
        margin: 1rem 0;
    }
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    h1 {
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    h2 {
        color: #4a5568;
        margin-top: 1.5rem;
    }
    h3 {
        margin-top: 1.5rem;
        color: #2d3748;
    }
    .stMultiSelect {
        margin-bottom: 1rem;
    }

    /* Improve button focus states for accessibility */
    button:focus {
        outline: 2px solid #667eea !important;
        outline-offset: 2px !important;
    }

    /* Better spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_data():
    """Load and cache the stacking data"""
    loader = StackingDataLoader()
    loader.load_data()
    return loader


def main():
    """Main application logic with tabbed architecture"""

    # Load data
    data_loader = load_data()

    # Render enhanced sidebar
    render_enhanced_sidebar(data_loader.get_metadata())

    # Main content area - create tabs
    tabs = st.tabs([
        "🏠 Overview",
        "🔍 Check Compatibility",
        "📊 Matrix View",
        "💰 Value Estimator",
        "📑 Use Cases",
        "❓ FAQ & Glossary",
        "📧 Contact"
    ])

    # ========================================================================
    # TAB 1: OVERVIEW
    # ========================================================================
    with tabs[0]:
        log_analytics_event('tab_view', {'tab': 'overview'})

        render_hero_section()
        render_what_is_flexibility()
        render_routes_to_value()
        render_how_tool_helps()

        # Estimator disclaimer
        st.markdown("---")
        with st.expander("⚠️ Important: About Our Estimates"):
            st.markdown("""
            **These are estimates based on your inputs and general assumptions, not advice.**

            Actual outcomes depend on:
            - Your specific tariff structure and rates
            - Operational constraints and flexibility in practice
            - Eligibility for programs (location, asset type, capacity)
            - Contract terms, performance requirements, and penalties
            - Market conditions and auction results

            **Always verify**:
            1. Tariff details with your energy supplier
            2. Eligibility and technical requirements with NESO/DNO
            3. Compatibility with existing contracts
            4. Commercial terms before committing
            """)

    # ========================================================================
    # TAB 2: CHECK COMPATIBILITY
    # ========================================================================
    with tabs[1]:
        log_analytics_event('tab_view', {'tab': 'check_compatibility'})

        st.header("Check Service Compatibility")

        st.markdown("""
        Select 2 or more flexibility services to check if they can be "stacked" (combined) for greater value.
        We'll show you three stacking modes: **co-delivery**, **splitting**, and **jumping**.
        """)

        col1, col2 = st.columns([1, 1])

        with col1:
            # Service selection
            services = data_loader.get_services()
            selected_services = render_service_selector(services, key="main_selector")

            # Asset specifications (optional)
            if selected_services:
                asset_specs = render_asset_specifications()

        with col2:
            # Show instructions if no services selected
            if not selected_services:
                st.info("👈 Select at least 2 services from the left to begin analysis")
            elif len(selected_services) == 1:
                st.warning("Please select at least 2 services to compare compatibility")
            else:
                st.success(f"Analyzing {len(selected_services)} services...")

        # Show results when services are selected
        if len(selected_services) >= 2:
            st.markdown("---")

            # Compatibility analysis
            compatibility_results = data_loader.check_multi_compatibility(selected_services)

            # Sub-tabs for results and details
            result_tab1, result_tab2 = st.tabs(["📊 Compatibility Results", "📋 Service Details"])

            with result_tab1:
                render_multi_service_compatibility(compatibility_results)

                # CTA after results
                st.markdown("---")
                st.info("💡 **Need help understanding these results?** Visit the Contact tab to get in touch.")

            with result_tab2:
                st.markdown("### Technical Requirements")
                st.caption("Explore detailed technical specifications for each selected service")

                for service in selected_services:
                    tech_reqs = data_loader.get_technical_requirements(service)
                    render_service_details(service, tech_reqs)

    # ========================================================================
    # TAB 3: MATRIX VIEW
    # ========================================================================
    with tabs[2]:
        log_analytics_event('tab_view', {'tab': 'matrix_view'})

        st.header("Compatibility Matrix")

        st.markdown("""
        Visual overview of compatibility between all services. Select services and a stacking mode to see the full matrix.
        """)

        # Service selection for matrix
        services = data_loader.get_services()
        matrix_services = st.multiselect(
            "Select services to include in matrix:",
            options=services,
            default=services[:6] if len(services) >= 6 else services,
            help="Select up to 12 services for best visibility",
            key="matrix_selector"
        )

        if matrix_services:
            mode = st.selectbox(
                "Select compatibility mode:",
                options=['codelivery', 'splitting', 'jumping'],
                format_func=lambda x: {
                    'codelivery': '🔄 Co-delivery (same MW, same time)',
                    'splitting': '✂️ Splitting (different MW, same time)',
                    'jumping': '⚡ Jumping (same asset, different times)'
                }[x]
            )

            render_compatibility_matrix(matrix_services, data_loader, mode)

            # Explanation
            with st.expander("ℹ️ What do these modes mean?"):
                st.markdown("""
                **Co-delivery** 🔄: Using the same MW for multiple services at the same time in the same direction.
                Example: Providing frequency response while in a capacity market contract.

                **Splitting** ✂️: Dividing your asset's capacity between different services at the same time.
                Example: A 5 MW battery split into 3 MW for one service and 2 MW for another.

                **Jumping** ⚡: Switching the same asset between different services at different times.
                Example: Providing peak reduction during the day, then frequency response at night.
                """)
        else:
            st.info("👆 Select services above to view the compatibility matrix")

    # ========================================================================
    # TAB 4: VALUE ESTIMATOR
    # ========================================================================
    with tabs[3]:
        log_analytics_event('tab_view', {'tab': 'value_estimator'})

        render_estimator_tab()

    # ========================================================================
    # TAB 5: USE CASES
    # ========================================================================
    with tabs[4]:
        log_analytics_event('tab_view', {'tab': 'use_cases'})

        render_use_case_cards()

        # CTA
        st.markdown("---")
        st.markdown("### Ready to Explore Your Value?")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("💰 Go to Value Estimator", use_container_width=True, type="primary"):
                st.session_state['navigate_to'] = 'Value Estimator'
                st.info("👆 Click on the 'Value Estimator' tab above to continue")

        with col2:
            if st.button("📧 Contact Us", use_container_width=True):
                st.session_state['navigate_to'] = 'Contact'
                st.info("👆 Click on the 'Contact' tab above to get in touch")

    # ========================================================================
    # TAB 6: FAQ & GLOSSARY
    # ========================================================================
    with tabs[5]:
        log_analytics_event('tab_view', {'tab': 'faq_glossary'})

        render_faq_glossary_tab()

    # ========================================================================
    # TAB 7: CONTACT
    # ========================================================================
    with tabs[6]:
        log_analytics_event('tab_view', {'tab': 'contact'})

        render_contact_form()

    # Footer (always visible)
    st.markdown("---")
    footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])

    with footer_col1:
        st.caption("📊 Data source: ENA Open Networks Revenue Stacking Assessment Tool V1.0 (Jan 2025)")

    with footer_col2:
        st.caption("© 2025 | Built with Streamlit")

    with footer_col3:
        st.caption("Version 2.0")


if __name__ == "__main__":
    main()
