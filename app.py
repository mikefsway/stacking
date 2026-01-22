"""
UK Energy Value Stacking Resource - V3.0

A simple, highly useful information resource on value stacking in UK energy flexibility markets,
foregrounding the interactive compatibility tool.
"""

import streamlit as st
from utils.data_loader import StackingDataLoader
from modules.ui_components import (
    render_service_selector,
    render_multi_service_compatibility,
    render_service_details,
    render_compatibility_matrix,
    render_stacking_explainer,
    render_educational_content,
    render_simple_faq,
    render_simple_contact_form,
    log_analytics_event
)

# Page configuration
st.set_page_config(
    page_title="UK Energy Value Stacking Resource",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# EXTENSIVE CUSTOM CSS TO LOOK LIKE A PROPER WEBSITE
# ============================================================================
st.markdown("""
    <style>
    /* Hide Streamlit branding and UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Remove padding and margins for full-width design */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }

    /* Custom color scheme - professional and clean */
    :root {
        --primary-color: #2563eb;
        --secondary-color: #1e40af;
        --accent-color: #3b82f6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --neutral-color: #6b7280;
        --background: #ffffff;
        --surface: #f9fafb;
        --border: #e5e7eb;
    }

    /* Hero section styling */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        line-height: 1.2;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        opacity: 0.95;
        max-width: 800px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
    }

    /* Section styling */
    .section {
        padding: 3rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 1rem;
        text-align: center;
    }

    .section-subtitle {
        font-size: 1.125rem;
        color: #4a5568;
        text-align: center;
        max-width: 700px;
        margin: 0 auto 2rem auto;
        line-height: 1.6;
    }

    /* Card styling */
    .info-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .info-card:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    .mode-card {
        background: linear-gradient(to bottom right, #f7fafc, #edf2f7);
        border-left: 4px solid var(--primary-color);
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 8px;
    }

    .mode-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .mode-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }

    .mode-description {
        color: #4a5568;
        line-height: 1.6;
    }

    /* Interactive tool styling */
    .tool-container {
        background: white;
        border: 2px solid #e2e8f0;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    .tool-title {
        font-size: 1.75rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
    }

    /* Improve Streamlit widgets */
    .stMultiSelect {
        background: white;
    }

    .stMultiSelect > div > div {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
    }

    .stButton > button {
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }

    /* Typography improvements */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    h1 {
        color: #1a202c;
        font-weight: 700;
    }

    h2 {
        color: #2d3748;
        font-weight: 600;
        margin-top: 2rem;
    }

    h3 {
        color: #4a5568;
        font-weight: 600;
    }

    /* Better spacing */
    .stMarkdown {
        line-height: 1.7;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        border-bottom: 2px solid #e2e8f0;
    }

    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 1.5rem;
        background-color: transparent;
        border-radius: 8px 8px 0 0;
        color: #6b7280;
        font-weight: 500;
        font-size: 1rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: white;
        color: var(--primary-color);
        font-weight: 600;
    }

    /* Compatibility results */
    .compatibility-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-weight: 600;
        margin: 0.25rem;
    }

    .badge-yes {
        background: #d1fae5;
        color: #065f46;
    }

    .badge-no {
        background: #fee2e2;
        color: #991b1b;
    }

    .badge-unknown {
        background: #fef3c7;
        color: #92400e;
    }

    /* Alert boxes */
    .stAlert {
        border-radius: 8px;
        border: none;
        padding: 1rem 1.5rem;
    }

    /* Expander styling */
    .stExpander {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        background: white;
        margin: 0.5rem 0;
    }

    /* Mobile responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }

        .hero-subtitle {
            font-size: 1rem;
        }

        .section-title {
            font-size: 1.75rem;
        }

        .section {
            padding: 2rem 1rem;
        }

        .tool-container {
            padding: 1rem;
        }

        .info-card {
            padding: 1.5rem;
        }
    }

    /* Footer styling */
    .custom-footer {
        background: #f9fafb;
        padding: 2rem;
        margin-top: 4rem;
        border-top: 1px solid #e5e7eb;
        text-align: center;
        color: #6b7280;
    }

    /* Data source badge */
    .data-source {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 8px;
        padding: 1rem;
        margin: 2rem auto;
        max-width: 800px;
        text-align: center;
        color: #1e40af;
    }

    /* Clean up default Streamlit styling */
    .element-container {
        margin-bottom: 0.5rem;
    }

    /* Tab content spacing */
    .stTabs [data-baseweb="tab-panel"] {
        padding-top: 2rem;
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
    """Main application - focus on value stacking education and compatibility tool"""

    # Load data
    data_loader = load_data()

    # ========================================================================
    # HERO SECTION
    # ========================================================================
    st.markdown("""
        <div class="hero-section">
            <h1 class="hero-title">UK Energy Value Stacking</h1>
            <p class="hero-subtitle">
                Understand how to combine multiple flexibility services to unlock more value
                from your energy assets. Simple, interactive tools to check compatibility
                and learn about stacking strategies.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ========================================================================
    # MAIN NAVIGATION TABS
    # ========================================================================
    tabs = st.tabs([
        "🔍 Compatibility Tool",
        "📚 Learn About Stacking",
        "💡 Resources",
        "📧 Contact"
    ])

    # ========================================================================
    # TAB 1: INTERACTIVE COMPATIBILITY TOOL (PRIMARY FOCUS)
    # ========================================================================
    with tabs[0]:
        log_analytics_event('tab_view', {'tab': 'compatibility_tool'})

        st.markdown('<div class="section">', unsafe_allow_html=True)

        st.markdown("""
            <h2 class="section-title">Check Service Compatibility</h2>
            <p class="section-subtitle">
                Select 2 or more UK flexibility services to instantly check if they can be
                "stacked" (combined) using three different strategies: co-delivery, splitting, or jumping.
            </p>
        """, unsafe_allow_html=True)

        # Interactive compatibility tool
        st.markdown('<div class="tool-container">', unsafe_allow_html=True)

        services = data_loader.get_services()
        selected_services = render_service_selector(services, key="main_selector")

        if len(selected_services) < 2:
            st.info("👆 **Get started:** Select at least 2 services above to check their compatibility")
        else:
            # Show compatibility results
            st.markdown("---")
            compatibility_results = data_loader.check_multi_compatibility(selected_services)
            render_multi_service_compatibility(compatibility_results)

            # Show detailed technical requirements
            with st.expander("📋 View Technical Requirements"):
                for service in selected_services:
                    tech_reqs = data_loader.get_technical_requirements(service)
                    render_service_details(service, tech_reqs)

        st.markdown('</div>', unsafe_allow_html=True)

        # Matrix view for advanced users
        st.markdown("---")
        st.markdown("### 📊 Advanced: Full Compatibility Matrix")
        st.markdown("View all possible combinations at once in a visual matrix format.")

        with st.expander("Show Compatibility Matrix"):
            matrix_services = st.multiselect(
                "Select services for matrix:",
                options=services,
                default=services[:6] if len(services) >= 6 else services,
                help="Select up to 10 services for best readability",
                key="matrix_selector"
            )

            if matrix_services:
                mode = st.selectbox(
                    "Stacking mode:",
                    options=['codelivery', 'splitting', 'jumping'],
                    format_func=lambda x: {
                        'codelivery': '🔄 Co-delivery',
                        'splitting': '✂️ Splitting',
                        'jumping': '⚡ Jumping'
                    }[x]
                )

                render_compatibility_matrix(matrix_services, data_loader, mode)

        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # TAB 2: EDUCATIONAL CONTENT ABOUT VALUE STACKING
    # ========================================================================
    with tabs[1]:
        log_analytics_event('tab_view', {'tab': 'learn_stacking'})

        st.markdown('<div class="section">', unsafe_allow_html=True)

        st.markdown("""
            <h2 class="section-title">What is Value Stacking?</h2>
            <p class="section-subtitle">
                Value stacking means combining multiple flexibility services to maximize
                revenue from your energy assets. Learn about the three main strategies
                and when to use each one.
            </p>
        """, unsafe_allow_html=True)

        # Render the stacking explainer component
        render_stacking_explainer()

        # Educational content
        render_educational_content()

        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # TAB 3: RESOURCES (FAQ, USE CASES, ETC.)
    # ========================================================================
    with tabs[2]:
        log_analytics_event('tab_view', {'tab': 'resources'})

        st.markdown('<div class="section">', unsafe_allow_html=True)

        st.markdown("""
            <h2 class="section-title">Resources & FAQ</h2>
            <p class="section-subtitle">
                Common questions about UK energy flexibility services and value stacking strategies.
            </p>
        """, unsafe_allow_html=True)

        render_simple_faq()

        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # TAB 4: CONTACT
    # ========================================================================
    with tabs[3]:
        log_analytics_event('tab_view', {'tab': 'contact'})

        st.markdown('<div class="section">', unsafe_allow_html=True)

        st.markdown("""
            <h2 class="section-title">Get in Touch</h2>
            <p class="section-subtitle">
                Questions about value stacking or need help understanding compatibility results?
            </p>
        """, unsafe_allow_html=True)

        render_simple_contact_form()

        st.markdown('</div>', unsafe_allow_html=True)

    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("""
        <div class="custom-footer">
            <div class="data-source">
                📊 <strong>Data Source:</strong> ENA Open Networks Revenue Stacking Assessment Tool V1.0 (January 2025)
                and NESO/DSO Technical Requirements (December 2024)
            </div>
            <p style="margin-top: 1rem; font-size: 0.875rem;">
                This tool provides guidance based on current UK flexibility market rules.
                Always verify eligibility and requirements with service operators before committing.
            </p>
            <p style="margin-top: 0.5rem; font-size: 0.75rem; color: #9ca3af;">
                UK Energy Value Stacking Resource © 2025 | Version 3.0
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
