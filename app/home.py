import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import plotly.express as px
import requests
import streamlit as st

from src.utils.data_loader import load_patient_data, load_persona_data
from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, narrative_card


st.set_page_config(
    page_title="CareFlow IQ",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://54.158.220.0:8000"
).rstrip("/")


def check_api_health() -> bool:
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


st.markdown(
    """
    <style>
    .cf-logo {
        border: 1px solid rgba(56,189,248,.25);
        border-radius: 22px;
        padding: 1.1rem;
        background: linear-gradient(135deg, rgba(15,23,42,.95), rgba(8,47,73,.65));
        box-shadow: 0 0 28px rgba(56,189,248,.12);
        margin-bottom: 1rem;
    }
    .cf-brand {
        font-size: 1.75rem;
        font-weight: 900;
        color: #f8fafc;
        line-height: 1.05;
    }
    .cf-brand span {
        color: #fb923c;
    }
    .cf-subtitle {
        font-size: .76rem;
        color: #94a3b8;
        margin-top: .35rem;
        letter-spacing: .05rem;
    }
    .side-card {
        border: 1px solid rgba(148,163,184,.18);
        border-radius: 16px;
        padding: .85rem;
        background: rgba(15,23,42,.78);
        margin-bottom: .75rem;
    }
    .side-title {
        color: #94a3b8;
        font-size: .72rem;
        text-transform: uppercase;
        letter-spacing: .12rem;
        font-weight: 800;
        margin-bottom: .55rem;
    }
    .status-online {
        color: #4ade80;
        font-weight: 900;
    }
    .status-offline {
        color: #fb7185;
        font-weight: 900;
    }
    .model-row {
        display:flex;
        justify-content:space-between;
        gap:.5rem;
        color:#cbd5e1;
        font-size:.78rem;
        margin-bottom:.4rem;
    }
    .cloud-row {
        color:#cbd5e1;
        font-size:.8rem;
        line-height:1.5;
        margin-bottom:.45rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.markdown(
        """
        <div class="cf-logo">
            <div class="cf-brand">CareFlow <span>IQ</span></div>
            <div class="cf-subtitle">Intelligent Care. Better Outcomes.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### NHS UNSCHEDULED CARE")
    st.caption("Clinical, operational and strategic intelligence")

    st.divider()

    st.markdown(
        f"""
        <div class="side-card">
            <div class="side-title">API Status</div>
            <div class="{ 'status-online' if check_api_health() else 'status-offline' }">
                { '● ONLINE' if check_api_health() else '● OFFLINE' }
            </div>
            <div style="color:#94a3b8;font-size:.75rem;margin-top:.3rem;">
                {API_BASE_URL}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="side-card">
            <div class="side-title">Model Status</div>
            <div class="model-row"><span>Admission</span><b>Random Forest</b></div>
            <div class="model-row"><span>Operational</span><b>LightGBM</b></div>
            <div class="model-row"><span>Policy</span><b>XGBoost</b></div>
            <div style="color:#4ade80;font-size:.75rem;margin-top:.5rem;">● Production models active</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="side-card">
            <div class="side-title">Cloud Infrastructure</div>
            <div class="cloud-row">☁️ Amazon S3 — Model/artifact storage</div>
            <div class="cloud-row">🖥️ Amazon EC2 — Application runtime</div>
            <div class="cloud-row">📦 Amazon ECR — Container registry</div>
            <div class="cloud-row">⚙️ GitHub Actions — CI/CD deployment</div>
            <div class="cloud-row">🔐 AWS SSM — Secure deployment control</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="side-card">
            <div class="side-title">Production Runtime</div>
            <div class="cloud-row">FastAPI: Port 8000</div>
            <div class="cloud-row">Streamlit: Port 8501</div>
            <div style="color:#4ade80;font-size:.75rem;margin-top:.5rem;">● All services monitored</div>
        </div>
        """,
        unsafe_allow_html=True
    )


journey_df = load_patient_data()
persona_df = load_persona_data()

page_header(
    "CareFlow",
    "IQ",
    "NHS Unscheduled Care Intelligence Platform for clinical, operational and strategic decision support."
)

section_label("Executive Command Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Patients Analysed", f"{len(journey_df):,}", "Journey records")

with c2:
    kpi_card("Journey Segments", f"{journey_df['cluster_name'].nunique()}", "AI-derived groups")

with c3:
    kpi_card("Admission Rate", f"{journey_df['admit_flag'].mean() * 100:.1f}%", "Overall burden")

with c4:
    kpi_card("Production Models", "3", "Admission, operational, policy")


section_label("Platform Intelligence Overview")

narrative_card(
    """
    <b>CareFlow IQ</b> converts unscheduled care pathway data into executive-ready intelligence.
    It combines patient segmentation, pathway analysis, admission prediction, operational pressure
    forecasting, policy prioritisation, SHAP explainability and cloud-based MLOps governance.
    <br><br>
    The platform is deployed as a Dockerised FastAPI and Streamlit application on AWS EC2,
    with model artifacts and data products served from Amazon S3 and automated deployment through GitHub Actions.
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
        Predict admission risk, operational pressure and strategic policy priority using production ML models.
        <br><br>
        <b>Output:</b> risk scores, SHAP drivers and recommended actions.
        """
    )
    st.page_link("pages/predictive_overview.py", label="Launch Predictive Intelligence")

with m3:
    narrative_card(
        """
        <b>Governance Intelligence</b><br><br>
        Show the full cloud production architecture: S3, EC2, ECR, Docker, GitHub Actions, SSM and MLflow.
        <br><br>
        <b>Output:</b> deployment controls, model lifecycle and production traceability.
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


section_label("Key Business Value Delivered")

deliverables = [
    ("Patient Segmentation", "4 Cohorts", "AI-derived pathway groups"),
    ("Predictive Intelligence", "3 Models", "Admission, operational and policy"),
    ("Explainability", "SHAP", "Transparent prediction drivers"),
    ("Pathway Intelligence", "Sankey", "Journey flow analysis"),
    ("Cloud Deployment", "AWS", "EC2, S3, ECR and SSM"),
    ("CI/CD Pipeline", "GitHub Actions", "Automated build and deployment"),
]

cols = st.columns(3)

for idx, item in enumerate(deliverables):
    title, metric, note = item
    with cols[idx % 3]:
        kpi_card(title, metric, note)