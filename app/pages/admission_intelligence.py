import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import pandas as pd
import plotly.express as px
import streamlit as st

from src.intelligence.patient_scenario_engine import generate_patient_intelligence

from utils.styling import load_css
from utils.ui_components import (
    page_header,
    section_label,
    kpi_card,
    narrative_card,
    gauge_chart,
)


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Admission Intelligence",
    page_icon="",
    layout="wide"
)

load_css()


# =====================================================
# LOCAL PAGE CSS
# =====================================================

st.markdown(
    """
    <style>
    .action-panel {
        background: rgba(15, 23, 42, 0.88);
        border-radius: 22px;
        padding: 1.25rem;
        min-height: 430px;
        box-shadow: 0 0 28px rgba(0,0,0,0.18);
    }

    .clinical-panel {
        border-left: 5px solid #4ade80;
    }

    .operational-panel {
        border-left: 5px solid #38bdf8;
    }

    .strategic-panel {
        border-left: 5px solid #fb923c;
    }

    .action-title {
        color: #f8fafc;
        font-size: 1.45rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }

    .action-item {
        background: rgba(2, 8, 23, 0.42);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.7rem;
        color: #f8fafc;
        font-size: 0.95rem;
        line-height: 1.45;
    }

    .action-note {
        color: #94a3b8;
        font-size: 0.82rem;
        line-height: 1.45;
        margin-top: 0.8rem;
    }

    .driver-pill {
        display: inline-block;
        background: rgba(74, 222, 128, 0.12);
        border: 1px solid rgba(74, 222, 128, 0.24);
        color: #bbf7d0;
        border-radius: 999px;
        padding: 0.42rem 0.75rem;
        margin: 0.2rem 0.25rem 0.2rem 0;
        font-size: 0.82rem;
        font-weight: 700;
    }

    .mini-summary {
        background: rgba(15, 23, 42, 0.9);
        border-left: 5px solid #fb923c;
        border-radius: 20px;
        padding: 1.25rem;
        color: #f8fafc;
        line-height: 1.6;
        box-shadow: 0 0 26px rgba(251,146,60,0.08);
    }

    .download-card {
        background: rgba(15, 23, 42, 0.84);
        border: 1px solid rgba(74,222,128,0.18);
        border-radius: 20px;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# HELPERS
# =====================================================

def clean_feature_name(feature: str) -> str:
    feature = str(feature)
    feature = feature.replace("num__", "")
    feature = feature.replace("cat__", "")
    feature = feature.replace("_", " ")
    feature = feature.replace("arrivalhour bin", "arrival time")
    feature = feature.replace("previousdispo", "previous disposition")
    feature = feature.replace("employstatus", "employment status")
    return feature.title()


def get_top_driver_names(result: dict, top_n: int = 5) -> list:
    drivers = result.get("executive_drivers", [])

    if not drivers:
        return []

    driver_df = pd.DataFrame(drivers)

    if driver_df.empty or "feature" not in driver_df.columns:
        return []

    driver_df = driver_df.sort_values(
        "impact",
        ascending=False
    )

    return [
        clean_feature_name(feature)
        for feature in driver_df.head(top_n)["feature"].tolist()
    ]


def build_action_lists(
    probability: float,
    risk_level: str,
    cluster_name: str,
    top_drivers: list
) -> dict:

    clinical_actions = []
    operational_actions = []
    strategic_actions = []

    probability_pct = probability * 100
    driver_text = " ".join(top_drivers).lower()
    cluster_text = cluster_name.lower()

    # =================================================
    # RISK-LEVEL ACTIONS
    # =================================================

    if probability_pct >= 80 or risk_level == "Very High":

        clinical_actions.extend([
            "Request senior clinical review and confirm admission decision early.",
            "Prepare for inpatient assessment while reviewing immediate alternatives.",
            "Prioritise diagnostics, observations and specialty input to reduce delay."
        ])

        operational_actions.extend([
            "Alert flow coordination team to likely bed demand.",
            "Reserve escalation capacity if current flow pressure is high.",
            "Begin early discharge planning checks to protect downstream capacity."
        ])

        strategic_actions.extend([
            "Review whether this presentation reflects avoidable admission demand.",
            "Monitor similar high-risk attendances for repeated pathway pressure.",
            "Use this case profile to inform admission avoidance and capacity planning."
        ])

    elif probability_pct >= 60 or risk_level == "High":

        clinical_actions.extend([
            "Use rapid assessment pathway to confirm admission need.",
            "Consider Same Day Emergency Care or observation pathway where safe.",
            "Increase clinical monitoring until discharge or admission decision is clear."
        ])

        operational_actions.extend([
            "Monitor bed demand trajectory and maintain escalation readiness.",
            "Coordinate diagnostics and decision-making to prevent avoidable delay.",
            "Review discharge and transfer capacity if admission becomes likely."
        ])

        strategic_actions.extend([
            "Track similar profiles for preventable admission opportunities.",
            "Assess whether community or virtual ward alternatives are suitable.",
            "Monitor pathway effectiveness for this patient group."
        ])

    elif probability_pct >= 40 or risk_level == "Moderate":

        clinical_actions.extend([
            "Complete focused clinical review and monitor escalation triggers.",
            "Assess ambulatory care, observation or short-stay suitability.",
            "Confirm discharge safety criteria early."
        ])

        operational_actions.extend([
            "Apply routine flow monitoring with contingency escalation plan.",
            "Avoid premature bed allocation unless clinical risk increases.",
            "Coordinate timely review to prevent unnecessary waiting."
        ])

        strategic_actions.extend([
            "Monitor this group for rising admission conversion.",
            "Review preventable escalation points across similar cases.",
            "Use pathway data to refine community follow-up planning."
        ])

    else:

        clinical_actions.extend([
            "Manage through community or ambulatory pathway where clinically appropriate.",
            "Confirm safety-netting and follow-up arrangements.",
            "Avoid unnecessary inpatient escalation unless symptoms change."
        ])

        operational_actions.extend([
            "Prioritise efficient streaming away from bed-based care.",
            "Support rapid discharge or community referral workflow.",
            "Maintain low-intensity monitoring without occupying escalation capacity."
        ])

        strategic_actions.extend([
            "Use this profile to strengthen prevention and community care pathways.",
            "Monitor repeat attendance patterns over time.",
            "Review if low-risk demand begins to increase."
        ])

    # =================================================
    # CLUSTER-SPECIFIC ACTIONS
    # =================================================

    if "elderly" in cluster_text:

        clinical_actions.extend([
            "Complete frailty screening and consider Comprehensive Geriatric Assessment."
        ])

        operational_actions.extend([
            "Engage discharge, therapy and social care planning early."
        ])

        strategic_actions.extend([
            "Assess Hospital-at-Home, virtual ward or frailty pathway suitability."
        ])

    elif "ambulatory" in cluster_text:

        clinical_actions.extend([
            "Prioritise urgent treatment or ambulatory pathway review."
        ])

        operational_actions.extend([
            "Avoid bed allocation where safe community management is appropriate."
        ])

        strategic_actions.extend([
            "Strengthen community diversion and urgent treatment centre pathways."
        ])

    elif "moderate" in cluster_text:

        clinical_actions.extend([
            "Use rapid diagnostics to support a timely admit-or-discharge decision."
        ])

        operational_actions.extend([
            "Prepare SDEC or short-stay streaming if clinical uncertainty remains."
        ])

        strategic_actions.extend([
            "Review mixed-acuity pathway delays and SDEC capacity."
        ])

    elif "ambulance" in cluster_text:

        clinical_actions.extend([
            "Prioritise ambulance arrival assessment and escalation review."
        ])

        operational_actions.extend([
            "Monitor ambulance handover and arrival-to-assessment timing."
        ])

        strategic_actions.extend([
            "Review ambulance streaming and ED congestion drivers."
        ])

    # =================================================
    # SHAP-DRIVER-SPECIFIC ACTIONS
    # =================================================

    if "acuity" in driver_text:
        clinical_actions.append(
            "Escalate review because clinical acuity is a key prediction driver."
        )

    if "age" in driver_text:
        clinical_actions.append(
            "Review age-related frailty, comorbidity and discharge support needs."
        )

    if "flow" in driver_text:
        operational_actions.append(
            "Increase flow coordination because operational pressure is influencing risk."
        )

    if "previous disposition" in driver_text:
        operational_actions.append(
            "Review previous pathway outcome to identify repeat utilisation or failed discharge signals."
        )

    if (
        "race" in driver_text
        or "insurance" in driver_text
        or "employment" in driver_text
    ):
        strategic_actions.append(
            "Monitor equity and access variation linked to prediction drivers."
        )

    return {
        "clinical_actions": list(dict.fromkeys(clinical_actions))[:5],
        "operational_actions": list(dict.fromkeys(operational_actions))[:5],
        "strategic_actions": list(dict.fromkeys(strategic_actions))[:5],
    }


def render_action_panel(
    title: str,
    actions: list,
    panel_class: str,
    footer: str
) -> None:

    action_html = ""

    for action in actions:
        action_html += (
            "<div class='action-item'>"
            f"{action}"
            "</div>"
        )

    html = (
        f"<div class='action-panel {panel_class}'>"
        f"<div class='action-title'>{title}</div>"
        f"{action_html}"
        f"<div class='action-note'>{footer}</div>"
        "</div>"
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


def render_driver_pills(drivers: list) -> None:

    if not drivers:
        st.markdown(
            "<span class='driver-pill'>Model-derived pathway features</span>",
            unsafe_allow_html=True
        )
        return

    pill_html = ""

    for driver in drivers:
        pill_html += (
            "<span class='driver-pill'>"
            f"{driver}"
            "</span>"
        )

    st.markdown(
        pill_html,
        unsafe_allow_html=True
    )


# =====================================================
# HEADER
# =====================================================

page_header(
    "Admission",
    "Intelligence",
    """
    Patient-level admission prediction, pathway classification,
    SHAP explainability and executive NHS decision support.
    """
)


# =====================================================
# PATIENT INPUTS
# =====================================================

section_label("Patient Scenario Simulator")

col1, col2, col3 = st.columns(3)

with col1:

    age = st.slider(
        "Age",
        18,
        100,
        65
    )

    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female"
        ]
    )

    ethnicity = st.selectbox(
        "Ethnicity",
        [
            "Non-Hispanic",
            "Hispanic",
            "Unknown"
        ]
    )

    race = st.selectbox(
        "Race",
        [
            "White",
            "Black",
            "Asian",
            "Other",
            "Unknown"
        ]
    )

    insurance_status = st.selectbox(
        "Insurance Status",
        [
            "Private",
            "Public",
            "Self Pay",
            "Medicaid",
            "Unknown"
        ]
    )

with col2:

    employstatus = st.selectbox(
        "Employment Status",
        [
            "Student Full Time",
            "Employed",
            "Unemployed",
            "Retired",
            "Disabled",
            "Unknown"
        ]
    )

    arrivalmode = st.selectbox(
        "Arrival Mode",
        [
            "Walk-in",
            "Wheelchair",
            "Car",
            "Ambulance",
            "Transfer",
            "Public Transportation",
            "Unknown"
        ]
    )

    previousdispo = st.selectbox(
        "Previous Disposition",
        [
            "Home",
            "Admission",
            "Transfer",
            "Discharged",
            "Unknown"
        ]
    )

    clinical_acuity = st.slider(
        "Clinical Acuity",
        1,
        5,
        3
    )

with col3:

    arrivalmonth = st.selectbox(
        "Arrival Month",
        [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ]
    )

    arrivalday = st.selectbox(
        "Arrival Day",
        [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"
        ]
    )

    arrivalhour_bin = st.selectbox(
        "Arrival Time Band",
        [
            "Night",
            "Morning",
            "Day",
            "Evening"
        ]
    )

    flow_pressure_z = st.slider(
        "Flow Pressure",
        -3.0,
        3.0,
        0.0
    )

    vitals_documented = st.selectbox(
        "Vitals Documented",
        [
            0,
            1
        ]
    )


# =====================================================
# GENERATE INTELLIGENCE
# =====================================================

if st.button(
    "Generate Admission Intelligence",
    use_container_width=True
):

    patient = {
        "age": age,
        "gender": gender,
        "ethnicity": ethnicity,
        "race": race,
        "lang": "English",
        "employstatus": employstatus,
        "insurance_status": insurance_status,
        "arrivalmode": arrivalmode,
        "arrivalmonth": arrivalmonth,
        "arrivalday": arrivalday,
        "arrivalhour_bin": arrivalhour_bin,
        "previousdispo": previousdispo,
        "flow_pressure_z": flow_pressure_z,
        "clinical_acuity": clinical_acuity,
        "vitals_documented": vitals_documented
    }

    with st.spinner(
        "Generating AI-powered admission intelligence..."
    ):

        result = generate_patient_intelligence(
            patient
        )

    probability = result["probability"] * 100
    risk_level = result["risk_level"]
    cluster_name = result["cluster_name"]
    cluster_confidence = result["cluster_confidence"] * 100

    top_drivers = get_top_driver_names(
        result=result,
        top_n=5
    )

    actions = build_action_lists(
        probability=result["probability"],
        risk_level=risk_level,
        cluster_name=cluster_name,
        top_drivers=top_drivers
    )


    # =================================================
    # KPI SUMMARY
    # =================================================

    section_label("Executive Intelligence Summary")

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        kpi_card(
            "Admission Probability",
            f"{probability:.1f}%",
            "Predicted inpatient risk"
        )

    with k2:

        kpi_card(
            "Risk Level",
            risk_level,
            "Escalation category"
        )

    with k3:

        kpi_card(
            "Patient Segment",
            cluster_name,
            "Predicted pathway group"
        )

    with k4:

        kpi_card(
            "Segment Confidence",
            f"{cluster_confidence:.1f}%",
            "Cluster certainty"
        )



    # =================================================
    # PREDICTION EVIDENCE
    # =================================================

    section_label("Prediction Evidence")

    left, right = st.columns(2)

    with left:

        st.plotly_chart(
            gauge_chart(
                probability,
                "Admission Probability"
            ),
            use_container_width=True
        )

    with right:

        cluster_df = pd.DataFrame({
            "Segment": list(
                result["cluster_probabilities"].keys()
            ),
            "Probability": list(
                result["cluster_probabilities"].values()
            )
        })

        fig_cluster = px.bar(
            cluster_df.sort_values(
                "Probability"
            ),
            x="Probability",
            y="Segment",
            orientation="h",
            text="Probability",
            color="Probability",
            color_continuous_scale=[
                "#4ade80",
                "#fb923c"
            ],
            title="Patient Pathway Classification",
            template="plotly_dark"
        )

        fig_cluster.update_layout(
            height=360,
            yaxis_title="",
            xaxis_title="Cluster Likelihood",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#f8fafc"
            )
        )

        st.plotly_chart(
            fig_cluster,
            use_container_width=True
        )


    # =================================================
    # SHAP DRIVER ANALYSIS
    # =================================================

    section_label("AI Driver Intelligence")

    driver_df = pd.DataFrame(
        result.get(
            "executive_drivers",
            []
        )
    )

    if not driver_df.empty:

        driver_df["feature"] = driver_df["feature"].apply(
            clean_feature_name
        )

        driver_df = driver_df.sort_values(
            "impact",
            ascending=True
        )

        fig_drivers = px.bar(
            driver_df,
            x="impact",
            y="feature",
            orientation="h",
            color="direction",
            text="impact",
            title="Feature Contribution Toward Admission Risk",
            template="plotly_dark"
        )

        fig_drivers.update_layout(
            height=520,
            yaxis_title="",
            xaxis_title="SHAP Impact",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#f8fafc"
            )
        )

        st.plotly_chart(
            fig_drivers,
            use_container_width=True
        )

    else:

        st.warning(
            "SHAP drivers unavailable for this prediction."
        )



    # =================================================
    # EXECUTIVE SUMMARY
    # =================================================

    section_label("Executive Admission Assessment")

    st.markdown(
        f"""
        <div class="mini-summary">
            <b>Decision summary:</b><br><br>
            This patient profile is predicted to belong to the
            <b>{cluster_name}</b> pathway segment with an admission
            probability of <b>{probability:.1f}%</b>.
            This places the patient in the <b>{risk_level}</b>
            admission risk category.
            <br><br>
            <b>Key explainability signals:</b><br>
        </div>
        """,
        unsafe_allow_html=True
    )

    render_driver_pills(
        top_drivers
    )
    # =================================================
    # ACTION FRAMEWORK
    # =================================================

    section_label("Executive Action Framework")

    clinical_col, operational_col, strategic_col = st.columns(3)

    with clinical_col:

        render_action_panel(
            title="Clinical Priorities",
            actions=actions["clinical_actions"],
            panel_class="clinical-panel",
            footer="Focused on clinical safety, early review and appropriate care pathway selection."
        )

    with operational_col:

        render_action_panel(
            title="Operational Priorities",
            actions=actions["operational_actions"],
            panel_class="operational-panel",
            footer="Focused on flow coordination, bed demand, escalation readiness and discharge planning."
        )

    with strategic_col:

        render_action_panel(
            title="Strategic Priorities",
            actions=actions["strategic_actions"],
            panel_class="strategic-panel",
            footer="Focused on avoidable admission reduction, pathway redesign and equity-aware planning."
        )


    # =================================================
    # DOWNLOAD REPORT
    # =================================================

    section_label("Executive Report")

    flat_actions = (
        actions["clinical_actions"]
        + actions["operational_actions"]
        + actions["strategic_actions"]
    )

    report_text = f"""
ADMISSION INTELLIGENCE REPORT

Patient Segment:
{cluster_name}

Segment Confidence:
{cluster_confidence:.1f}%

Admission Probability:
{probability:.1f}%

Risk Level:
{risk_level}

Key Explainability Drivers:
{chr(10).join(top_drivers)}

Clinical Actions:
{chr(10).join(actions["clinical_actions"])}

Operational Actions:
{chr(10).join(actions["operational_actions"])}

Strategic Actions:
{chr(10).join(actions["strategic_actions"])}
"""

    st.markdown(
        """
        <div class="download-card">
            Download a concise executive report containing the prediction,
            pathway segment, explainability drivers and recommended actions.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.download_button(
        label="Download Admission Intelligence Report",
        data=report_text,
        file_name="admission_intelligence_report.txt",
        mime="text/plain",
        use_container_width=True
    )