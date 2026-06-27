import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import pandas as pd
import plotly.express as px
import streamlit as st

from src.clustering.cluster_feature_builder import build_cluster_features
from src.clustering.cluster_predictor import predict_cluster
from src.predictive.predict_operational import predict_operational
from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, gauge_chart, narrative_card


st.set_page_config(page_title="Operational Intelligence", page_icon="", layout="wide")
load_css()

st.markdown("""
<style>
.action-panel{background:rgba(15,23,42,.88);border-radius:22px;padding:1.25rem;min-height:330px}
.op-clinical{border-left:5px solid #4ade80}.op-flow{border-left:5px solid #38bdf8}.op-system{border-left:5px solid #fb923c}
.action-title{font-size:1.35rem;font-weight:800;color:#f8fafc;margin-bottom:1rem}
.action-item{background:rgba(2,8,23,.45);border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:.8rem 1rem;margin-bottom:.65rem;color:#f8fafc;font-weight:600}
</style>
""", unsafe_allow_html=True)


def render_panel(title, actions, css_class):
    items = "".join([f"<div class='action-item'>{a}</div>" for a in actions])
    st.markdown(
        f"<div class='action-panel {css_class}'><div class='action-title'>{title}</div>{items}</div>",
        unsafe_allow_html=True
    )


def operational_actions(pressure, segment, arrivalmode, flow_pressure_z, clinical_acuity):
    clinical = []
    flow = []
    system = []

    if pressure == "Critical":
        clinical += ["Immediate senior review readiness", "Prioritise diagnostics and assessment", "Escalate if acuity deteriorates"]
        flow += ["Activate capacity escalation review", "Notify patient flow coordination team", "Prepare bed management contingency"]
        system += ["Monitor high-pressure cohort demand", "Review avoidable congestion drivers", "Escalate to operational command if sustained"]
    elif pressure == "High":
        clinical += ["Rapid clinical review pathway", "Enhanced observation until decision", "Review SDEC suitability"]
        flow += ["Monitor bed demand trajectory", "Maintain escalation readiness", "Coordinate diagnostics to reduce delay"]
        system += ["Track recurring pressure pattern", "Review streaming effectiveness", "Assess preventable flow disruption"]
    elif pressure == "Moderate":
        clinical += ["Focused clinical review", "Monitor escalation triggers", "Assess discharge or observation route"]
        flow += ["Routine flow monitoring", "Prepare contingency capacity route", "Support timely decision-making"]
        system += ["Monitor pressure trend", "Review pathway utilisation", "Identify emerging bottlenecks"]
    else:
        clinical += ["Routine clinical monitoring", "Ambulatory pathway where safe", "Confirm discharge readiness"]
        flow += ["Avoid unnecessary bed allocation", "Support rapid streaming", "Maintain standard capacity monitoring"]
        system += ["Continue surveillance", "Track low-risk demand", "Review only if volume increases"]

    if "Elderly" in segment:
        clinical.append("Include frailty and discharge support review")
        flow.append("Coordinate therapy, social care and discharge planning early")
    if "Ambulance" in segment or arrivalmode in ["Ambulance", "Transfer"]:
        flow.append("Monitor ambulance handover and arrival-to-assessment time")
        system.append("Review ambulance streaming pressure")
    if flow_pressure_z >= 1:
        flow.append("Increase flow coordination due to elevated pressure")
    if clinical_acuity >= 4:
        clinical.append("Prioritise high-acuity clinical assessment")

    return {
        "clinical": list(dict.fromkeys(clinical))[:5],
        "flow": list(dict.fromkeys(flow))[:5],
        "system": list(dict.fromkeys(system))[:5],
    }


page_header(
    "Operational",
    "Intelligence",
    "Predict operational pressure, escalation risk and patient flow disruption across unscheduled care."
)

section_label("Operational Scenario Simulator")

c1, c2, c3 = st.columns(3)

with c1:
    age = st.slider("Age", 18, 100, 65)
    gender = st.selectbox("Gender", ["Male", "Female"])
    insurance_status = st.selectbox("Insurance Status", ["Private", "Public", "Self Pay", "Medicaid", "Unknown"])
    employstatus = st.selectbox("Employment Status", ["Student Full Time", "Employed", "Unemployed", "Retired", "Unknown"])

with c2:
    arrivalmode = st.selectbox("Arrival Mode", ["Walk-in", "Wheelchair", "Car", "Ambulance", "Transfer", "Public Transportation", "Unknown"])
    previousdispo = st.selectbox("Previous Disposition", ["Home", "Admission", "Transfer", "Discharged", "Unknown"])
    clinical_acuity = st.slider("Clinical Acuity", 1, 5, 3)
    flow_pressure_z = st.slider("Flow Pressure", -3.0, 3.0, 0.0)

with c3:
    arrivalmonth = st.selectbox("Arrival Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    arrivalday = st.selectbox("Arrival Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    arrivalhour_bin = st.selectbox("Arrival Time Band", ["Night", "Morning", "Day", "Evening"])
    vitals_documented = st.selectbox("Vitals Documented", [0, 1])

if st.button("Generate Operational Forecast", use_container_width=True):
    patient = {
        "age": age,
        "gender": gender,
        "ethnicity": "Unknown",
        "race": "Unknown",
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

    prediction = predict_operational(patient)
    pressure_probability = prediction["probability"] * 100
    pressure = prediction["pressure"]
    segment = cluster_result["cluster_name"]

    section_label("Executive Operational KPIs")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        kpi_card("Pressure Probability", f"{pressure_probability:.1f}%", "Operational stress score")
    with k2:
        kpi_card("Pressure Level", pressure, "Escalation category")
    with k3:
        kpi_card("Patient Segment", segment, "Pathway context")
    with k4:
        kpi_card("Segment Confidence", f"{cluster_result['confidence'] * 100:.1f}%", "Pattern certainty")

    section_label("Operational Assessment")

    narrative_card(
        f"""
        This profile is predicted to create a <b>{pressure}</b> operational pressure signal
        with a probability of <b>{pressure_probability:.1f}%</b>.
        <br><br>
        The profile aligns with the <b>{segment}</b> pathway. Operational response should focus on
        flow coordination, escalation readiness and timely pathway streaming.
        """
    )

    section_label("Operational Evidence")

    left, right = st.columns(2)

    with left:
        st.plotly_chart(gauge_chart(pressure_probability, "Operational Pressure"), use_container_width=True)

    with right:
        driver_df = pd.DataFrame({
            "Driver": ["Flow Pressure", "Clinical Acuity", "Arrival Mode", "Previous Disposition", "Patient Segment"],
            "Contribution": [
                abs(flow_pressure_z),
                clinical_acuity / 5,
                0.85 if arrivalmode in ["Ambulance", "Transfer"] else 0.45,
                0.75 if previousdispo in ["Admission", "Transfer"] else 0.35,
                cluster_result["confidence"]
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
            title="Operational Driver Pattern"
        )

        fig.update_layout(
            height=390,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title="",
            xaxis_title="Relative pressure signal",
            font=dict(color="#f8fafc")
        )

        st.plotly_chart(fig, use_container_width=True)

    section_label("Executive Operational Action Framework")

    actions = operational_actions(
        pressure=pressure,
        segment=segment,
        arrivalmode=arrivalmode,
        flow_pressure_z=flow_pressure_z,
        clinical_acuity=clinical_acuity
    )

    a1, a2, a3 = st.columns(3)

    with a1:
        render_panel("Clinical Readiness", actions["clinical"], "op-clinical")
    with a2:
        render_panel("Flow Priorities", actions["flow"], "op-flow")
    with a3:
        render_panel("System Response", actions["system"], "op-system")