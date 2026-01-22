# UK Energy Flexibility Tool (Revenue Stacking Explorer)

A Streamlit web application for entrepreneurs and energy asset owners to estimate value, analyze compatibility between UK flexibility services, and optimize revenue stacking opportunities—without needing energy market expertise.

## Overview

This tool helps you unlock more value from your energy flexibility by:
- **Estimating potential savings and revenue** from shifting when you use power
- **Checking which flexibility services can be "stacked"** (combined) for greater value
- **Understanding technical requirements** in plain English
- **Finding your path** with use-case examples for common assets (EV fleets, batteries, HVAC, manufacturing)

Perfect for busy entrepreneurs who want to derive business value from energy flexibility but are not flexibility experts.

## Features (V2.0)

### For Entrepreneurs & Business Owners

- 💰 **Value Estimator**: Get indicative ranges for annual cost savings and potential revenue
- 📑 **Use Case Cards**: Find quick wins and considerations for EV fleets, batteries, HVAC, and manufacturing
- ❓ **FAQ & Glossary**: Plain-English explanations of energy market jargon
- 📧 **Contact Form**: Get help with next steps

### Technical Features

- 🎯 **Multi-Service Compatibility Checker**: Compare multiple services simultaneously
- 📊 **Three Stacking Modes**: Analyze co-delivery, splitting, and jumping compatibility
- 📋 **Service Details**: View technical requirements with user-friendly explanations
- 🔢 **Matrix View**: Visual compatibility matrix for quick reference
- 💡 **Plain-English Throughout**: No energy market expertise required
- ⚙️ **Transparent Assumptions**: All estimator math is visible and editable
- ♿ **Accessible Design**: WCAG 2.2 AA compliant for contrast and keyboard navigation

## Data Source

Based on:
- **ENA Open Networks Revenue Stacking Assessment Tool V1.0** (January 2025)
- **NESO and DSO All Product Technical Requirements** (December 2024)

## Project Structure

```
/
├── app.py                          # Main Streamlit application (V2.0 - tabbed architecture)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── CHANGELOG.md                    # Top-5 UX issues and changes
├── COPY.md                         # Plain-English content deck
├── ASSUMPTIONS.md                  # Estimator methodology and transparency
├── .streamlit/
│   └── config.toml                # Theme (WCAG 2.2 AA compliant)
├── data/
│   ├── stacking_data.json         # Revenue stacking compatibility data
│   ├── leads.csv                  # Lead capture storage
│   └── events_log.csv             # Optional analytics events
├── modules/
│   ├── ui_components.py           # Streamlit UI components (enhanced)
│   └── estimator.py               # NEW - Value Estimator logic and UI
└── utils/
    ├── data_loader.py             # Data loading (@st.cache_data)
    └── descriptions.py            # Service descriptions, glossary, and FAQs
```

## Installation

### Local Development

1. Clone the repository:
```bash
git clone <your-repo-url>
cd streamlit-app
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Deployment on Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository and branch
5. Set main file path to `app.py`
6. Deploy!

## For Entrepreneurs: Quick Start

### I want to understand potential value (5 minutes)

1. **Launch the app** (see Installation below)
2. **Go to "Value Estimator" tab**
3. **Enter your details**:
   - Shiftable capacity (kW)
   - Flexibility hours per day
   - Your electricity tariff (peak/off-peak rates)
4. **Click "Calculate Value"** to see indicative annual savings
5. **Export results** to CSV for your records

**Important**: These are estimates, not guarantees. Actual results depend on your tariff, operations, and eligibility for programs. See `ASSUMPTIONS.md` for full methodology.

### I want to check service compatibility (3 minutes)

1. **Go to "Check Compatibility" tab**
2. **Select 2+ services** you're interested in (or that your aggregator suggested)
3. **View results** for co-delivery, splitting, and jumping
4. **Review technical requirements** to confirm eligibility

### I want to see what's possible for my asset type (2 minutes)

1. **Go to "Use Cases" tab**
2. **Find your asset**: EV Fleet, Battery Storage, HVAC, or Industrial/Manufacturing
3. **Review quick wins and watch-outs**

### I need help or have questions

1. **Go to "FAQ & Glossary" tab** for common questions
2. **Go to "Contact" tab** to get in touch—we'll respond within 2 working days

---

## Usage (Technical)

### Tabbed Architecture

The app is organized into 7 tabs:

1. **Overview**: Value proposition, plain-English intro to flexibility
2. **Check Compatibility**: Multi-service compatibility checker (existing feature, preserved)
3. **Matrix View**: Visual compatibility matrix (existing feature, preserved)
4. **Value Estimator**: NEW - Calculate potential savings and revenue
5. **Use Cases**: Asset-specific guidance (EV, Battery, HVAC, Industrial)
6. **FAQ & Glossary**: Plain-English definitions and common questions
7. **Contact**: Lead capture form

### Basic Workflow (Compatibility Checking)

1. **Select Services**: Use the multi-select dropdown to choose 2 or more services
2. **View Compatibility**: Check results for co-delivery, splitting, and jumping
3. **Explore Details**: Review technical requirements with helpful explanations
4. **Matrix View**: Use the matrix view for a quick overview of all compatibilities

### Understanding Results

#### Compatibility Modes

- **Co-delivery** 🔄: Using the same MW for multiple services at the same time in the same direction
- **Splitting** ✂️: Dividing your asset's capacity between different services at the same time
- **Jumping** ⚡: Switching between services at different times

#### Status Indicators

- ✅ **Explicit Yes**: Services can definitely be stacked
- ❌ **Explicit No**: Services cannot be stacked (explanation provided)
- ❓ **No Data**: Compatibility not yet assessed
- ⚠️ **N/A**: Not applicable (e.g., same service)

## Services Covered

The tool covers 22 UK energy flexibility services:

### National ESO Services
- Capacity Market (CM)
- Wholesale Market (WM)
- Balancing Market (BM)
- Balancing Reserve (BR)
- Quick Reserve (QR)
- Slow Reserve (SR)
- Short Term Operating Reserve (STOR)
- Dynamic Containment (DC)
- Dynamic Moderation (DM)
- Dynamic Regulation (DR)
- Static Firm Frequency Response (SFFR)
- MW Dispatch (MWD)
- Local Constraint Market (LCM)
- Demand Flexibility Service (DFS)

### DNO Services
- Peak load reduction (PR)
- Scheduled Utilisation (SU)
- Operational Utilisation (OU) variants
- Scheduled Availability + Operational Utilisation (SA+OU) variants
- Variable Availability + Operational Utilisation (VA+OU) variants

## Development

### Adding New Features

The modular structure makes it easy to extend:

- **New UI components**: Add to `modules/ui_components.py`
- **New data processing**: Add to `utils/data_loader.py`
- **New service descriptions**: Update `utils/descriptions.py`

### Data Updates

To update the stacking data:

1. Update `data/stacking_data.json` with new compatibility information
2. Update service descriptions in `utils/descriptions.py` if new services are added
3. Update field explanations if new technical requirements are added

## Configuration

### Streamlit Configuration

Create a `.streamlit/config.toml` file for custom configuration:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 10
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This tool is provided for informational purposes. Always verify compatibility and contractual terms with the relevant service operators (NESO, DNOs) before making commercial decisions.

## Support

For questions or issues:
1. Check the in-app help tooltips (ℹ️ icons)
2. Review the official ENA and NESO documentation
3. Open an issue on GitHub

## Value Estimator Details

The **Value Estimator** provides indicative ranges for:

1. **Annual Cost Savings**: From shifting electricity use to cheaper periods (time-of-use arbitrage)
2. **Potential Incentive Revenue** (optional): From participating in flexibility services
3. **CO₂ Savings** (optional): From shifting to lower-carbon periods

### Key Features

- **Transparent assumptions**: All math is visible and editable
- **Range-based outputs**: Low and high estimates to reflect uncertainty
- **No external APIs**: All calculations are client-side (deterministic and fast)
- **CSV export**: Download results with full inputs for your records
- **Clear disclaimers**: "This is an estimate, not advice"

### What's NOT Included in Estimates

- Capital costs (hardware, installation)
- Ongoing management costs
- Efficiency losses (battery round-trip, HVAC rebound)
- Penalties for non-performance
- Tax implications

**Always verify**:
1. Tariff details with your energy supplier
2. Eligibility and technical requirements with NESO/DNO
3. Compatibility with existing contracts
4. Commercial terms before committing

See `ASSUMPTIONS.md` for full methodology and default values.

---

## Important Disclaimers

**Estimates are illustrative and depend on**:
- Your specific tariff, operations, and eligibility for programs
- Verify compatibility and contractual terms with NESO and your DSO before making commercial decisions

**Data currency**:
- Compatibility data reflects rules as of **January 2025**
- Program terms may change—always check with the relevant service operator

**Not financial advice**:
- This tool provides information and estimates to help you explore options
- Consult qualified professionals for detailed business cases and contracts

---

## Acknowledgments

- **ENA Open Networks**: For the Revenue Stacking Assessment Tool V1.0 (January 2025)
- **NESO**: For technical requirements documentation (December 2024)
- **DSOs**: For local flexibility service specifications
- **Streamlit**: For the excellent web framework

---

**Version**: 2.0
**Last Updated**: January 2026
**Data Source**: ENA Open Networks V1.0 (Jan 2025), NESO/DSO Requirements (Dec 2024)
