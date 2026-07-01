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

LOGO_PATH = ROOT_DIR / "app" / "assets" / "care_logo.png"

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
    .objective-card {
        min-height: 185px;
        background: linear-gradient(145deg, rgba(15,23,42,.96), rgba(8,47,73,.42));
        border: 1px solid rgba(56,189,248,.20);
        border-radius: 22px;
        padding: 1.25rem 1.35rem;
        margin-bottom: 1rem;
        box-shadow: 0 10px 28px rgba(0,0,0,.18);
        transition: all .25s ease-in-out;
        position: relative;
        overflow: hidden;
    }

    .objective-label {
        color: #fb923c;
        font-size: .72rem;
        text-transform: uppercase;
        letter-spacing: .18rem;
        font-weight: 900;
        margin-bottom: .75rem;
    }

    .objective-title {
        color: #f8fafc;
        font-size: 1.3rem;
        font-weight: 900;
        margin-bottom: .85rem;
    }

    .objective-text {
        color: #cbd5e1;
        font-size: .9rem;
        line-height: 1.55;
    }

    .module-card {
        min-height: 310px;
        background: linear-gradient(145deg, rgba(15,23,42,.96), rgba(2,6,23,.94));
        border: 1px solid rgba(56,189,248,.22);
        border-left: 4px solid #fb923c;
        border-radius: 24px;
        padding: 1.55rem;
        box-shadow: 0 14px 34px rgba(0,0,0,.20);
        margin-bottom: 1rem;
        transition: all .25s ease-in-out;
        cursor: pointer;
    }

    .module-card:hover {
        transform: translateY(-6px);
        border-color: rgba(74,222,128,.85);
        border-left-color: #4ade80;
        box-shadow:
            0 0 0 1px rgba(74,222,128,.25),
            0 0 34px rgba(74,222,128,.22),
            0 18px 40px rgba(0,0,0,.28);
        background: linear-gradient(145deg, rgba(15,23,42,.98), rgba(20,83,45,.34));
    }

    .module-card:hover .module-title {
        color: #4ade80;
    }

    .module-card:hover .module-output b {
        color: #fb923c;
    }

    .module-title {
        color: #f8fafc;
        font-size: 1.28rem;
        font-weight: 900;
        margin-bottom: 1rem;
        transition: color .25s ease-in-out;
    }

    .module-text {
        color: #cbd5e1;
        font-size: .95rem;
        line-height: 1.65;
        margin-bottom: 1rem;
    }

    .module-output {
        color: #94a3b8;
        font-size: .86rem;
        line-height: 1.55;
    }

    .module-output b {
        color: #4ade80;
        transition: color .25s ease-in-out;
    }

    div[data-testid="stPageLink"] a {
        width: 100%;
        justify-content: center;
        background: rgba(15, 23, 42, 0.95);
        border: 1px solid rgba(251, 146, 60, 0.45);
        color: #f8fafc !important;
        padding: .85rem;
        border-radius: 15px;
        font-weight: 850;
        transition: all .25s ease-in-out;
    }

    div[data-testid="stPageLink"] a:hover {
        background: rgba(20,83,45,.42);
        border-color: rgba(74,222,128,.85);
        color: #ffffff !important;
        transform: translateY(-3px);
        box-shadow:
            0 0 0 1px rgba(74,222,128,.18),
            0 0 24px rgba(74,222,128,.18);
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:

    if LOGO_PATH.exists():
        st.markdown(
            """
            <div style="
                border:1px solid rgba(56,189,248,.25);
                border-radius:22px;
                padding:0.75rem;
                background:linear-gradient(135deg, rgba(15,23,42,.95), rgba(8,47,73,.65));
                box-shadow:0 0 28px rgba(56,189,248,.12);
                margin-bottom:1rem;
            ">
            """,
            unsafe_allow_html=True
        )

        st.image(str(LOGO_PATH), use_column_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown(
            """
            <div class="side-card">
                <div style="font-size:1.55rem;font-weight:900;color:white;">
                    CareFlow <span style="color:#fb923c;">IQ</span>
                </div>
                <div style="color:#94a3b8;font-size:.76rem;margin-top:.35rem;">
                    Intelligent Care. Better Outcomes.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### NHS UNSCHEDULED CARE")
    st.caption("Clinical, operational and strategic intelligence")

    st.divider()

    api_online = check_api_health()

    st.markdown(
        f"""
        <div class="side-card">
            <div class="side-title">API Status</div>
            <div class="{ 'status-online' if api_online else 'status-offline' }">
                { '● ONLINE' if api_online else '● OFFLINE' }
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
            <div class="cloud-row">Amazon S3 — Model/artifact storage</div>
            <div class="cloud-row">Amazon EC2 — Application runtime</div>
            <div class="cloud-row">Amazon ECR — Container registry</div>
            <div class="cloud-row">GitHub Actions — CI/CD deployment</div>
            <div class="cloud-row">AWS SSM — Secure deployment control</div>
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


section_label("Current Problems in Unscheduled Care")

problem_items = [
    {
        "title": "Rising Emergency Demand",
        "text": """
        Emergency Departments face sustained growth in attendances driven by ageing populations,
        multimorbidity, ambulance demand, constrained primary care access and increased clinical complexity.
        """,
        "impact": """
        <b>Business Impact:</b> overcrowding, delayed admissions, reduced patient flow,
        poorer experience and increased operational cost.
        """
    },
    {
        "title": "Fragmented Patient Pathways",
        "text": """
        Patients with very different clinical needs can experience similar operational journeys,
        making it difficult to stream patients into the most appropriate care pathway early.
        """,
        "impact": """
        <b>Business Impact:</b> unnecessary admissions, longer waiting times,
        inefficient resource utilisation and hidden pathway variation.
        """
    },
    {
        "title": "Reactive Decision-Making",
        "text": """
        Operational teams often respond after pressure has already developed, rather than using
        predictive signals to anticipate risk, flow disruption and capacity pressure.
        """,
        "impact": """
        <b>Business Impact:</b> delayed escalation, weaker bed planning,
        reduced resilience and higher pressure on staff.
        """
    },
    {
        "title": "Limited Intelligence from Routine Data",
        "text": """
        Healthcare systems collect large volumes of data, but it is often used for retrospective
        reporting rather than proactive patient-level, operational and strategic intelligence.
        """,
        "impact": """
        <b>Business Impact:</b> missed redesign opportunities, limited visibility of demand drivers
        and slower evidence-based decision-making.
        """
    },
]

pcols = st.columns(4)

for idx, item in enumerate(problem_items):
    with pcols[idx % 4]:
        st.markdown(
            f"""
            <div class="exec-card">
                <div class="exec-title">{item["title"]}</div>
                <div class="exec-text">{item["text"]}</div>
                <div class="exec-impact">{item["impact"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


section_label("Project Objectives")

objectives = [
    ("Patient Segmentation", "Identify clinically and operationally distinct patient pathway groups."),
    ("Admission Prediction", "Predict inpatient admission risk using triage and pathway-level features."),
    ("Operational Intelligence", "Forecast pressure signals that may affect patient flow and escalation."),
    ("Policy Intelligence", "Identify service redesign priorities and population-level improvement opportunities."),
    ("Explainable AI", "Use SHAP to explain patient-level and model-level prediction drivers."),
    ("Production MLOps", "Deploy a governed, cloud-ready AI platform with CI/CD and retraining capability."),
]

ocols = st.columns(3)

for idx, item in enumerate(objectives):
    title, detail = item

    with ocols[idx % 3]:
        st.markdown(
            f"""
            <div class="objective-card">
                <div class="objective-label">Strategic Objective</div>
                <div class="objective-title">{title}</div>
                <div class="objective-text">{detail}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


section_label("Strategic Objectives")

narrative_card(
    """
    The strategic objective of <b>CareFlow IQ</b> is to move unscheduled care analytics
    from retrospective reporting into proactive, explainable and operationally useful
    decision intelligence.
    <br><br>
    The platform supports healthcare stakeholders by identifying hidden patient journey
    segments, predicting admission risk, surfacing operational pressure, recommending
    care pathways, and providing transparent evidence for service redesign, escalation
    planning and admission avoidance.
    """
)


section_label("Clinical Data Source")

d1, d2, d3, d4 = st.columns(4)

with d1:
    kpi_card("Health System", "Yale New Haven", "Emergency care dataset")

with d2:
    kpi_card("ED Encounters", "558,018", "Adult visits analysed")

with d3:
    kpi_card("Study Period", "2014–2017", "March 2014 to July 2017")

with d4:
    kpi_card("Original Variables", "972", "Per patient encounter")

narrative_card(
    """
    The source dataset comes from a retrospective study of adult Emergency Department visits
    across the <b>Yale New Haven Health System</b>, including one academic and two community
    Emergency Departments.
    <br><br>
    The original study was affiliated with the <b>Department of Emergency Medicine,
    Yale School of Medicine, New Haven, Connecticut, USA</b>, and was designed to predict
    hospital admission at the time of Emergency Department triage.
    <br><br>
    CareFlow IQ extends that original admission-prediction objective into a broader
    intelligence platform covering segmentation, prediction, explainability, operational
    pressure, policy insight, governance and cloud deployment.
    """
)


section_label("Intelligence Modules")

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-title">Cluster Intelligence</div>
            <div class="module-text">
                Explore AI-derived patient journey groups, population burden,
                demographic variation and service redesign opportunities across
                unscheduled care pathways.
            </div>
            <div class="module-output">
                <b>Output:</b> segment profiles, pathway opportunities,
                cohort-level admission burden and policy insight.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link(
        "pages/cluster_overview.py",
        label="Launch Cluster Intelligence",
        use_container_width=True
    )

with m2:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-title">Predictive Intelligence</div>
            <div class="module-text">
                Generate admission risk, operational pressure and strategic policy
                predictions using production-ready machine learning models.
            </div>
            <div class="module-output">
                <b>Output:</b> risk scores, SHAP explanations, executive narratives
                and recommended interventions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link(
        "pages/predictive_overview.py",
        label="Launch Predictive Intelligence",
        use_container_width=True
    )

with m3:
    st.markdown(
        """
        <div class="module-card">
            <div class="module-title">Governance Intelligence</div>
            <div class="module-text">
                Monitor cloud infrastructure, model lifecycle, deployment governance
                and enterprise AI production controls across the platform.
            </div>
            <div class="module-output">
                <b>Output:</b> cloud runtime, deployment architecture,
                model governance and production traceability.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link(
        "pages/governance_intelligence.py",
        label="Launch Governance Intelligence",
        use_container_width=True
    )


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
        Applied unsupervised machine learning to identify four clinically meaningful
        patient pathway cohorts across more than 550,000 unscheduled care journeys.
        <br><br>
        <b>Executive Impact</b><br>
        Enables leaders to understand demand by patient type rather than total attendances,
        supporting targeted service redesign and resource planning.
        """
    },
    {
        "title": "Admission Intelligence",
        "metric": "Random Forest",
        "note": "Patient-level prediction",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Developed a production-ready admission prediction engine estimating admission
        probability using demographic, clinical and pathway characteristics.
        <br><br>
        <b>Executive Impact</b><br>
        Supports escalation, admission avoidance, bed management and proactive clinical intervention.
        """
    },
    {
        "title": "Operational Intelligence",
        "metric": "LightGBM",
        "note": "Pressure forecasting",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Built an operational intelligence model that predicts pressure signals using flow,
        acuity and utilisation indicators.
        <br><br>
        <b>Executive Impact</b><br>
        Helps teams anticipate congestion, optimise flow and plan capacity before pressures escalate.
        """
    },
    {
        "title": "Policy Intelligence",
        "metric": "XGBoost",
        "note": "Strategic prioritisation",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Developed a strategic intelligence model identifying patient populations and pathways
        requiring redesign and policy intervention.
        <br><br>
        <b>Executive Impact</b><br>
        Enables evidence-based investment decisions, commissioning priorities and sustainable improvement.
        """
    },
    {
        "title": "Explainable AI",
        "metric": "SHAP",
        "note": "Transparent decisions",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Integrated SHAP explainability to expose the clinical and operational factors driving predictions.
        <br><br>
        <b>Executive Impact</b><br>
        Improves transparency, clinician confidence, accountability and responsible AI governance.
        """
    },
    {
        "title": "Cloud MLOps Platform",
        "metric": "AWS",
        "note": "Enterprise deployment",
        "detail": """
        <b>Business Value Delivered</b><br><br>
        Engineered a cloud-native platform using EC2, S3, ECR, Docker, MLflow and GitHub Actions.
        <br><br>
        <b>Executive Impact</b><br>
        Provides a scalable, resilient and production-ready healthcare AI deployment architecture.
        """
    },
]

cols = st.columns(3)

for idx, item in enumerate(deliverables):
    with cols[idx % 3]:
        kpi_card(item["title"], item["metric"], item["note"])
        narrative_card(item["detail"])