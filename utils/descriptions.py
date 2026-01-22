"""
Service descriptions and field explanations for user-friendly display
"""

SERVICE_DESCRIPTIONS = {
    "Capacity Market (CM)": "A long-term market where you're paid to guarantee capacity availability during peak demand periods.",
    "Wholesale Market (WM)": "Trading electricity in advance through day-ahead and intraday markets based on supply and demand.",
    "Balancing Market (BM)": "Real-time trading where the ESO adjusts your generation or demand to balance the grid.",
    "Balancing Reserve (BR)": "Providing rapid response reserve capacity to help manage unexpected generation losses.",
    "Quick Reserve (QR)": "Fast-acting reserve that can deliver full power within 2 minutes for grid stability.",
    "Slow Reserve (SR)": "Reserve service with longer response times, currently under development by NESO.",
    "Short Term Operating Reserve (STOR)": "Providing backup power or demand reduction within 20 minutes of instruction.",
    "Dynamic Containment (DC)": "Fastest frequency response service, automatically correcting frequency deviations within 1 second.",
    "Dynamic Moderation (DM)": "Automatic frequency response service reacting within 1 second to moderate frequency changes.",
    "Dynamic Regulation (DR)": "Continuous automatic response to regulate grid frequency within narrow tolerances.",
    "Static Firm Frequency Response (SFFR)": "Traditional frequency response service providing automatic power adjustments.",
    "MW Dispatch (MWD)": "On-demand dispatch service where the ESO requests specific MW changes.",
    "Local Constraint Market (LCM)": "Local flexibility services to resolve network constraints at distribution level.",
    "Demand Flexibility Service (DFS)": "National scheme for reducing electricity demand during peak periods (typically 4-7pm).",
    "Peak load reduction (PR)": "Services to reduce demand during network peak times, helping avoid reinforcement costs.",
    "Scheduled Utilisation (SU)": "Pre-scheduled flexibility services booked in advance with your local distribution network.",
    "Operational Utilisation (OU) (2 & 15 mins)": "Short-notice flexibility services dispatched by DNOs within 2 or 15 minutes.",
    "Operational Utilisation (OU) (week ahead)": "Week-ahead operational flexibility services for distribution network management.",
    "Scheduled Availability + Operational Utilisation (SA+OU) (2 mins)": "Combined service offering availability payments plus rapid 2-minute dispatch.",
    "Scheduled Availability + Operational Utilisation (SA+OU) (day-ahead)": "Day-ahead availability with operational dispatch for distribution network support.",
    "Variable Availability + Operational Utilisation (VA+OU) (2 & 15 mins)": "Flexible availability windows with rapid dispatch capability for DNO services.",
    "Variable Availability + Operational Utilisation (VA+OU) (DA & WA)": "Variable availability combined with day-ahead and week-ahead operational dispatch."
}

FIELD_EXPLANATIONS = {
    "Strategic Direction": "NESO's long-term vision and development plans for this service",
    "Payment structure": "How you get paid - availability fees, utilization fees, or both",
    "Procurement mechanism": "How the service is bought - auction, tender, bilateral contract, etc.",
    "Procurement frequency": "How often procurement windows open (daily, monthly, annually)",
    "Pricing timing": "When prices are set - in advance or after delivery",
    "Contract length": "Duration of your commitment once accepted into the service",
    "Pre-qualification": "Requirements you must meet before you can participate",
    "Minimum capacity": "Smallest MW size that can participate in the service",
    "Maximum capacity": "Largest MW size or no upper limit for participation",
    "Metering requirements": "Type of meter and data collection needed (e.g., half-hourly, second-by-second)",
    "Response time": "How quickly you must deliver full power after receiving instruction",
    "Sustained delivery time": "How long you must maintain your response once activated",
    "Recovery time": "How long before you must be ready to respond again",
    "Availability windows": "When the service operates (24/7, peak hours, seasonal)",
    "Notice period": "How much warning you get before being dispatched",
    "Baseline methodology": "How your normal consumption/generation is calculated for measuring response",
    "Operational direction": "What you're asked to do - increase, decrease, or both",
    "Performance monitoring": "How your delivery is measured and verified",
    "Penalties": "Financial consequences for underdelivery or non-compliance",
    "Availability": "How often you must be ready to provide the service"
}


def get_service_description(service_name):
    """Get user-friendly description for a service"""
    return SERVICE_DESCRIPTIONS.get(service_name, "")


def get_field_explanation(field_name):
    """Get explanation for a technical field with fuzzy matching"""
    # Try exact match first
    if field_name in FIELD_EXPLANATIONS:
        return FIELD_EXPLANATIONS[field_name]

    # Try fuzzy matching for common variations
    lower_field = field_name.lower()
    for key, value in FIELD_EXPLANATIONS.items():
        if lower_field in key.lower() or key.lower() in lower_field:
            return value

    return None
