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
    .exec-card {
        min-height: 210px;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(56, 189, 248, 0.18);
        border-left: 4px solid #fb923c;
        border-radius: 22px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 0 26px rgba(0,0,0,0.16);
    }
    .exec-title {
        color: #f8fafc;
        font-size: 1.05rem;
        font-weight: 900;
        margin-bottom: .65rem;
    }
    .exec-text {
        color: #cbd5e1;
        font-size: .88rem;
        line-height: 1.55;
    }
    .exec-impact {
        color: #94a3b8;
        font-size: .82rem;
        line-height: 1.5;
        margin-top: .7rem;
    }
    .exec-impact b {
        color: #4ade80;
    }

    .objective-card{

        min-height:290px;

        background:linear-gradient(
            145deg,
            rgba(15,23,42,.98),
            rgba(17,24,39,.95)
        );

        border:1px solid rgba(74,222,128,.18);

        border-top:4px solid #fb923c;

        border-radius:22px;

        padding:28px;

        transition:.30s ease;

        margin-bottom:20px;

        box-shadow:0 12px 30px rgba(0,0,0,.22);

        cursor:pointer;

    }

    .objective-card:hover{

        transform:translateY(-8px);

        border-color:#4ade80;

        border-top-color:#4ade80;

        box-shadow:
            0 0 28px rgba(74,222,128,.18),
            0 18px 38px rgba(0,0,0,.35);

        background:linear-gradient(
            145deg,
            rgba(20,30,48,.98),
            rgba(20,83,45,.28)
        );

    }

    .objective-title{

        font-size:1.25rem;

        font-weight:900;

        color:white;

        margin-bottom:20px;

    }

    .objective-heading{

        color:#4ade80;

        font-size:.82rem;

        text-transform:uppercase;

        letter-spacing:.18rem;

        font-weight:800;

        margin-bottom:12px;

    }

    .objective-text{

        color:#e2e8f0;

        font-size:.96rem;

        line-height:1.7;

        margin-bottom:22px;

    }

    .objective-impact{

        color:#94a3b8;

        line-height:1.6;

        font-size:.86rem;

    }

    .objective-impact b{

        color:#fb923c;

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


section_label("Platform Overview")

narrative_card(
    """
    <b>CareFlow IQ</b> is an enterprise healthcare intelligence platform that transforms
    Emergency Department data into clinical, operational and strategic decision support.

    The platform combines patient segmentation, predictive machine learning,
    explainable AI, operational analytics and cloud-native MLOps to provide
    healthcare leaders with proactive intelligence rather than retrospective reporting.

    Through a production-ready architecture built on AWS, Docker, FastAPI,
    Streamlit and GitHub Actions, CareFlow IQ delivers transparent,
    scalable and governable AI for modern unscheduled care services.
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


section_label("Executive Value Proposition")

narrative_card(
    """
    CareFlow IQ enables healthcare organisations to move beyond traditional reporting
    by transforming routine Emergency Department data into actionable intelligence.

    The platform identifies hidden patient pathway variation, predicts admission risk,
    forecasts operational pressure, explains AI-driven recommendations and supports
    evidence-based service redesign through a fully governed production environment.

    This creates a single intelligence platform supporting frontline clinicians,
    operational managers, executives and healthcare policymakers.
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
    CareFlow IQ is built using a retrospective Emergency Department dataset from the
    Yale New Haven Health System comprising over <b>558,000 adult patient encounters</b>
    collected between <b>March 2014 and July 2017</b> across one academic and two
    community Emergency Departments.

    Originally developed to predict hospital admission at triage,
    the dataset has been transformed into a comprehensive intelligence platform
    supporting patient segmentation, predictive analytics,
    explainable AI, operational intelligence,
    strategic planning and enterprise deployment.
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