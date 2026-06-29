import os
import sys
from pathlib import Path
import subprocess

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import boto3
import streamlit as st

from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, narrative_card


st.set_page_config(
    page_title="Model Retraining Center",
    page_icon="🔁",
    layout="wide"
)

load_css()


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv(
    "S3_BUCKET_NAME",
    "unscheduled-care-patient-pathway-intelligence"
)

CLUSTER_ARTIFACT_PREFIX = "cluster-artifacts/"
LOCAL_CLUSTER_DIR = ROOT_DIR / "cluster_data"

REQUIRED_CLUSTER_FILES = [
    "cluster_centroids.csv",
    "cluster_distribution.csv",
    "cluster_features.csv",
    "cluster_metadata.csv",
    "executive_cluster_personas.csv",
    "feature_dictionary.csv",
    "journey_df_engineered.csv",
    "patient_journey_segments.csv",
]


def is_cloud_runtime() -> bool:
    return os.getenv("USE_S3", "false").lower() == "true"


def sync_cluster_artifacts_from_s3() -> None:
    LOCAL_CLUSTER_DIR.mkdir(parents=True, exist_ok=True)

    s3 = boto3.client(
        "s3",
        region_name=AWS_REGION
    )

    for file_name in REQUIRED_CLUSTER_FILES:
        s3_key = f"{CLUSTER_ARTIFACT_PREFIX}{file_name}"
        local_path = LOCAL_CLUSTER_DIR / file_name

        s3.download_file(
            S3_BUCKET_NAME,
            s3_key,
            str(local_path)
        )


def validate_local_cluster_artifacts() -> list:
    missing_files = []

    for file_name in REQUIRED_CLUSTER_FILES:
        local_path = LOCAL_CLUSTER_DIR / file_name

        if not local_path.exists():
            missing_files.append(str(local_path))

    return missing_files


page_header(
    "Model",
    "Retraining Center",
    "Controlled lifecycle management for model refresh, validation, registry update and production readiness."
)


section_label("Current Model Registry Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Admission Model",
        "Random Forest",
        "Patient admission intelligence"
    )

with c2:
    kpi_card(
        "Operational Model",
        "LightGBM",
        "Operational flow intelligence"
    )

with c3:
    kpi_card(
        "Policy Model",
        "XGBoost",
        "Strategic policy intelligence"
    )

with c4:
    kpi_card(
        "Tracking",
        "MLflow + S3",
        "Registry and artifact governance"
    )


section_label("Retraining Workflow")

narrative_card(
    """
    The retraining pipeline runs the full production MLOps workflow using:
    <b>python -m src.pipeline.training</b>.
    <br><br>
    Before training starts, this page synchronises the required cluster artifacts
    from Amazon S3 into the container's local <b>cluster_data</b> directory.
    The pipeline then rebuilds preprocessing, trains Random Forest, LightGBM and XGBoost,
    evaluates performance, registers models in MLflow and uploads refreshed artifacts to S3.
    """
)


section_label("Training Pipeline Controls")

controls = [
    ("S3 Artifact Sync", "Downloads required cluster artifacts from Amazon S3 before training."),
    ("Data Validation", "Checks required modelling features and target columns."),
    ("Preprocessing", "Applies imputation, scaling and one-hot encoding."),
    ("Model Training", "Trains Random Forest, LightGBM and XGBoost."),
    ("Evaluation", "Logs accuracy, precision, recall, F1, ROC AUC and PR AUC."),
    ("Feature Importance", "Generates technical and executive feature-importance artifacts."),
    ("Model Registry", "Registers refreshed models using configured MLflow registry names."),
    ("S3 Backup", "Uploads refreshed models, reports and summaries to Amazon S3."),
]

cols = st.columns(4)

for idx, item in enumerate(controls):
    title, detail = item

    with cols[idx % 4]:
        st.markdown(
            f"""
            <div class="glass-card" style="min-height:145px; margin-bottom:1rem;">
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


section_label("Production Safety Notice")

if is_cloud_runtime():
    narrative_card(
        """
        <b>Cloud runtime detected.</b><br><br>
        This application is running with S3-backed production artifacts.
        Retraining should only be triggered when the dataset, modelling features
        or model governance requirements have changed.
        <br><br>
        The system will first download required cluster artifacts from S3,
        then execute the governed training pipeline.
        """
    )
else:
    narrative_card(
        """
        <b>Local development runtime detected.</b><br><br>
        This page can be used to test the complete training pipeline locally before
        promoting refreshed artifacts to production.
        """
    )


section_label("Production Retraining Trigger")

narrative_card(
    """
    This control executes the project-level training entry point:
    <b>python -m src.pipeline.training</b>.
    <br><br>
    That entry point calls <b>TrainingPipeline</b>, which runs the
    <b>ModellingPipeline</b> inside <b>src.modelling.train_models</b>.
    """
)

confirm = st.checkbox(
    "I understand this will run the full model training pipeline and may update model artifacts."
)

if st.button(
    "Start Full Model Retraining",
    use_container_width=True,
    disabled=not confirm
):
    with st.spinner("Preparing artifacts and retraining all models. This may take several minutes..."):

        try:
            if is_cloud_runtime():
                st.info("Synchronising cluster artifacts from Amazon S3...")
                sync_cluster_artifacts_from_s3()

            missing_files = validate_local_cluster_artifacts()

            if missing_files:
                st.error("Retraining stopped because required local artifacts are still missing.")

                with st.expander("Missing Files"):
                    st.code("\n".join(missing_files))

                st.stop()

            st.success("Cluster artifacts validated. Starting training pipeline...")

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "src.pipeline.training"
                ],
                cwd=str(ROOT_DIR),
                capture_output=True,
                text=True,
                timeout=7200
            )

            if result.returncode == 0:
                st.success("Production retraining completed successfully.")

                s1, s2, s3 = st.columns(3)

                with s1:
                    st.success("✓ Models refreshed")

                with s2:
                    st.success("✓ MLflow registry updated")

                with s3:
                    st.success("✓ S3 artifacts uploaded")

                narrative_card(
                    """
                    <b>Retraining completed.</b><br><br>
                    Random Forest Admission Intelligence, LightGBM Operational Intelligence
                    and XGBoost Policy Intelligence have been refreshed through the governed
                    training pipeline. Review the generated outputs before promoting the
                    refreshed models for production decision support.
                    """
                )

                with st.expander("View Training Output"):
                    st.code(result.stdout or "No standard output returned.")

                if result.stderr:
                    with st.expander("View Warning / Error Stream"):
                        st.code(result.stderr)

            else:
                st.error("Retraining failed.")

                with st.expander("View Error Output"):
                    st.code(result.stderr or "No error output returned.")

                with st.expander("View Training Output"):
                    st.code(result.stdout or "No standard output returned.")

        except subprocess.TimeoutExpired:
            st.error("Retraining timed out after 120 minutes.")

        except Exception as error:
            st.error(f"Retraining failed: {error}")


section_label("Post-Retraining Validation Checklist")

checks = [
    "Confirm required cluster artifacts were downloaded from Amazon S3.",
    "Confirm the latest MLflow runs were created successfully.",
    "Check Random Forest, LightGBM and XGBoost metrics before promotion.",
    "Verify model files were uploaded to the S3 model-registry folders.",
    "Confirm executive feature importance artifacts were regenerated.",
    "Review model_comparison.csv and training_summary.json.",
    "Redeploy or restart the application if refreshed artifacts should be loaded immediately.",
    "Test Admission, Operational and Policy Intelligence pages end-to-end.",
]

for check in checks:
    st.markdown(f"✅ {check}")


section_label("Governance Notes")

narrative_card(
    """
    Model retraining is treated as a governed lifecycle event. A refreshed model should
    only be promoted after validating performance, checking feature-importance stability,
    confirming S3 artifact synchronisation and testing live prediction behaviour across
    the deployed Streamlit and FastAPI layers.
    """
)