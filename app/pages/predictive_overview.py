import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, narrative_card, beautiful_bar


st.set_page_config(
    page_title="Predictive Intelligence Suite",
    page_icon="",
    layout="wide"
)

load_css()

page_header(
    "Predictive",
    "Intelligence Suite",
    "AI-powered NHS decision intelligence for admission prediction, operational pressure and policy redesign."
)

section_label("Executive Intelligence Summary")

k1, k2, k3, k4 = st.columns(4)

with k1:
    kpi_card("Patients Analysed", "558,018", "Unscheduled care records")

with k2:
    kpi_card("Admission Model", "AUC 0.862", "Random Forest")

with k3:
    kpi_card("Operational Model", "AUC 0.858", "LightGBM")

with k4:
    kpi_card("Policy Model", "AUC 0.855", "XGBoost")

section_label("Executive Intelligence Narrative")

narrative_card(
    """
    The Predictive Intelligence Suite provides a patient-to-system
    decision intelligence framework across unscheduled care.
    <br><br>
    Admission Intelligence predicts inpatient admission risk,
    Operational Intelligence forecasts pressure and congestion risk,
    while Policy Intelligence identifies service redesign and
    population-level improvement opportunities.
    """
)

section_label("AI Intelligence Portfolio")

c1, c2, c3 = st.columns(3)

with c1:
    narrative_card(
        """
        <b>Admission Intelligence</b><br><br>
        Predicts patient-level admission probability and explains
        risk drivers using SHAP.
        <br><br>
        <b>Best for:</b> clinical review, bed planning and escalation.
        """
    )
    st.page_link("pages/admission_intelligence.py", label="Launch Admission Intelligence")

with c2:
    narrative_card(
        """
        <b>Operational Intelligence</b><br><br>
        Predicts operational pressure, escalation risk and patient
        flow disruption.
        <br><br>
        <b>Best for:</b> capacity planning, flow control and escalation readiness.
        """
    )
    st.page_link("pages/operational_intelligence.py", label="Launch Operational Intelligence")

with c3:
    narrative_card(
        """
        <b>Policy Intelligence</b><br><br>
        Predicts strategic redesign priority and pathway improvement
        opportunity.
        <br><br>
        <b>Best for:</b> service redesign, equity monitoring and long-term planning.
        """
    )
    st.page_link("pages/policy_intelligence.py", label="Launch Policy Intelligence")

section_label("Individual Model Feature Importance")

xgb_df = pd.DataFrame({
    "Feature": [
        "Patient Segment", "Clinical Acuity", "Employment",
        "Previous Disposition", "Insurance", "Arrival Mode",
        "Age", "Race", "Arrival Month", "Arrival Time"
    ],
    "Importance": [0.57, 0.11, 0.08, 0.06, 0.06, 0.03, 0.02, 0.015, 0.01, 0.01]
})

lgbm_df = pd.DataFrame({
    "Feature": [
        "Clinical Acuity", "Age", "Flow Pressure", "Insurance",
        "Employment", "Arrival Mode", "Arrival Month",
        "Arrival Time", "Vitals Documentation", "Previous Disposition"
    ],
    "Importance": [1775, 1320, 870, 735, 610, 560, 485, 465, 450, 360]
})

rf_df = pd.DataFrame({
    "Feature": [
        "Clinical Acuity", "Patient Segment", "Age", "Employment",
        "Flow Pressure", "Previous Disposition", "Insurance",
        "Arrival Mode", "Race", "Vitals Documentation"
    ],
    "Importance": [0.30, 0.255, 0.08, 0.078, 0.075, 0.066, 0.057, 0.047, 0.012, 0.009]
})

tabs = st.tabs([
    "Admission Model",
    "Operational Model",
    "Policy Model"
])



with tabs[0]:

    fig = px.bar(
        rf_df.sort_values("Importance"),
        x="Importance",
        y="Feature",
        orientation="h",
        text="Importance",
        color="Importance",
        color_continuous_scale=["#4ade80", "#fb923c"],
        template="plotly_dark",
        title="Random Forest Admission Feature Importance"
    )

    st.plotly_chart(beautiful_bar(fig), use_container_width=True)

    narrative_card(
        """
        <b>Why Random Forest for Admission Intelligence?</b><br><br>
        Random Forest was selected for Admission Intelligence because it provides
        stable patient-level risk stratification while preserving interpretability
        across clinical, demographic and pathway features.
        <br><br>
        The feature importance shows that admission risk is strongly shaped by
        clinical acuity, patient segment, age, employment status, flow pressure
        and previous disposition. This supports safer escalation decisions,
        senior review prioritisation and bed planning.
        """
    )


with tabs[1]:

    fig = px.bar(
        lgbm_df.sort_values("Importance"),
        x="Importance",
        y="Feature",
        orientation="h",
        text="Importance",
        color="Importance",
        color_continuous_scale=["#4ade80", "#fb923c"],
        template="plotly_dark",
        title="LightGBM Operational Feature Importance"
    )

    st.plotly_chart(beautiful_bar(fig), use_container_width=True)

    narrative_card(
        """
        <b>Why LightGBM for Operational Intelligence?</b><br><br>
        LightGBM was selected for Operational Intelligence because it efficiently
        captures high-volume structured pressure signals across unscheduled care.
        <br><br>
        The feature ranking shows that operational risk is driven by clinical
        acuity, age, flow pressure, insurance status, employment status, arrival
        route and timing. This supports capacity planning, flow coordination and
        escalation readiness.
        """
    )


with tabs[2]:

    fig = px.bar(
        xgb_df.sort_values("Importance"),
        x="Importance",
        y="Feature",
        orientation="h",
        text="Importance",
        color="Importance",
        color_continuous_scale=["#4ade80", "#fb923c"],
        template="plotly_dark",
        title="XGBoost Policy Feature Importance"
    )

    st.plotly_chart(beautiful_bar(fig), use_container_width=True)

    narrative_card(
        """
        <b>Why XGBoost for Policy Intelligence?</b><br><br>
        XGBoost was selected for Policy Intelligence because it captures strong
        pathway-level patterns that are useful for strategic redesign and
        population-level planning.
        <br><br>
        The feature importance shows that policy opportunity is strongly shaped
        by patient segment, clinical acuity, employment status, insurance status,
        previous disposition and arrival mode. This supports transparent service
        redesign, admission avoidance planning and equity-aware improvement.
        """
    )
