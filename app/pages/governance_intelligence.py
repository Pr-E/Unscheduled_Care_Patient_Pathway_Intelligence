import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st

from src.utils.data_loader import load_patient_data, load_persona_data
from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, narrative_card


st.set_page_config(
    page_title="Governance Intelligence",
    layout="wide"
)

load_css()

ASSET_PATH = ROOT_DIR / "app" / "assets" / "patient_flow.png"

journey_df = load_patient_data()
persona_df = load_persona_data()

page_header(
    "Governance &",
    "Production Intelligence",
    "Enterprise readiness, cloud deployment, model governance, explainability and end-to-end system intelligence."
)


section_label("Production Governance KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Patient Records", f"{len(journey_df):,}", "Training population")

with c2:
    kpi_card("Cluster Segments", f"{persona_df.shape[0]}", "Patient pathway groups")

with c3:
    kpi_card("Registered Models", "3", "Admission, operational, policy")

with c4:
    kpi_card("Cloud Runtime", "AWS EC2", "Dockerised production app")


section_label("Cloud & Deployment Architecture")

cloud_items = [
    ("Data & Artifacts", "Amazon S3", "Secure storage for models, metadata, cluster outputs and feature artifacts."),
    ("Application Hosting", "Amazon EC2", "Production compute runtime serving FastAPI and Streamlit."),
    ("Container Registry", "Amazon ECR", "Versioned Docker image repository for reproducible deployment."),
    ("CI/CD Pipeline", "GitHub Actions", "Automated build, tag, push and deployment on every main branch update."),
    ("Deployment Control", "AWS SSM", "Secure command-based deployment without relying on public GitHub SSH access."),
    ("Runtime Container", "Docker", "Portable application environment exposing FastAPI on 8000 and Streamlit on 8501."),
]

cols = st.columns(3)

for idx, item in enumerate(cloud_items):
    layer, tech, purpose = item

    with cols[idx % 3]:
        st.markdown(
            f"""
            <div class="glass-card" style="min-height:165px; margin-bottom:1rem;">
                <div style="color:#38bdf8; font-size:0.75rem; letter-spacing:0.16rem; text-transform:uppercase; font-weight:800;">
                    {layer}
                </div>
                <div style="color:white; font-size:1.25rem; font-weight:900; margin-top:0.65rem;">
                    {tech}
                </div>
                <div style="color:#cbd5e1; font-size:0.82rem; margin-top:0.6rem; line-height:1.5;">
                    {purpose}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


section_label("Model Governance Architecture")

m1, m2, m3 = st.columns(3)

with m1:
    narrative_card(
        """
        <b>Admission Intelligence</b><br><br>
        <b>Model:</b> Random Forest<br>
        <b>Purpose:</b> Patient-level admission risk prediction.<br>
        <b>Governance value:</b> Supports escalation, senior review and bed planning.
        """
    )

with m2:
    narrative_card(
        """
        <b>Operational Intelligence</b><br><br>
        <b>Model:</b> LightGBM<br>
        <b>Purpose:</b> Operational pressure and flow disruption forecasting.<br>
        <b>Governance value:</b> Supports capacity planning and command-centre readiness.
        """
    )

with m3:
    narrative_card(
        """
        <b>Policy Intelligence</b><br><br>
        <b>Model:</b> XGBoost<br>
        <b>Purpose:</b> Strategic service redesign priority.<br>
        <b>Governance value:</b> Supports admission avoidance, equity monitoring and pathway redesign.
        """
    )


section_label("Cluster Segment Governance")

segment_cols = st.columns(min(4, len(persona_df)))

for idx, (_, row) in enumerate(persona_df.iterrows()):
    with segment_cols[idx % len(segment_cols)]:
        kpi_card(
            row["segment_name"],
            f"{row['patient_pct']:.1f}%",
            f"Admission burden: {row['admission_pct']:.1f}%"
        )


section_label("Technology Stack")

tech_items = [

    ("Primary IDE", "Visual Studio Code",
     "Unified development environment for Python, R, FastAPI, Streamlit, Docker and cloud deployment."),

    ("Statistical Computing",
     "R",
     "Patient pathway segmentation, K-Means clustering, cluster profiling, executive personas and exported analytical artifacts."),

    ("Machine Learning",
     "Python",
     "Feature engineering, predictive modelling, explainability and production inference."),

    ("Version Control",
     "GitHub",
     "Source code management and collaborative development."),

    ("CI/CD",
     "GitHub Actions",
     "Automated Docker build, testing, image publishing and deployment."),

    ("Containerisation",
     "Docker",
     "Portable runtime for production deployment."),

    ("Container Registry",
     "Amazon ECR",
     "Versioned Docker image repository."),

    ("Cloud Runtime",
     "Amazon EC2",
     "Production hosting for FastAPI and Streamlit services."),

    ("Artifact Storage",
     "Amazon S3",
     "Cluster outputs, trained models, metadata, reports and governance artifacts."),

    ("Experiment Tracking",
     "MLflow + DagsHub",
     "Model registry, experiment tracking and lifecycle governance."),

    ("API Serving",
     "FastAPI",
     "Production REST prediction services."),

    ("Executive Dashboard",
     "Streamlit",
     "Interactive healthcare intelligence platform."),

    ("Explainability",
     "SHAP",
     "Model transparency and feature attribution."),

    ("Deployment Control",
     "AWS Systems Manager",
     "Secure server deployment and lifecycle automation.")
]

cols = st.columns(4)

for idx, item in enumerate(tech_items):
    layer, tech, purpose = item

    with cols[idx % 4]:
        st.markdown(
            f"""
            <div class="glass-card" style="min-height:150px; margin-bottom:1rem;">
                <div style="color:#fb923c; font-size:0.75rem; letter-spacing:0.16rem; text-transform:uppercase; font-weight:800;">
                    {layer}
                </div>
                <div style="color:white; font-size:1.18rem; font-weight:900; margin-top:0.65rem;">
                    {tech}
                </div>
                <div style="color:#cbd5e1; font-size:0.82rem; margin-top:0.55rem; line-height:1.45;">
                    {purpose}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


section_label("End-to-End Patient Intelligence Flow")

narrative_card(
    """
    Patient journey data is transformed into engineered pathway features and AI-derived segments.
    Predictive models generate admission, operational and policy intelligence, while SHAP explains
    the drivers behind patient-level decisions. FastAPI serves predictions to the Streamlit command
    centre, with MLflow, Amazon S3 and GitHub Actions providing traceability, artifact governance and
    automated deployment.
    """
)

if ASSET_PATH.exists():
    st.image(str(ASSET_PATH), use_column_width=True)
else:
    st.info("Optional architecture image not found at app/assets/patient_flow.png.")


section_label("Governance Controls")

governance_items = [
    ("Model Registry", "Implemented", "Registered models tracked through MLflow/DagsHub."),
    ("S3 Artifact Storage", "Implemented", "Models, metadata, cluster outputs and reports stored in Amazon S3."),
    ("Docker Image Versioning", "Implemented", "Application images built and stored in Amazon ECR."),
    ("Automated CI/CD", "Implemented", "GitHub Actions rebuilds and redeploys on push to main."),
    ("EC2 Runtime", "Implemented", "FastAPI and Streamlit served from AWS EC2."),
    ("SSM Deployment", "Implemented", "Secure deployment commands executed through AWS Systems Manager."),
    ("Explainability Layer", "Implemented", "SHAP supports transparent patient-level prediction drivers."),
    ("Prediction Traceability", "Implemented", "Patient inputs link to risk, segment, drivers and recommended actions."),
    ("Feature Importance", "Implemented", "Executive and technical importance artifacts generated."),
    ("Retraining Readiness", "Implemented", "Full training pipeline available through governed retraining workflow."),
    ("Health Monitoring", "Implemented", "API health endpoint supports service readiness checks."),
    ("Executive Narrative", "Implemented", "Stakeholder-friendly interpretation generated across intelligence layers."),
]

gcols = st.columns(4)

for idx, item in enumerate(governance_items):
    control, status, description = item

    with gcols[idx % 4]:
        st.markdown(
            f"""
            <div class="glass-card" style="min-height:150px; margin-bottom:1rem;">
                <div style="color:#4ade80; font-weight:900; font-size:1rem;">
                    ✓ {control}
                </div>
                <div style="color:#fb923c; font-size:0.82rem; font-weight:900; margin-top:0.45rem;">
                    {status}
                </div>
                <div style="color:#cbd5e1; font-size:0.8rem; margin-top:0.55rem; line-height:1.45;">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


section_label("Governance Narrative")

narrative_card(
    """
    CareFlow IQ demonstrates a production-ready healthcare AI architecture.
    The platform connects patient-level prediction, pathway segmentation, explainability,
    model lifecycle governance, cloud artifact storage, Dockerised application serving and
    automated CI/CD deployment. This creates a transparent and auditable decision intelligence
    system for safer unscheduled care planning.
    """
)