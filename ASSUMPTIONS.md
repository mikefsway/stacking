# Value Estimator - Assumptions & Methodology

## Purpose

This document explains the methodology, assumptions, and limitations of the Value Estimator tool. All assumptions are transparent and editable by users to reflect their specific circumstances.

---

## Overview

The Value Estimator provides **indicative ranges** for potential cost savings and revenue from energy flexibility. It is designed as a first-pass filter to help entrepreneurs understand order-of-magnitude value, NOT as precise financial advice.

**Key Principle**: Transparency over precision. We show our work, explain limitations, and let users adjust assumptions.

---

## Core Calculations

### 1. Annual Cost Savings

**Formula**:
```
Annual Savings (£) = kWh shifted per day × (Peak rate - Off-peak rate) × Participation rate × 365 days
```

**Where**:
- **kWh shifted per day** = Shiftable capacity (kW) × Flexibility hours per day
- **Peak rate** = User-entered peak tariff rate (p/kWh)
- **Off-peak rate** = User-entered baseline/off-peak rate (p/kWh)
- **Participation rate** = Percentage of days/hours flexibility is actually used (30-80% typical)

**Range**:
- **Low estimate**: Uses minimum participation rate (default: 30%)
- **High estimate**: Uses maximum participation rate (default: 80%)

**Default Values**:
- Peak rate: 35 p/kWh (typical UK commercial peak)
- Off-peak rate: 15 p/kWh (typical UK commercial off-peak)
- Participation rate range: 30% - 80%

**Assumptions**:
1. Simple time-of-use (TOU) tariff structure
2. Consistent peak/off-peak differential
3. No demand charges (add separately if applicable)
4. No additional costs for control/hardware
5. Linear scaling (no diminishing returns)

**Limitations**:
- Real tariffs may have multiple time bands
- Actual participation depends on operations, weather, and constraints
- Does not account for rebound effects or efficiency losses
- Network charges and other tariff components not included

---

### 2. Potential Annual Incentives (Optional)

**Formula**:
```
Annual Incentives (£) = Capacity (kW) × Availability hours × Rate per kW-hour × Participation rate
```

**Where**:
- **Capacity (kW)** = User-entered shiftable capacity
- **Availability hours** = Hours per year asset is available for services (default: 2000-4000)
- **Rate per kW-hour** = Typical incentive rate for relevant services (£/kW/h or £/MWh)
- **Participation rate** = Percentage of availability actually dispatched

**Default Values**:
- Availability: 2000-4000 hours/year
- Typical rates:
  - Demand Flexibility Service (DFS): £1-3 per kWh delivered
  - Dynamic Containment (DC): £15-25 per MW per hour availability
  - Peak Reduction (DNO): £40-80 per kW per year availability
  - (User selects service type to apply relevant rate)

**Assumptions**:
1. User is eligible for selected service(s)
2. Asset meets minimum technical requirements
3. Pre-qualification completed
4. Availability windows align with service requirements
5. Rates based on recent auction/tender results

**Limitations**:
- **Incentives are NOT guaranteed**—availability and rates vary by location and time
- Eligibility requirements (capacity, response time, duration) must be verified
- Services have contracts, lock-in periods, and performance penalties
- Some services are competitive (auction-based)—not all applicants accepted
- Rates shown are historical averages; future rates may differ
- Assumes no conflicts with existing contracts

**Why Optional?**
We hide incentive estimates behind a toggle ("Programs may be available in my area") because:
- Not all assets/locations qualify
- Creates false expectations if shown by default
- Focuses users on certain cost savings first

---

### 3. CO₂ Emissions Savings (Optional)

**Formula**:
```
Annual CO₂ Savings (kg) = kWh shifted × (Peak emission factor - Off-peak emission factor) × 365
```

**Where**:
- **kWh shifted** = (Shiftable capacity × Flexibility hours per day)
- **Peak emission factor** = Carbon intensity during peak hours (kg CO₂/kWh)
- **Off-peak emission factor** = Carbon intensity during off-peak hours (kg CO₂/kWh)

**Default Values**:
- Peak emission factor: 0.25 kg CO₂/kWh (typical UK grid peak)
- Off-peak emission factor: 0.15 kg CO₂/kWh (typical UK grid off-peak with more renewables)
- Differential: 0.10 kg CO₂/kWh

**Assumptions**:
1. Average UK grid carbon intensity by time of day
2. Off-peak periods have higher renewable penetration
3. Avoided emissions (not absolute emissions reduction)
4. No lifecycle emissions from enabling technology

**Limitations**:
- Grid carbon intensity varies by location, season, and weather
- Does not account for embedded generation or private wire arrangements
- Simplified two-band model (real grid varies continuously)
- Scope 2 emissions only (operational, not embodied)

---

## Input Parameters

### Required Inputs

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| **Asset Type** | None | Multi-select from 22 services | Maps to relevant flexibility services |
| **Shiftable Capacity (kW)** | 100 | 1 - 10,000 | Maximum power that can be shifted |
| **Flexibility Hours/Day** | 4 | 0.5 - 24 | Hours per day available for shifting |
| **Flexibility Window** | 22:00 - 06:00 | Any | Earliest start / latest finish times |
| **Baseline Tariff (p/kWh)** | 15 | 5 - 50 | Off-peak or average electricity rate |
| **Peak Rate (p/kWh)** | 35 | 10 - 80 | Peak electricity rate |

### Optional Inputs

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| **Participation Rate Low (%)** | 30 | 10 - 100 | Minimum realistic usage of flexibility |
| **Participation Rate High (%)** | 80 | 10 - 100 | Maximum realistic usage of flexibility |
| **Programs Available?** | Off | Toggle | Show potential incentives from services |
| **Peak Emission Factor (kg/kWh)** | 0.25 | 0.1 - 0.5 | Carbon intensity at peak |
| **Off-peak Emission Factor (kg/kWh)** | 0.15 | 0.05 - 0.3 | Carbon intensity off-peak |

---

## Asset Type Mapping

The estimator uses the 22 services from the compatibility tool to help users identify relevant programs:

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

Users select relevant services → estimator suggests typical rates → compatibility checker shows stacking options.

---

## Constraints & Filters

Users can specify operational constraints:

| Constraint | Purpose |
|------------|---------|
| **Comfort Window** | For HVAC: acceptable temperature range |
| **Minimum State of Charge (SOC)** | For batteries: always keep X% charge |
| **Duty Cycle** | For EVs: must be charged by Y time |
| **Production Schedule** | For manufacturing: non-flexible hours |

These constraints are **shown but not enforced in calculation**—they serve as reminders for users to consider when interpreting results.

---

## Output Presentation

### Ranges, Not Point Estimates

All outputs are shown as ranges to reflect uncertainty:

**Annual Cost Savings**: £1,200 - £3,200
- Low: Conservative participation, fewer hours
- High: Optimistic participation, more hours

**Potential Incentives** (if toggled): £800 - £2,400
- Low: Lower availability, lower rates
- High: Higher availability, higher rates

### Sensitivity Analysis (Optional Feature)

Simple sensitivity chart showing impact of:
- Participation rate (±20%)
- Peak/off-peak differential (±5 p/kWh)
- Capacity (±20%)

Helps users understand which assumptions matter most.

---

## Disclaimers

### Shown in UI

**This is an estimate, not advice.**
Actual savings and revenue depend on:
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

### Not Included in Estimates

- Capital costs (hardware, control systems)
- Installation and commissioning costs
- Ongoing management and monitoring costs
- Efficiency losses (battery round-trip, HVAC rebound)
- Network charges or balancing costs
- Tax implications
- Penalties for non-performance

---

## Validation & Calibration

### Methodology Validation

Calculations reviewed against:
- ENA Open Networks Revenue Stacking Tool V1.0 (Jan 2025)
- NESO technical requirements (Dec 2024)
- Industry case studies and typical results

### Rate Calibration

Default rates updated quarterly based on:
- NESO auction results (DC, DM, DR)
- DNO flexibility tender outcomes
- Wholesale market averages (day-ahead, intraday)
- Retail tariff surveys

### User Feedback Loop

Users encouraged to:
- Report inaccurate assumptions
- Share actual results vs estimates (anonymized)
- Suggest missing cost/benefit factors

---

## Updates & Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-22 | Initial release with core calculations |

**Next planned updates**:
- Add demand charge calculations
- Include regional rate variations
- Add battery degradation cost model
- Include stacking complexity penalty (reduced participation when combining services)

---

## Technical Implementation

### Calculation Functions

Estimator logic implemented in `modules/estimator.py`:
- `calculate_cost_savings()` - Simple TOU arbitrage
- `calculate_incentives()` - Service-specific revenue
- `calculate_co2_savings()` - Emissions avoided
- `generate_sensitivity_chart()` - Parameter impact

All functions are **pure Python** (no external APIs) for deterministic, testable results.

### Caching

Calculations are fast (<100ms) and do not require caching. Data inputs stored in `st.session_state` for persistence within session.

### Export Format

CSV export includes:
- All inputs (for reproducibility)
- All outputs (low/high ranges)
- Timestamp and version
- Editable "Notes" field for user context

---

## Ethical Considerations

### Avoiding Over-Promising

- Show ranges, not guarantees
- Hide incentives by default
- Prominent disclaimers
- Link to official sources (NESO, DNO websites)

### Inclusive Design

- All assumptions editable (works for different asset types, tariffs, locations)
- Plain-English labels
- Help text for every parameter
- No hidden costs or "gotchas"

### Privacy

- No personal data required
- All calculations client-side
- No tracking of financial estimates

---

**Document Version**: 1.0
**Last Updated**: 2026-01-22
**Maintained By**: Development Team
**Review Frequency**: Quarterly (or when NESO/DNO rules change)
