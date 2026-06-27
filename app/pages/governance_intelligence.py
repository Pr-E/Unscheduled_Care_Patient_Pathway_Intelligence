import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

BASE_DIR = Path(__file__).resolve().parents[1]

ASSET_PATH = BASE_DIR / "assets" / "patient_flow.png"

import streamlit as st

from utils.styling import load_css
from utils.ui_components import (
    page_header,
    section_label,
    kpi_card,
    narrative_card
)


st.set_page_config(
    page_title="Governance Intelligence",
    page_icon="",
    layout="wide"
)

load_css()

ASSET_PATH = (
    ROOT_DIR
    / "app"
    / "assets"
    / "patient_flow.png"
)

page_header(
    "Governance &",
    "Production Intelligence",
    "Enterprise readiness, explainability, model lifecycle governance and end-to-end system intelligence."
)

section_label("Production Governance KPIs")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Patient Records",
        "558,018",
        "Training and intelligence population"
    )

with c2:
    kpi_card(
        "Cluster Segments",
        "4",
        "Patient pathway groups"
    )

with c3:
    kpi_card(
        "Registered Models",
        "3",
        "Admission, operational, policy"
    )

with c4:
    kpi_card(
        "Explainability",
        "SHAP",
        "Transparent prediction drivers"
    )


section_label("Cluster Segment Governance")

s1, s2, s3, s4 = st.columns(4)

with s1:
    kpi_card(
        "Community Ambulatory Care",
        "32.7%",
        "Largest population segment"
    )

with s2:
    kpi_card(
        "Moderate Complexity Care",
        "23.8%",
        "Mixed-acuity pathway"
    )

with s3:
    kpi_card(
        "Acute Ambulance Pathways",
        "22.7%",
        "Emergency access burden"
    )

with s4:
    kpi_card(
        "Complex Elderly Admissions",
        "20.8%",
        "Highest admission burden"
    )


section_label("End-to-End Patient Intelligence Flow")

narrative_card(
    """
    This flow shows how the platform moves from patient journey data
    into clustering, pathway intelligence, policy insight, predictive
    modelling, explainability, governance controls and executive-ready
    decision outputs.
    """
)

if ASSET_PATH.exists():

    st.image(
        str(ASSET_PATH),
        use_column_width=True
    )

else:

    st.warning(
        "patient_flow.png not found. Save the generated image inside app/assets/patient_flow.png"
    )


section_label("Technology Stack")

tech_items = [
    ("Development", "VS Code", "Production development environment"),
    ("Data Processing", "Pandas / NumPy", "Patient journey preparation"),
    ("Feature Engineering", "Python Pipeline", "Clinical, operational and segment features"),
    ("Model Training", "RF / XGB / LGBM", "Three-model predictive intelligence layer"),
    ("Experiment Tracking", "MLflow + DagsHub", "Metrics, artifacts and model registry"),
    ("Explainability", "SHAP", "Transparent local driver intelligence"),
    ("Dashboard", "Streamlit", "Executive intelligence interface"),
    ("Deployment Ready", "FastAPI / Docker", "Production API and container pathway"),
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
                <div style="color:white; font-size:1.22rem; font-weight:800; margin-top:0.65rem;">
                    {tech}
                </div>
                <div style="color:#cbd5e1; font-size:0.82rem; margin-top:0.55rem; line-height:1.45;">
                    {purpose}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


section_label("Governance Controls")

governance_items = [
    ("Model Registry", "Implemented", "Registered models tracked through MLflow."),
    ("Experiment Tracking", "Implemented", "Metrics, parameters and artifacts logged."),
    ("Feature Importance", "Implemented", "Executive and technical feature importance artifacts generated."),
    ("Explainability Layer", "Implemented", "SHAP supports transparent patient-level predictions."),
    ("Prediction Traceability", "Implemented", "Prediction links patient features to risk, drivers and actions."),
    ("Retraining Readiness", "Implemented", "Training pipeline supports model refresh and registration."),
    ("Executive Narrative", "Implemented", "Stakeholder-friendly interpretation generated across layers."),
    ("Governance Dashboard", "Implemented", "Production flow and controls visible in Streamlit."),
]

g1, g2, g3, g4 = st.columns(4)

for idx, item in enumerate(governance_items):

    control, status, description = item

    with [g1, g2, g3, g4][idx % 4]:

        st.markdown(
            f"""
            <div class="glass-card" style="min-height:145px; margin-bottom:1rem;">
                <div style="color:#4ade80; font-weight:800; font-size:1rem;">
                    ✓ {control}
                </div>
                <div style="color:#fb923c; font-size:0.82rem; font-weight:800; margin-top:0.45rem;">
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
    The governance layer demonstrates how the platform moves from raw patient journey data
    to accountable intelligence. Each prediction is connected to a registered model,
    explainability drivers, segment intelligence, recommended actions and model lifecycle controls.
    This supports transparency, auditability and responsible AI use in healthcare decision-making.
    """
)