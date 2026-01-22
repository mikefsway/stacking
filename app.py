"""
UK Energy Revenue Stacking Explorer - Streamlit App

Main application file for the revenue stacking compatibility tool.
"""

import streamlit as st
from utils.data_loader import StackingDataLoader
from modules.ui_components import (
    render_header,
    render_service_selector,
    render_multi_service_compatibility,
    render_service_details,
    render_asset_specifications,
    render_compatibility_matrix,
    render_sidebar_info
)

# Page configuration
st.set_page_config(
    page_title="UK Energy Revenue Stacking Explorer",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
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
    }
    h3 {
        margin-top: 1.5rem;
    }
    .stMultiSelect {
        margin-bottom: 1rem;
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
    """Main application logic"""

    # Load data
    data_loader = load_data()

    # Render header
    render_header()

    # Render sidebar
    render_sidebar_info(data_loader.get_metadata())

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        # Service selection
        services = data_loader.get_services()
        selected_services = render_service_selector(services)

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

        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Compatibility Results", "📋 Service Details", "🔢 Matrix View"])

        with tab1:
            render_multi_service_compatibility(compatibility_results)

        with tab2:
            st.markdown("### Technical Requirements")
            st.caption("Explore detailed technical specifications for each selected service")

            for service in selected_services:
                tech_reqs = data_loader.get_technical_requirements(service)
                render_service_details(service, tech_reqs)

        with tab3:
            mode = st.selectbox(
                "Select compatibility mode:",
                options=['codelivery', 'splitting', 'jumping'],
                format_func=lambda x: {
                    'codelivery': '🔄 Co-delivery (same MW, same time)',
                    'splitting': '✂️ Splitting (different MW, same time)',
                    'jumping': '⚡ Jumping (same asset, different times)'
                }[x]
            )

            render_compatibility_matrix(selected_services, data_loader, mode)

    # Footer
    st.markdown("---")
    st.caption("Data source: ENA Open Networks Revenue Stacking Assessment Tool V1.0 (Jan 2025)")
    st.caption("© 2025 | Built with Streamlit")


if __name__ == "__main__":
    main()
