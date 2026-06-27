import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import plotly.express as px
import streamlit as st

from src.utils.data_loader import load_patient_data, load_persona_data
from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, narrative_card


st.set_page_config(
    page_title="NHS Intelligence Platform",
    page_icon="",
    layout="wide"
)

load_css()

journey_df = load_patient_data()
persona_df = load_persona_data()

page_header(
    "NHS Unscheduled Care",
    "Intelligence Platform",
    "Transforming patient journey data into clinical, operational and strategic intelligence."
)

section_label("Executive Command Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Patients", f"{len(journey_df):,}", "Journey records analysed")

with c2:
    kpi_card("Journey Segments", f"{journey_df['cluster_name'].nunique()}", "AI-derived pathway groups")

with c3:
    kpi_card("Admission Rate", f"{journey_df['admit_flag'].mean() * 100:.1f}%", "Overall admission burden")

with c4:
    kpi_card("Registered Models", "3", "Admission, operational, policy")

section_label("Platform Intelligence Narrative")

narrative_card(
    """
    This platform converts unscheduled care pathway data into executive-ready intelligence.
    It combines clustering, patient pathway analysis, admission prediction, operational
    pressure forecasting, policy opportunity detection, SHAP explainability and governance
    controls to support safer, faster and more transparent NHS decision-making.
    """
)

section_label("Intelligence Modules")

m1, m2, m3 = st.columns(3)

with m1:
    narrative_card(
        """
        <b>Cluster Intelligence</b><br><br>
        Understand patient segments, population burden, demographic variation and service redesign opportunities.
        <br><br>
        <b>Output:</b> segment profiles, pathway opportunities and policy insight.
        """
    )
    st.page_link("pages/cluster_overview.py", label="Launch Cluster Intelligence")

with m2:
    narrative_card(
        """
        <b>Predictive Intelligence</b><br><br>
        Predict admission risk, operational pressure and strategic policy priority using three registered models.
        <br><br>
        <b>Output:</b> risk scores, SHAP drivers and recommended actions.
        """
    )
    st.page_link("pages/predictive_overview.py", label="Launch Predictive Intelligence")

with m3:
    narrative_card(
        """
        <b>Governance Intelligence</b><br><br>
        Show how the platform works end-to-end, including model traceability, explainability and retraining readiness.
        <br><br>
        <b>Output:</b> production flow, controls and model lifecycle.
        """
    )
    st.page_link("pages/governance_intelligence.py", label="Launch Governance Intelligence")

section_label("Patient Journey Segment Distribution")

cluster_dist = (
    journey_df
    .groupby("cluster_name")
    .size()
    .reset_index(name="patients")
)

fig = px.pie(
    cluster_dist,
    names="cluster_name",
    values="patients",
    hole=0.62,
    title="Patient Journey Segment Distribution",
    template="plotly_dark"
)

fig.update_layout(
    height=520,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#f8fafc")
)

st.plotly_chart(fig, use_container_width=True)


section_label("Key Business Values Deliverables")

deliverables = [
    {
        "title": "Patient Segmentation Delivered",
        "metric": "4 Cohorts",
        "note": "AI-derived pathway groups",
        "detail": """
        <b>What this delivered:</b><br>
        The project identified four meaningful unscheduled care patient segments:
        Community Ambulatory Care, Moderate Complexity Care, Acute Ambulance Pathways,
        and Complex Elderly Admissions.
        <br><br>
        <b>Stakeholder value:</b><br>
        Enables NHS leaders to understand demand by patient type, not just total attendances.
        """
    },
    {
        "title": "Admission Burden Identified",
        "metric": f"{journey_df['admit_flag'].mean() * 100:.1f}%",
        "note": "Overall admission rate",
        "detail": """
        <b>What this delivered:</b><br>
        The platform quantifies admission burden across the full unscheduled care pathway
        and shows which patient groups contribute most strongly to inpatient demand.
        <br><br>
        <b>Stakeholder value:</b><br>
        Supports bed planning, escalation decisions, admission avoidance and senior review prioritisation.
        """
    },
    {
        "title": "Predictive Intelligence Built",
        "metric": "3 Models",
        "note": "Admission, operational and policy",
        "detail": """
        <b>What this delivered:</b><br>
        Three predictive models were trained and registered: XGBoost for admission risk,
        LightGBM for operational pressure, and Random Forest for policy priority.
        <br><br>
        <b>Stakeholder value:</b><br>
        Moves the system from descriptive reporting to proactive decision intelligence.
        """
    },
    {
        "title": "Explainable AI Added",
        "metric": "SHAP",
        "note": "Transparent prediction drivers",
        "detail": """
        <b>What this delivered:</b><br>
        SHAP explainability was integrated to show the drivers behind patient-level risk predictions.
        <br><br>
        <b>Stakeholder value:</b><br>
        Improves trust, transparency, governance and clinical interpretability.
        """
    },
    {
        "title": "Pathway Intelligence Created",
        "metric": "Sankey",
        "note": "Journey flow analysis",
        "detail": """
        <b>What this delivered:</b><br>
        The dashboard maps patient movement from arrival route through segment assignment
        to final disposition outcome.
        <br><br>
        <b>Stakeholder value:</b><br>
        Reveals bottlenecks, high-risk pathways and opportunities for better streaming.
        """
    },
    {
        "title": "Governance Layer Delivered",
        "metric": "MLOps",
        "note": "Registry, S3, API-ready",
        "detail": """
        <b>What this delivered:</b><br>
        The project now includes MLflow registration, local/S3 artifact storage,
        FastAPI readiness and governance documentation.
        <br><br>
        <b>Stakeholder value:</b><br>
        Positions the platform as a production-ready healthcare AI system, not just a dashboard.
        """
    }
]

for idx in range(0, len(deliverables), 3):

    cols = st.columns(3)

    for col, item in zip(cols, deliverables[idx:idx + 3]):

        with col:

            kpi_card(
                item["title"],
                item["metric"],
                item["note"]
            )

            narrative_card(
                item["detail"]
            )