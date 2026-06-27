import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import subprocess
import streamlit as st

from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, narrative_card


st.set_page_config(
    page_title="Model Retraining Center",
    page_icon="",
    layout="wide"
)

load_css()

page_header(
    "Model",
    "Retraining Center",
    "Lifecycle management for model freshness, governance, validation and production readiness."
)

section_label("Current Model Registry Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card("Admission Model", "XGBoost", "Admission prediction")

with c2:
    kpi_card("Operational Model", "LightGBM", "Flow pressure intelligence")

with c3:
    kpi_card("Policy Model", "Random Forest", "Service redesign priority")

with c4:
    kpi_card("Tracking", "MLflow", "Registry and artifacts")

section_label("Retraining Workflow")

narrative_card(
    """
    Retraining executes the complete intelligence pipeline: loading patient journey data,
    validating required columns, rebuilding preprocessing, training Random Forest,
    XGBoost and LightGBM models, calculating performance metrics, generating executive
    feature importance artifacts, registering models in MLflow and saving model comparison reports.
    """
)

section_label("Training Pipeline Controls")

controls = [
    ("Data Validation", "Checks required modelling features and target columns."),
    ("Preprocessing", "Applies imputation, scaling and one-hot encoding."),
    ("Model Training", "Trains Random Forest, XGBoost and LightGBM."),
    ("Evaluation", "Logs accuracy, precision, recall, F1, ROC AUC and PR AUC."),
    ("Feature Importance", "Generates technical and executive feature importance."),
    ("Model Registry", "Registers each model using the configured MLflow registry names."),
    ("Best Model Report", "Stores best model metadata and model comparison report."),
    ("Governance Output", "Supports traceability, transparency and reproducibility."),
]

cols = st.columns(4)

for idx, item in enumerate(controls):

    title, detail = item

    with cols[idx % 4]:

        st.markdown(
            f"""
            <div class="glass-card" style="min-height:140px; margin-bottom:1rem;">
                <div style="color:#4ade80; font-weight:800;">
                    {title}
                </div>
                <div style="color:#cbd5e1; font-size:0.82rem; margin-top:0.6rem; line-height:1.45;">
                    {detail}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

section_label("Production Retraining Trigger")

narrative_card(
    """
    Use this button only when the dataset, features or modelling requirements have changed.
    The command runs the same training module used in development:
    <b>python -m src.models.train_models_mlflow</b>.
    """
)

if st.button(
    "Start Full Model Retraining",
    use_container_width=True
):

    with st.spinner(
        "Retraining all models. This may take several minutes..."
    ):

        try:

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "src.models.train_models_mlflow"
                ],
                cwd=str(ROOT_DIR),
                capture_output=True,
                text=True,
                timeout=1800
            )

            if result.returncode == 0:

                st.success(
                    "Retraining completed successfully."
                )

                with st.expander(
                    "View Training Output"
                ):

                    st.code(
                        result.stdout
                    )

            else:

                st.error(
                    "Retraining failed."
                )

                with st.expander(
                    "View Error Output"
                ):

                    st.code(
                        result.stderr
                    )

        except Exception as error:

            st.error(
                f"Retraining failed: {error}"
            )

section_label("Governance Notes")

narrative_card(
    """
    After retraining, validate the latest MLflow runs, compare ROC AUC and PR AUC,
    confirm feature importance stability, and test Admission, Operational and Policy
    Intelligence pages end-to-end before treating the refreshed models as production-ready.
    """
)