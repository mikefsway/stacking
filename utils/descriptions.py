"""
Service descriptions, field explanations, glossary, and FAQs for user-friendly display
"""

# ============================================================================
# SERVICE DESCRIPTIONS (Plain-English)
# ============================================================================

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


# ============================================================================
# GLOSSARY (Plain-English Definitions)
# ============================================================================

GLOSSARY = {
    "Energy Flexibility": {
        "definition": "The ability to shift or shape when you use electricity—charging, discharging, or reducing load at specific times.",
        "example": "Delaying EV charging until nighttime when electricity is cheaper and the grid is cleaner."
    },
    "Time-of-Use (TOU) Tariff": {
        "definition": "Electricity pricing that varies by time of day—typically cheaper at night, more expensive at peak times (e.g., 4-7pm).",
        "example": "A tariff charging 15p/kWh overnight but 35p/kWh during the evening peak."
    },
    "Peak Shaving": {
        "definition": "Reducing your maximum power demand during peak periods to lower demand charges and avoid grid stress.",
        "example": "Precooling a building before 4pm to avoid running AC during the expensive peak period."
    },
    "Demand Response": {
        "definition": "Adjusting electricity use in response to grid signals or price changes—often rewarded with payments or lower bills.",
        "example": "Turning down industrial processes when the grid operator sends a high-price signal."
    },
    "Ancillary Services": {
        "definition": "Services that help keep the grid stable—frequency response, voltage control, reserve capacity. Provided to NESO.",
        "example": "A battery automatically injecting power within 1 second when grid frequency drops below 50 Hz."
    },
    "Baseline": {
        "definition": "Your estimated 'normal' electricity use without flexibility actions—used to measure how much you've shifted or reduced.",
        "example": "If your baseline is 100 kW and you reduce to 80 kW, you've provided 20 kW of demand reduction."
    },
    "Flexibility Window": {
        "definition": "The time range when you're willing or able to shift your electricity use.",
        "example": "EV charging allowed between 10pm-6am (but not during the day when vehicles are in use)."
    },
    "Virtual Power Plant (VPP)": {
        "definition": "A network of distributed energy assets (batteries, EVs, generators) coordinated as a single flexible resource.",
        "example": "An aggregator combining 500 home batteries to act as a 5 MW grid-balancing asset."
    },
    "Co-Delivery": {
        "definition": "Using the same capacity (MW) for multiple services at the same time in the same direction.",
        "example": "Providing frequency response while in a capacity market contract—both services count the same MW."
    },
    "Splitting": {
        "definition": "Dividing your asset's capacity between different services at the same time.",
        "example": "A 5 MW battery split into 3 MW for one service and 2 MW for another service simultaneously."
    },
    "Jumping": {
        "definition": "Switching the same asset between different services at different times.",
        "example": "Providing peak reduction during the day, then switching to frequency response at night."
    },
    "NESO (National Energy System Operator)": {
        "definition": "The organization responsible for balancing electricity supply and demand across Great Britain's transmission system (formerly National Grid ESO).",
        "example": "NESO runs services like Dynamic Containment and Balancing Reserve."
    },
    "DNO (Distribution Network Operator)": {
        "definition": "Regional companies managing local electricity networks. They run local flexibility services.",
        "example": "UK Power Networks, Northern Powergrid, Scottish Power Energy Networks."
    },
    "Capacity Market (CM)": {
        "definition": "A long-term market where you're paid to guarantee capacity availability during peak demand periods.",
        "example": "Agreeing to have your backup generator ready for dispatch during winter stress events."
    },
    "Dynamic Containment (DC)": {
        "definition": "The fastest frequency response service—automatically corrects frequency deviations within 1 second using batteries or other fast assets.",
        "example": "A battery providing immediate frequency support when a power plant trips offline."
    },
    "Demand Flexibility Service (DFS)": {
        "definition": "National scheme for reducing electricity demand during peak periods (typically 4-7pm)—available to households and businesses.",
        "example": "Businesses reducing consumption during a 'saving session' and earning payments per kWh saved."
    },
    "Stacking": {
        "definition": "Combining multiple flexibility services to maximize value—either at the same time or at different times.",
        "example": "Using co-delivery to provide both Capacity Market and frequency response simultaneously."
    },
}


# ============================================================================
# FAQs (Frequently Asked Questions)
# ============================================================================

FAQS = {
    "Will this disrupt my operations?": {
        "answer": "No. We prioritize your constraints first—comfort windows, production schedules, duty cycles. "
                 "Flexibility programs are designed to work around your core needs. You maintain full control and can "
                 "set limits on when and how much flexibility you provide.",
        "category": "General"
    },
    "Do I need new hardware?": {
        "answer": "Often no. Many businesses can start with simple scheduling and policy changes using existing systems. "
                 "Advanced control and automation can be added later if the business case justifies it. "
                 "Some services (like Dynamic Containment) require specific metering and response capabilities.",
        "category": "Technical"
    },
    "Is this allowed in my area?": {
        "answer": "Flexibility options vary by location and network operator. This tool shows general pathways and "
                 "compatibility based on national rules. Always verify program availability and eligibility with "
                 "NESO (for national services) and your local DNO (for local services).",
        "category": "Eligibility"
    },
    "How accurate is the Value Estimator?": {
        "answer": "It provides indicative ranges using transparent, editable assumptions. Actual results depend on your "
                 "specific tariff, operational patterns, and program participation. Treat it as a first-pass filter "
                 "to understand order-of-magnitude value, not a guarantee. Always get detailed quotes and professional advice "
                 "before making commercial decisions.",
        "category": "Value Estimator"
    },
    "What's the difference between NESO and DNO services?": {
        "answer": "NESO (National Energy System Operator) runs national-level services for grid balancing across Great Britain—"
                 "like frequency response and capacity markets. DNOs (Distribution Network Operators) are regional companies "
                 "running local services for network management—like peak reduction and local constraints. Some assets can "
                 "participate in both, which is where 'stacking' becomes valuable.",
        "category": "General"
    },
    "What does 'stacking' mean?": {
        "answer": "Stacking means combining multiple flexibility services to maximize value. There are three ways to stack: "
                 "(1) Co-delivery: using the same capacity for different services at the same time; "
                 "(2) Splitting: dividing capacity between services at the same time; "
                 "(3) Jumping: switching between services at different times. This tool helps you understand which combinations are allowed.",
        "category": "General"
    },
    "Are there penalties for non-delivery?": {
        "answer": "Yes, most services have performance requirements and penalties for under-delivery. These vary by service and are "
                 "specified in the contract terms. Some services are quite strict (Dynamic Containment), while others are more "
                 "forgiving (Demand Flexibility Service). Always review contract terms carefully before committing.",
        "category": "Contracts"
    },
    "How do I get started?": {
        "answer": "1. Use the Value Estimator to understand potential value\n"
                 "2. Check compatibility of relevant services for your asset type\n"
                 "3. Review technical requirements to confirm eligibility\n"
                 "4. Contact us (via Contact tab) or the relevant service operator (NESO/DNO) for next steps\n"
                 "5. Consider working with an aggregator if you don't want to manage services directly",
        "category": "Getting Started"
    },
    "What is a baseline and why does it matter?": {
        "answer": "A baseline is your estimated 'normal' electricity use without flexibility actions. It's used to measure how much "
                 "you've reduced or shifted. Different services use different baseline methodologies—some use your average consumption, "
                 "others use similar days, and some use weather-adjusted models. Getting the baseline right is crucial because your "
                 "payment is often based on the difference between your baseline and actual consumption.",
        "category": "Technical"
    },
    "Can I participate if I'm a small business?": {
        "answer": "Yes! Many services now accept smaller capacities, especially when aggregated. For example, Demand Flexibility Service "
                 "(DFS) is open to all sizes. Some DNO services accept capacities as low as 1 kW when aggregated. However, services like "
                 "Dynamic Containment typically require minimum capacities (1 MW+). Consider working with an aggregator who can combine "
                 "multiple small assets.",
        "category": "Eligibility"
    },
    "What is an aggregator?": {
        "answer": "An aggregator is a company that combines multiple smaller flexibility assets (like your business) into a larger portfolio "
                 "that can participate in flexibility markets. They handle the complexity of bidding, dispatch, settlement, and compliance—"
                 "you just provide the flexibility and receive a share of the revenue. This is often the easiest route for smaller businesses.",
        "category": "Getting Started"
    },
    "How long are the contracts?": {
        "answer": "Contract lengths vary widely by service:\n"
                 "- Capacity Market: 1-15 years (depending on auction type)\n"
                 "- Dynamic Containment: Monthly auctions\n"
                 "- Demand Flexibility Service: Event-by-event (no long-term commitment)\n"
                 "- DNO services: Typically 1-3 years\n"
                 "Check the specific service requirements in the 'Service Details' section.",
        "category": "Contracts"
    },
    "What if I can't deliver when called?": {
        "answer": "Consequences vary by service. For 'firm' services (like Capacity Market or Dynamic Containment), non-delivery results in "
                 "financial penalties. For 'non-firm' services (like Demand Flexibility Service), non-delivery typically just means no payment "
                 "for that event—no penalty. Always understand the performance requirements and penalties before signing up.",
        "category": "Contracts"
    },
    "Can I stack services with my existing PPA or tariff?": {
        "answer": "Usually yes, but check your contract terms. Some Power Purchase Agreements (PPAs) or commercial tariffs have exclusivity "
                 "clauses that limit participation in other markets. Export tariffs (for generation) may also have restrictions. "
                 "Review your existing contracts and consult your supplier before committing to flexibility services.",
        "category": "Contracts"
    },
}


def get_glossary():
    """Get the complete glossary"""
    return GLOSSARY


def get_faqs():
    """Get the complete FAQ list"""
    return FAQS


def get_faqs_by_category():
    """Get FAQs organized by category"""
    categories = {}
    for question, details in FAQS.items():
        category = details.get('category', 'General')
        if category not in categories:
            categories[category] = []
        categories[category].append({
            'question': question,
            'answer': details['answer']
        })
    return categories
