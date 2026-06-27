# =====================================================
# EXECUTIVE AI ASSESSMENT
# =====================================================

def generate_admission_narrative(

    probability,

    risk_level,

    cluster_name,

    top_drivers

):

    probability_pct = round(
        probability * 100,
        1
    )

    drivers = "\n".join([

        f"• {driver}"

        for driver

        in top_drivers[:5]

    ])

    return f"""
This patient has been classified into the
{cluster_name} segment.

Admission probability is estimated at
{probability_pct}% and is categorised as
{risk_level} risk.

The strongest contributors influencing
this prediction are:

{drivers}

This patient profile closely resembles
historical pathways associated with
elevated inpatient utilisation and
operational demand.

Recommended priority actions include:

• Early clinical review

• Capacity planning

• Pathway optimisation

• Appropriate discharge planning

The patient should be considered for
proactive pathway management to reduce
avoidable delays and improve care flow.
"""