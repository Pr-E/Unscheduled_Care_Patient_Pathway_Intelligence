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

st.markdown("""
<style>
.module-card {
    min-height: 300px;
    background: rgba(15, 23, 42, 0.92);
    border: 1px solid rgba(56, 189, 248, 0.18);
    border-left: 4px solid #fb923c;
    border-radius: 22px;
    padding: 1.5rem;
    box-shadow: 0 0 26px rgba(0,0,0,0.16);
    margin-bottom: 0.9rem;
}
.module-title {
    color: #f8fafc;
    font-size: 1.25rem;
    font-weight: 900;
    margin-bottom: 1rem;
}
.module-text {
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.65;
    margin-bottom: 1rem;
}
.module-output {
    color: #94a3b8;
    font-size: 0.86rem;
    line-height: 1.55;
}
.module-output b {
    color: #4ade80;
}
div[data-testid="stPageLink"] a {
    width: 100%;
    justify-content: center;
    background: rgba(15, 23, 42, 0.95);
    border: 1px solid rgba(251, 146, 60, 0.45);
    color: #f8fafc !important;
    padding: 0.8rem;
    border-radius: 14px;
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
<div class="module-card">
<div class="module-title">Cluster Intelligence</div>
<div class="module-text">
Explore AI-derived patient journey groups, population burden, demographic variation and service redesign opportunities across unscheduled care pathways.
</div>
<div class="module-output">
<b>Output:</b> segment profiles, pathway opportunities, cohort-level admission burden and policy insight.
</div>
</div>
""", unsafe_allow_html=True)
    st.page_link("pages/cluster_overview.py", label="Launch Cluster Intelligence", use_container_width=True)

with m2:
    st.markdown("""
<div class="module-card">
<div class="module-title">Predictive Intelligence</div>
<div class="module-text">
Generate admission risk, operational pressure and strategic policy predictions using production-ready machine learning models.
</div>
<div class="module-output">
<b>Output:</b> risk scores, SHAP explanations, executive narratives and recommended interventions.
</div>
</div>
""", unsafe_allow_html=True)
    st.page_link("pages/predictive_overview.py", label="Launch Predictive Intelligence", use_container_width=True)

with m3:
    st.markdown("""
<div class="module-card">
<div class="module-title">Governance Intelligence</div>
<div class="module-text">
Monitor cloud infrastructure, model lifecycle, deployment governance and enterprise AI production controls across the platform.
</div>
<div class="module-output">
<b>Output:</b> cloud runtime, deployment architecture, model governance and production traceability.
</div>
</div>
""", unsafe_allow_html=True)
    st.page_link("pages/governance_intelligence.py", label="Launch Governance Intelligence", use_container_width=True)



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
    {
        "title": "AI Patient Segmentation",
        "metric": "4 Cohorts",
        "note": "Population stratification",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Applied unsupervised machine learning to identify four clinically
        meaningful patient pathway cohorts across more than 550,000
        unscheduled care journeys.
        <br><br>
        <b>Executive Impact</b><br>
        Enables NHS leaders to understand demand by patient type rather
        than total attendances, supporting targeted service redesign,
        pathway optimisation and resource planning.
        """
    },
    {
        "title": "Admission Intelligence",
        "metric": "Random Forest",
        "note": "Patient-level prediction",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Developed a production-ready admission prediction engine capable
        of estimating admission probability for individual patients using
        demographic, clinical and pathway characteristics.
        <br><br>
        <b>Executive Impact</b><br>
        Supports earlier escalation decisions, admission avoidance,
        improved bed management and more proactive clinical intervention.
        """
    },
    {
        "title": "Operational Intelligence",
        "metric": "LightGBM",
        "note": "Service pressure forecasting",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Built an operational intelligence model that predicts service
        pressure across the patient pathway using flow, acuity and
        utilisation indicators.
        <br><br>
        <b>Executive Impact</b><br>
        Helps operational teams anticipate congestion, optimise patient
        flow and improve capacity planning before pressures escalate.
        """
    },
    {
        "title": "Strategic Policy Intelligence",
        "metric": "XGBoost",
        "note": "Population-level prioritisation",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Developed a strategic intelligence model that identifies patient
        populations and pathway characteristics requiring long-term
        service redesign and policy intervention.
        <br><br>
        <b>Executive Impact</b><br>
        Enables evidence-based investment decisions, commissioning
        priorities and sustainable improvements across unscheduled care.
        """
    },
    {
        "title": "Patient Pathway Intelligence",
        "metric": "End-to-End",
        "note": "Journey flow optimisation",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Mapped complete patient journeys from arrival mode through
        pathway segmentation to final disposition, revealing bottlenecks,
        repeated transitions and high-friction care pathways.
        <br><br>
        <b>Executive Impact</b><br>
        Supports pathway redesign, improved streaming decisions,
        reduced delays and more efficient patient movement across
        emergency and urgent care services.
        """
    },
    {
        "title": "Explainable AI",
        "metric": "SHAP",
        "note": "Transparent decision support",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Integrated SHAP explainability to expose the individual clinical
        and operational factors driving every prediction generated by the
        platform.
        <br><br>
        <b>Executive Impact</b><br>
        Improves transparency, clinician confidence, governance,
        accountability and responsible adoption of AI within healthcare.
        """
    },
    {
        "title": "Cloud MLOps Platform",
        "metric": "AWS",
        "note": "Enterprise deployment",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Engineered a cloud-native deployment architecture using Amazon
        EC2, Amazon S3, Amazon ECR, Docker and MLflow for secure model
        storage, versioning and production serving.
        <br><br>
        <b>Executive Impact</b><br>
        Provides a scalable, resilient and production-ready platform
        capable of supporting enterprise healthcare AI deployment.
        """
    },
    {
        "title": "Continuous Delivery",
        "metric": "GitHub Actions",
        "note": "Automated CI/CD",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Implemented an automated CI/CD pipeline that builds, tests,
        containers and deploys the platform directly to AWS whenever
        approved code changes are merged.
        <br><br>
        <b>Executive Impact</b><br>
        Reduces deployment risk, improves release consistency,
        accelerates delivery of model improvements and strengthens
        operational governance.
        """
    },
]

cols = st.columns(3)

for idx, item in enumerate(deliverables):
    with cols[idx % 3]:
        kpi_card(item["title"], item["metric"], item["note"])
        narrative_card(item["detail"])  # Remove f-string and extra markup