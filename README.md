# UK Energy Revenue Stacking Explorer

A Streamlit web application for analyzing compatibility between UK energy flexibility services and optimizing revenue stacking opportunities.

## Overview

This tool helps energy asset owners and operators understand which flexibility services can be stacked together (co-delivery, splitting, or jumping) to maximize revenue opportunities while maintaining compliance with NESO and DSO requirements.

## Features

- 🎯 **Multi-Service Compatibility Checker**: Compare multiple services simultaneously
- 📊 **Three Stacking Modes**: Analyze co-delivery, splitting, and jumping compatibility
- 📋 **Service Details**: View technical requirements with user-friendly explanations
- 🔢 **Matrix View**: Visual compatibility matrix for quick reference
- 💡 **User-Friendly**: Plain English descriptions and helpful tooltips
- ⚙️ **Asset Specifications**: Optional input for personalized recommendations

## Data Source

Based on:
- **ENA Open Networks Revenue Stacking Assessment Tool V1.0** (January 2025)
- **NESO and DSO All Product Technical Requirements** (December 2024)

## Project Structure

```
streamlit-app/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/
│   └── stacking_data.json         # Revenue stacking compatibility data
├── modules/
│   └── ui_components.py           # Streamlit UI components
└── utils/
    ├── data_loader.py             # Data loading and processing
    └── descriptions.py            # Service descriptions and tooltips
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

## Usage

### Basic Workflow

1. **Select Services**: Use the multi-select dropdown to choose 2 or more services
2. **View Compatibility**: Check the compatibility results tab to see if services can be stacked
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

## Acknowledgments

- **ENA Open Networks**: For the Revenue Stacking Assessment Tool
- **NESO**: For technical requirements documentation
- **Streamlit**: For the excellent web framework

---

**Version**: 1.0
**Last Updated**: January 2025
**Data Source**: ENA Open Networks V1.0 (Jan 2025)
