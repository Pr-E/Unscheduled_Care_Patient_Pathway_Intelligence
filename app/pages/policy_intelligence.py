import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import pandas as pd
import plotly.express as px
import streamlit as st

from src.clustering.cluster_feature_builder import build_cluster_features
from src.clustering.cluster_predictor import predict_cluster
from src.predictive.predict_policy import predict_policy
from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, gauge_chart, narrative_card


st.set_page_config(page_title="Policy Intelligence", page_icon="", layout="wide")
load_css()

st.markdown("""
<style>
.policy-panel{background:rgba(15,23,42,.88);border-radius:22px;padding:1.25rem;min-height:330px}
.policy-priority{border-left:5px solid #4ade80}.policy-pathway{border-left:5px solid #38bdf8}.policy-equity{border-left:5px solid #fb923c}
.policy-title{font-size:1.35rem;font-weight:800;color:#f8fafc;margin-bottom:1rem}
.policy-item{background:rgba(2,8,23,.45);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:.8rem 1rem;margin-bottom:.65rem;color:#f8fafc;font-weight:600}
</style>
""", unsafe_allow_html=True)


def render_panel(title, actions, css_class):
    items = "".join([f"<div class='policy-item'>{a}</div>" for a in actions])
    st.markdown(
        f"<div class='policy-panel {css_class}'><div class='policy-title'>{title}</div>{items}</div>",
        unsafe_allow_html=True
    )


def policy_action_engine(priority, segment, arrivalmode, clinical_acuity, flow_pressure_z):
    priority_actions = []
    pathway_actions = []
    equity_actions = []

    if priority == "Critical":
        meaning = "Immediate redesign priority with high system impact."
        priority_actions += [
            "Prioritise this pathway for executive redesign review.",
            "Allocate improvement focus to admission avoidance and capacity protection.",
            "Escalate to service planning if this profile is frequent."
        ]
        pathway_actions += [
            "Review frailty, SDEC, virtual ward or community alternatives.",
            "Assess discharge barriers and avoidable inpatient conversion.",
            "Strengthen cross-service coordination for this pathway."
        ]
    elif priority == "High":
        meaning = "Strong redesign opportunity with clear operational benefit."
        priority_actions += [
            "Target this profile for pathway improvement planning.",
            "Monitor admission conversion and avoidable escalation.",
            "Review service capacity aligned to this cohort."
        ]
        pathway_actions += [
            "Strengthen same-day assessment and community diversion.",
            "Improve diagnostics, streaming and discharge coordination.",
            "Track pathway performance monthly."
        ]
    elif priority == "Moderate":
        meaning = "Targeted improvement opportunity requiring monitoring."
        priority_actions += [
            "Monitor demand pattern and admission conversion.",
            "Use as a candidate for small-scale pathway optimisation.",
            "Review if pressure increases over time."
        ]
        pathway_actions += [
            "Assess preventable escalation points.",
            "Review observation, discharge and community follow-up routes.",
            "Track pathway delay indicators."
        ]
    else:
        meaning = "Lower immediate redesign urgency, useful for surveillance and prevention."
        priority_actions += [
            "Continue population surveillance.",
            "Maintain routine service monitoring.",
            "Review if attendance volume or admission conversion rises."
        ]
        pathway_actions += [
            "Support prevention and community management.",
            "Avoid over-escalation into bed-based pathways.",
            "Use as baseline for monitoring future demand shifts."
        ]

    if "Elderly" in segment:
        pathway_actions.append("Prioritise frailty assessment, CGA, Hospital-at-Home and virtual ward options.")
    if "Ambulatory" in segment:
        pathway_actions.append("Expand urgent treatment, community diversion and ambulatory emergency care capacity.")
    if "Ambulance" in segment or arrivalmode in ["Ambulance", "Transfer"]:
        pathway_actions.append("Review ambulance streaming, handover pressure and rapid assessment access.")
    if clinical_acuity >= 4:
        priority_actions.append("Include high-acuity safety review in redesign planning.")
    if abs(flow_pressure_z) >= 1:
        priority_actions.append("Include flow pressure mitigation in service planning.")

    equity_actions += [
        "Monitor access and outcome variation by race, gender, employment and insurance status.",
        "Review whether pathway redesign could reduce inequity in admission outcomes.",
        "Ensure recommended changes support safe, fair and transparent care decisions."
    ]

    return meaning, {
        "priority": list(dict.fromkeys(priority_actions))[:5],
        "pathway": list(dict.fromkeys(pathway_actions))[:5],
        "equity": list(dict.fromkeys(equity_actions))[:5],
    }


page_header(
    "Policy",
    "Intelligence",
    "Predict strategic redesign priority and service improvement opportunity for patient pathway profiles."
)

section_label("Policy Scenario Simulator")

c1, c2, c3 = st.columns(3)

with c1:
    age = st.slider("Age", 18, 100, 65)
    gender = st.selectbox("Gender", ["Male", "Female"])
    ethnicity = st.selectbox("Ethnicity", ["Non-Hispanic", "Hispanic", "Unknown"])
    race = st.selectbox("Race", ["White", "Black", "Asian", "Other", "Unknown"])

with c2:
    insurance_status = st.selectbox("Insurance Status", ["Private", "Public", "Self Pay", "Medicaid", "Unknown"])
    employstatus = st.selectbox("Employment Status", ["Student Full Time", "Employed", "Unemployed", "Retired", "Unknown"])
    arrivalmode = st.selectbox("Arrival Mode", ["Walk-in", "Wheelchair", "Car", "Ambulance", "Transfer", "Public Transportation", "Unknown"])
    previousdispo = st.selectbox("Previous Disposition", ["Home", "Admission", "Transfer", "Discharged", "Unknown"])

with c3:
    arrivalmonth = st.selectbox("Arrival Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    arrivalday = st.selectbox("Arrival Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    arrivalhour_bin = st.selectbox("Arrival Time Band", ["Night", "Morning", "Day", "Evening"])
    clinical_acuity = st.slider("Clinical Acuity", 1, 5, 3)
    flow_pressure_z = st.slider("Flow Pressure", -3.0, 3.0, 0.0)
    vitals_documented = st.selectbox("Vitals Documented", [0, 1])

if st.button("Generate Policy Intelligence", use_container_width=True):
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

    cluster_result = predict_cluster(**build_cluster_features(patient))
    patient["cluster_name"] = cluster_result["cluster_name"]

    prediction = predict_policy(patient)
    priority_probability = prediction["probability"] * 100
    priority = prediction["priority"]
    segment = cluster_result["cluster_name"]

    meaning, actions = policy_action_engine(
        priority=priority,
        segment=segment,
        arrivalmode=arrivalmode,
        clinical_acuity=clinical_acuity,
        flow_pressure_z=flow_pressure_z
    )

    section_label("Executive Policy KPIs")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card("Redesign Priority", f"{priority_probability:.1f}%", "Strategic opportunity score")
    with k2:
        kpi_card("Priority Level", priority, "Policy category")
    with k3:
        kpi_card("Patient Segment", segment, "Population pattern")
    with k4:
        kpi_card("Segment Confidence", f"{cluster_result['confidence'] * 100:.1f}%", "Pattern certainty")

    section_label("Executive Policy Assessment")

    narrative_card(
        f"""
        This profile indicates a <b>{priority}</b> policy priority with a strategic opportunity score of
        <b>{priority_probability:.1f}%</b>.
        <br><br>
        <b>Interpretation:</b> {meaning}
        <br><br>
        The profile aligns with the <b>{segment}</b> population pattern, so policy action should focus on
        service redesign, admission avoidance, equity monitoring and pathway capacity.
        """
    )

    section_label("Policy Evidence")

    left, right = st.columns(2)

    with left:
        st.plotly_chart(gauge_chart(priority_probability, "Policy Priority"), use_container_width=True)

    with right:
        driver_df = pd.DataFrame({
            "Driver": ["Population Segment", "Clinical Acuity", "Flow Pressure", "Arrival Mode", "Previous Disposition"],
            "Contribution": [
                cluster_result["confidence"],
                clinical_acuity / 5,
                abs(flow_pressure_z),
                0.85 if arrivalmode in ["Ambulance", "Transfer"] else 0.40,
                0.75 if previousdispo in ["Admission", "Transfer"] else 0.35
            ]
        })

        fig = px.bar(
            driver_df.sort_values("Contribution"),
            x="Contribution",
            y="Driver",
            orientation="h",
            text="Contribution",
            color="Contribution",
            color_continuous_scale=["#4ade80", "#fb923c"],
            template="plotly_dark",
            title="Policy Driver Pattern"
        )

        fig.update_layout(
            height=390,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="",
            xaxis_title="Relative policy signal",
            font=dict(color="#f8fafc")
        )

        st.plotly_chart(fig, use_container_width=True)

    section_label("Cluster Policy Distribution")

    cluster_df = pd.DataFrame({
        "Segment": list(cluster_result["cluster_probabilities"].keys()),
        "Probability": list(cluster_result["cluster_probabilities"].values())
    })

    fig = px.bar(
        cluster_df.sort_values("Probability"),
        x="Probability",
        y="Segment",
        orientation="h",
        text="Probability",
        color="Probability",
        color_continuous_scale=["#4ade80", "#fb923c"],
        template="plotly_dark",
        title="Segment Likelihood Driving Policy Priority"
    )

    fig.update_layout(
        height=420,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title="",
        xaxis_title="Cluster likelihood",
        font=dict(color="#f8fafc")
    )

    st.plotly_chart(fig, use_container_width=True)

    section_label("Executive Policy Action Framework")

    p1, p2, p3 = st.columns(3)

    with p1:
        render_panel("Redesign Priorities", actions["priority"], "policy-priority")
    with p2:
        render_panel("Pathway Opportunities", actions["pathway"], "policy-pathway")
    with p3:
        render_panel("Equity & Governance", actions["equity"], "policy-equity")