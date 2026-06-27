# =====================================================
# ADMISSION RECOMMENDATIONS ENGINE
# =====================================================

def generate_admission_recommendations(
    probability,
    cluster_name
):

    clinical_actions = []

    operational_actions = []

    strategic_actions = []

    # ==========================================
    # VERY HIGH RISK
    # ==========================================

    if probability >= 0.80:

        clinical_actions.extend([

            "Senior clinician review",

            "Frailty assessment pathway",

            "Early specialty referral",

            "Immediate inpatient assessment"

        ])

        operational_actions.extend([

            "Bed demand forecasting",

            "Capacity escalation review",

            "Flow coordination prioritisation"

        ])

        strategic_actions.extend([

            "Review avoidable admission drivers",

            "Assess Hospital-at-Home suitability",

            "Monitor high-utilisation cohorts"

        ])

    # ==========================================
    # HIGH RISK
    # ==========================================

    elif probability >= 0.60:

        clinical_actions.extend([

            "Rapid assessment pathway",

            "Same Day Emergency Care review",

            "Enhanced clinical observation"

        ])

        operational_actions.extend([

            "Patient flow monitoring",

            "Capacity planning review",

            "Escalation trigger monitoring"

        ])

        strategic_actions.extend([

            "Community diversion assessment",

            "Virtual ward suitability review",

            "Monitor pathway effectiveness"

        ])

    # ==========================================
    # MODERATE / LOW
    # ==========================================

    else:

        clinical_actions.extend([

            "Community pathway review",

            "Virtual ward screening",

            "Discharge optimisation"

        ])

        operational_actions.extend([

            "Routine flow management",

            "Standard capacity monitoring"

        ])

        strategic_actions.extend([

            "Avoidable admission reduction",

            "Preventative care opportunities"

        ])

    return {

        "clinical_actions":
            clinical_actions,

        "operational_actions":
            operational_actions,

        "strategic_actions":
            strategic_actions

    }


