# CLAUDE.MD - AI Assistant Context

## Project Overview

**UK Energy Revenue Stacking Explorer** - A Streamlit web application for analyzing compatibility between UK energy flexibility services and optimizing revenue stacking opportunities.

**Purpose**: Help energy asset owners and operators understand which flexibility services can be stacked together (co-delivery, splitting, or jumping) to maximize revenue while maintaining compliance with NESO and DSO requirements.

**Data Source**: ENA Open Networks Revenue Stacking Assessment Tool V1.0 (January 2025) and NESO and DSO All Product Technical Requirements (December 2024).

---

## Architecture Overview

### Application Type
- **Framework**: Streamlit (Python web framework)
- **Architecture**: Modular MVC-style pattern
- **Deployment**: Streamlit Cloud (primary), self-hosted (optional)
- **Data Storage**: Static JSON file (256KB)

### Core Components

```
app.py                      # Main application entry point
├── modules/
│   └── ui_components.py    # Reusable Streamlit UI components
├── utils/
│   ├── data_loader.py      # Data loading and processing
│   └── descriptions.py     # User-friendly content and tooltips
└── data/
    └── stacking_data.json  # Compatibility dataset
```

### Data Flow

1. User opens app → `app.py` loads
2. `@st.cache_resource` loads data via `StackingDataLoader`
3. User selects services via UI components
4. Components query `StackingDataLoader` for compatibility
5. Results displayed with descriptions from `descriptions.py`

---

## Key Files and Their Roles

### `app.py` (87 lines)
- **Purpose**: Main application entry point
- **Responsibilities**:
  - Page configuration and theme
  - Data loading with caching
  - Main UI layout (tabs, columns)
  - Component integration
- **Key Functions**:
  - `load_data()` - Cached data loader using `@st.cache_resource`
  - `main()` - Main application logic
- **Pattern**: Keep this file minimal, delegate to modules

### `modules/ui_components.py` (280+ lines)
- **Purpose**: Reusable Streamlit UI components
- **Key Functions**:
  - `render_header()` - App title and intro
  - `render_service_selector()` - Multi-select dropdown
  - `render_compatibility_badge()` - Status indicators (✅❌❓⚠️)
  - `render_compatibility_results()` - Single pair compatibility
  - `render_multi_service_compatibility()` - Multiple pairs
  - `render_service_details()` - Technical requirements with tooltips
  - `render_asset_specifications()` - Optional asset input
  - `render_compatibility_matrix()` - Pandas DataFrame matrix
  - `render_sidebar_info()` - Help and about section
- **Pattern**: Each function is self-contained, accepts data_loader

### `utils/data_loader.py` (110+ lines)
- **Purpose**: Data access layer
- **Class**: `StackingDataLoader`
- **Key Methods**:
  - `load_data(file_path)` - Load JSON data
  - `get_services()` - List all services
  - `get_compatibility(service1, service2, mode)` - Check compatibility
  - `get_technical_requirements(service)` - Get service specs
  - `check_multi_compatibility(services, mode)` - Batch checking
- **Pattern**: Lazy loading, caching encouraged at app level

### `utils/descriptions.py` (90+ lines)
- **Purpose**: User-friendly content
- **Constants**:
  - `SERVICE_DESCRIPTIONS` - Plain English service explanations (22 services)
  - `FIELD_EXPLANATIONS` - Technical field explanations (21 fields)
- **Functions**:
  - `get_service_description(service)` - Get service description
  - `get_field_explanation(field)` - Get field explanation with fuzzy matching
- **Pattern**: Centralized content makes updates easy

### `data/stacking_data.json` (256KB)
- **Purpose**: Complete compatibility dataset
- **Structure**:
  ```json
  {
    "metadata": {...},
    "services": ["CM", "WM", "BM", ...],
    "service_abbreviations": {"CM": "Capacity Market", ...},
    "compatibility": {
      "codelivery": {"CM": {"WM": "yes", ...}},
      "splitting": {...},
      "jumping": {...}
    },
    "technical_requirements": {
      "CM": {"Contract length": "15 years", ...}
    },
    "service_name_mapping": {...}
  }
  ```

---

## Development Guidelines

### Code Style

1. **Streamlit Best Practices**:
   - Use `@st.cache_resource` for data loading
   - Use `@st.cache_data` for data transformations
   - Keep widget keys unique and descriptive
   - Use session state sparingly (Streamlit handles most state)

2. **Component Design**:
   - Each UI function should be self-contained
   - Pass `data_loader` instance as parameter
   - Return values only when needed by parent
   - Use clear, descriptive function names

3. **Data Access**:
   - Always access data through `StackingDataLoader`
   - Never directly read JSON in components
   - Handle missing data gracefully

4. **User Experience**:
   - Use clear status indicators: ✅ ❌ ❓ ⚠️
   - Provide tooltips for technical terms
   - Keep language simple and jargon-free
   - Display helpful error messages

### Naming Conventions

- **Functions**: `snake_case` (Python standard)
- **Classes**: `PascalCase` (e.g., `StackingDataLoader`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `SERVICE_DESCRIPTIONS`)
- **Streamlit widgets**: Use `key="descriptive_name"` for state persistence

### Adding New Features

#### New UI Component
1. Add function to `modules/ui_components.py`
2. Follow existing pattern: `render_[component_name](data_loader, ...)`
3. Use Streamlit's built-in components when possible
4. Document parameters and return values

#### New Data Processing
1. Add method to `StackingDataLoader` class
2. Keep methods focused (single responsibility)
3. Add type hints
4. Handle edge cases (missing data, invalid input)

#### New Service or Field
1. Update `data/stacking_data.json`
2. Add description to `utils/descriptions.py`
3. Test all compatibility modes
4. Update documentation

---

## Data Structure Details

### Compatibility Modes

1. **Co-delivery** (`"codelivery"`): Using the same MW for multiple services simultaneously in the same direction
2. **Splitting** (`"splitting"`): Dividing asset capacity between different services simultaneously
3. **Jumping** (`"jumping"`): Switching between services at different times

### Compatibility Values

- `"yes"` - Explicitly compatible
- `"no"` - Explicitly incompatible (usually with explanation)
- `null` or missing - No data available
- `"N/A"` - Not applicable (e.g., same service)

### Service Categories

- **NESO Services**: CM, WM, BM, BR, QR, SR, STOR, DC, DM, DR, SFFR, MWD, LCM, DFS
- **DNO Services**: PR, SU, various OU/SA+OU/VA+OU variants

### Technical Requirement Fields

Common fields: Contract length, Response time, Minimum capacity, Minimum duration, Availability windows, etc. (21 fields total)

---

## Common Tasks and Workflows

### Testing Locally

```bash
cd /home/user/stacking
pip install -r requirements.txt
streamlit run app.py
```

### Adding a New Service

1. Update `data/stacking_data.json`:
   ```json
   "services": [..., "NEW_SERVICE"],
   "service_abbreviations": {"NEW_SERVICE": "Full Name"},
   "compatibility": {
     "codelivery": {"NEW_SERVICE": {...}},
     "splitting": {"NEW_SERVICE": {...}},
     "jumping": {"NEW_SERVICE": {...}}
   },
   "technical_requirements": {"NEW_SERVICE": {...}}
   ```

2. Add description to `utils/descriptions.py`:
   ```python
   SERVICE_DESCRIPTIONS = {
       ...
       "NEW_SERVICE": "Plain English description here"
   }
   ```

3. Test all views (compatibility checker, matrix, details)

### Updating Compatibility Data

1. Edit `data/stacking_data.json`
2. Ensure symmetry in compatibility matrices (if A→B is "yes", B→A should be too)
3. Test affected service pairs
4. Update metadata version/date if significant

### Debugging Tips

1. **Data not loading**: Check JSON syntax, file path
2. **Compatibility not showing**: Verify service names match exactly (case-sensitive)
3. **Tooltips missing**: Check `descriptions.py` has entry for field
4. **Matrix errors**: Ensure pandas is installed, check for null values

---

## Important Patterns and Conventions

### Caching Pattern

```python
@st.cache_resource
def load_data():
    loader = StackingDataLoader()
    loader.load_data("data/stacking_data.json")
    return loader
```

- Use `@st.cache_resource` for objects (StackingDataLoader)
- Use `@st.cache_data` for data transformations
- Cache at app.py level, not in components

### Component Pattern

```python
def render_component(data_loader: StackingDataLoader, param1: str, ...):
    """
    Component description.

    Args:
        data_loader: Instance of StackingDataLoader
        param1: Description
    """
    # Component logic here
    st.markdown("Content")
```

### Error Handling

```python
# Graceful degradation
description = get_service_description(service)
if not description:
    description = f"No description available for {service}"
```

### Responsive Layout

```python
# Use columns for responsive design
col1, col2 = st.columns(2)
with col1:
    # Left content
with col2:
    # Right content
```

---

## Testing Approach

### Manual Testing Checklist

- [ ] Select 2-3 services and verify compatibility results
- [ ] Check all three modes (co-delivery, splitting, jumping)
- [ ] View service details with tooltips
- [ ] Test matrix view with all services
- [ ] Verify responsive design on narrow screens
- [ ] Check sidebar help content
- [ ] Test asset specifications form

### Automated Testing (Future)

Recommended structure:
```
tests/
├── test_data_loader.py      # Unit tests for StackingDataLoader
├── test_descriptions.py     # Test description lookups
└── test_ui_components.py    # Integration tests (pytest-streamlit)
```

---

## Deployment Information

### Current Deployment

- **Platform**: Streamlit Cloud (free tier)
- **Branch**: Deploy from `main` or `master`
- **Entry Point**: `app.py`
- **Python Version**: 3.9+

### Deployment Workflow

1. Make changes locally
2. Test with `streamlit run app.py`
3. Commit to git
4. Push to GitHub
5. Streamlit Cloud auto-deploys (if connected)

### Environment Variables

Currently none required. If secrets needed:
- Add to `.streamlit/secrets.toml` (local)
- Add via Streamlit Cloud dashboard (production)

---

## Performance Considerations

### Current Performance

- **Load Time**: < 2 seconds (with caching)
- **Data Size**: 256KB JSON
- **Concurrent Users**: Supports hundreds (free tier)
- **Response Time**: < 100ms for queries

### Optimization Tips

1. Keep `stacking_data.json` < 1MB
2. Use `@st.cache_resource` for all data loading
3. Lazy load large components (matrix view)
4. Minimize re-renders by using widget keys

---

## Common Issues and Solutions

### Issue: "ModuleNotFoundError"
**Solution**: Install requirements: `pip install -r requirements.txt`

### Issue: JSON parsing error
**Solution**: Validate JSON syntax at jsonlint.com, check for trailing commas

### Issue: Compatibility not displaying
**Solution**: Check exact service name spelling (case-sensitive), verify data exists in JSON

### Issue: Tooltips missing
**Solution**: Add field explanation to `FIELD_EXPLANATIONS` in `descriptions.py`

### Issue: Matrix display error
**Solution**: Ensure all services have entries in compatibility matrices (no missing keys)

---

## Code Quality Standards

### Required

- [ ] Type hints for function parameters
- [ ] Docstrings for public functions
- [ ] Error handling for data access
- [ ] Consistent use of status indicators

### Recommended

- [ ] Comments for complex logic
- [ ] Clear variable names
- [ ] DRY principle (Don't Repeat Yourself)
- [ ] Single Responsibility Principle

### Avoid

- ❌ Hardcoded data (use JSON file)
- ❌ Direct file access in components (use data_loader)
- ❌ Inconsistent terminology
- ❌ Magic numbers (use named constants)

---

## Future Enhancement Areas

### High Priority
- Export functionality (PDF/CSV reports)
- Revenue estimation calculator
- Search functionality for services

### Medium Priority
- Historical compatibility data
- User authentication for saved preferences
- API for programmatic access

### Low Priority
- Database backend (replace JSON)
- Admin panel for data updates
- Service comparison charts

---

## Security Considerations

- **Input Validation**: Service names from user input are validated against known services
- **No Secrets**: Currently no API keys or secrets required
- **Data Privacy**: No user data collected or stored
- **XSS Protection**: Streamlit handles output escaping automatically

---

## Maintenance Schedule

- **Weekly**: Monitor Streamlit Cloud logs for errors
- **Monthly**: Check for Streamlit version updates
- **Quarterly**: Update `stacking_data.json` with latest rules from ENA/NESO
- **Annually**: Review all service descriptions for accuracy

---

## Quick Reference

### File Paths
- Data: `data/stacking_data.json`
- Main app: `app.py`
- UI components: `modules/ui_components.py`
- Data loader: `utils/data_loader.py`
- Descriptions: `utils/descriptions.py`

### Key Classes
- `StackingDataLoader` - Data access layer

### Key Constants
- `SERVICE_DESCRIPTIONS` - Service explanations
- `FIELD_EXPLANATIONS` - Technical field explanations

### Status Indicators
- ✅ "Explicit Yes"
- ❌ "Explicit No"
- ❓ "No Data"
- ⚠️ "N/A"

---

## Contact and Support

For issues or questions:
1. Check in-app help tooltips
2. Review official ENA and NESO documentation
3. Open GitHub issue
4. Check Streamlit documentation: docs.streamlit.io

---

**Document Version**: 1.0
**Last Updated**: January 2025
**Maintained By**: Project Team
**For**: AI Assistants (Claude, etc.)

---

## Tips for AI Assistants

When working on this codebase:

1. **Always read before editing**: Use Read tool on files before making changes
2. **Maintain modularity**: Keep concerns separated (UI, data, content)
3. **Follow patterns**: Match existing code style and structure
4. **Test locally**: Suggest testing with `streamlit run app.py`
5. **Update documentation**: If changing functionality, update relevant .md files
6. **Preserve data integrity**: Be careful with `stacking_data.json` - validate JSON
7. **User-first**: Prioritize clear, simple language over technical jargon
8. **Performance**: Keep caching in mind, avoid expensive operations in render loops

### Before Making Changes

1. Understand the user's request fully
2. Read relevant files
3. Identify affected components
4. Plan changes (use TodoWrite if complex)
5. Make changes following existing patterns
6. Suggest testing approach

### When Stuck

1. Check `STRUCTURE.md` for file organization
2. Check `PROJECT_SUMMARY.md` for architecture
3. Check `DEPLOYMENT_GUIDE.md` for deployment issues
4. Read the actual code - it's well-structured and commented
