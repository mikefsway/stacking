# Project Structure

```
streamlit-app/
│
├── 📄 app.py                          # Main Streamlit application (entry point)
├── 📄 requirements.txt                # Python dependencies for deployment
├── 📄 .gitignore                     # Git ignore rules
│
├── 📁 .streamlit/
│   └── 📄 config.toml                # Streamlit configuration (theme, server settings)
│
├── 📁 data/
│   └── 📄 stacking_data.json        # Revenue stacking compatibility dataset (256KB)
│
├── 📁 modules/
│   ├── 📄 __init__.py               # Package marker
│   └── 📄 ui_components.py          # Reusable Streamlit UI components
│
├── 📁 utils/
│   ├── 📄 __init__.py               # Package marker
│   ├── 📄 data_loader.py            # Data loading and processing utilities
│   └── 📄 descriptions.py           # Service descriptions and field explanations
│
└── 📁 docs/ (documentation)
    ├── 📄 README.md                  # Main project documentation
    ├── 📄 DEPLOYMENT_GUIDE.md       # Streamlit Cloud deployment instructions
    ├── 📄 PROJECT_SUMMARY.md        # Technical project overview
    └── 📄 STRUCTURE.md              # This file
```

## File Descriptions

### Core Application Files

#### `app.py` (87 lines)
Main entry point for the Streamlit application.
- Page configuration and styling
- Data loading with caching
- Main UI layout (columns, tabs)
- Integration of all components
- Footer and metadata display

**Key Functions:**
- `load_data()` - Cached data loading
- `main()` - Main application logic

---

#### `requirements.txt`
Python package dependencies for deployment.
```
streamlit>=1.31.0
pandas>=2.0.0
```

---

### Configuration Files

#### `.streamlit/config.toml`
Streamlit configuration for theme and server settings.
- Custom color scheme (purple gradient theme)
- Server configuration (headless mode, port)
- Browser settings (disable analytics)

---

#### `.gitignore`
Standard Python and Streamlit ignore rules.
- Python cache and build files
- Virtual environments
- IDE configurations
- OS-specific files
- Streamlit secrets

---

### Data Files

#### `data/stacking_data.json` (256KB)
Complete revenue stacking compatibility dataset.

**Structure:**
```json
{
  "metadata": {...},
  "services": [...],
  "service_abbreviations": {...},
  "compatibility": {
    "codelivery": {...},
    "splitting": {...},
    "jumping": {...}
  },
  "technical_requirements": {...},
  "service_name_mapping": {...}
}
```

**Contains:**
- 22 UK energy flexibility services
- Compatibility matrices (3 modes)
- Technical requirements for each service
- Service abbreviations and mappings

---

### Module Files

#### `modules/ui_components.py` (280+ lines)
Reusable Streamlit UI components.

**Functions:**
- `render_header()` - App title and description
- `render_service_selector()` - Multi-select dropdown
- `render_compatibility_badge()` - Status emoji (✅❌❓⚠️)
- `render_compatibility_results()` - Service pair compatibility
- `render_multi_service_compatibility()` - Multiple pairs
- `render_service_details()` - Technical requirements with tooltips
- `render_asset_specifications()` - Optional asset input form
- `render_compatibility_matrix()` - Visual matrix table
- `render_sidebar_info()` - Help and about sidebar

**Features:**
- Consistent styling across components
- Helpful tooltips and explanations
- Responsive layout
- Accessibility considerations

---

### Utility Files

#### `utils/data_loader.py` (110+ lines)
Data loading and processing logic.

**Class: `StackingDataLoader`**

Methods:
- `load_data()` - Load JSON file
- `get_services()` - Get service list
- `get_service_abbreviations()` - Get abbreviation mapping
- `get_compatibility()` - Check service pair compatibility
- `get_technical_requirements()` - Get service specifications
- `check_multi_compatibility()` - Check multiple service pairs
- `get_metadata()` - Get dataset metadata

**Features:**
- Lazy loading (loads data only when needed)
- Service name mapping
- Type hints for clarity
- Error handling

---

#### `utils/descriptions.py` (90+ lines)
User-friendly content and explanations.

**Constants:**
- `SERVICE_DESCRIPTIONS` - 22 plain English service descriptions
- `FIELD_EXPLANATIONS` - 21 technical field explanations

**Functions:**
- `get_service_description()` - Get description for a service
- `get_field_explanation()` - Get explanation with fuzzy matching

**Example Descriptions:**
```python
"Dynamic Containment (DC)": "Fastest frequency response service,
automatically correcting frequency deviations within 1 second."

"Response time": "How quickly you must deliver full power
after receiving instruction"
```

---

### Documentation Files

#### `README.md` (5.5KB)
Main project documentation.

**Sections:**
- Overview and features
- Data source information
- Project structure
- Installation instructions (local and cloud)
- Usage guide
- Services covered
- Development guide
- Configuration options
- Support resources

**Target Audience:** End users and developers

---

#### `DEPLOYMENT_GUIDE.md` (6.8KB)
Comprehensive deployment instructions.

**Sections:**
- Quick deployment steps
- Repository setup
- Streamlit Cloud deployment
- Pre-deployment checklist
- Post-deployment testing
- Custom domain setup
- Troubleshooting guide
- Performance optimization
- Security best practices
- Maintenance schedule

**Target Audience:** Deployment engineers and maintainers

---

#### `PROJECT_SUMMARY.md` (8.4KB)
Technical overview and project analysis.

**Sections:**
- File structure
- Modular architecture breakdown
- Key features
- HTML vs Streamlit comparison
- Technology stack
- Deployment options
- Next steps for development
- Performance characteristics
- Testing recommendations
- Success metrics

**Target Audience:** Project managers and technical leads

---

## File Statistics

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | 87 | Main application |
| `modules/ui_components.py` | 280+ | UI components |
| `utils/data_loader.py` | 110+ | Data processing |
| `utils/descriptions.py` | 90+ | User content |
| **Total Python Code** | **570+** | |
| `data/stacking_data.json` | 1 | Data file (256KB) |
| Documentation | 4 files | ~20KB markdown |

## Import Dependencies

```python
# Standard Library
from pathlib import Path
from typing import Dict, List, Optional
import json

# Third-Party
import streamlit as st
import pandas as pd  # (only for matrix display)
```

**Minimal dependencies = Fast deployment!**

## Data Flow

```
1. User opens app
   ↓
2. app.py loads
   ↓
3. StackingDataLoader.load_data()
   ↓
4. data/stacking_data.json → Cached in memory
   ↓
5. User selects services
   ↓
6. app.py calls ui_components functions
   ↓
7. ui_components query data_loader
   ↓
8. Results displayed with descriptions from descriptions.py
```

## State Management

Streamlit uses automatic state management:
- Session state for user selections
- `@st.cache_resource` for data loading
- Widget keys for form state

No manual state management needed!

## Extension Points

To add new features:

1. **New UI component**: Add function to `modules/ui_components.py`
2. **New data processing**: Add method to `utils/data_loader.py`
3. **New service info**: Update `utils/descriptions.py`
4. **New data**: Update `data/stacking_data.json`
5. **New page/tab**: Add tab in `app.py`

## Testing Strategy

### Manual Testing
Run locally:
```bash
streamlit run app.py
```

### Unit Testing (Future)
```bash
pytest tests/
```

Recommended test structure:
```
tests/
├── test_data_loader.py
├── test_descriptions.py
└── test_ui_components.py
```

## Version Control

**Current Version**: 1.0

**Versioning Strategy**: Semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## File Size Summary

| Category | Size |
|----------|------|
| Python code | ~25KB |
| Data file | 256KB |
| Documentation | ~20KB |
| Configuration | <1KB |
| **Total** | **~300KB** |

Lightweight and fast to deploy! 🚀

---

**Last Updated**: January 2025
**Status**: Production Ready ✅
