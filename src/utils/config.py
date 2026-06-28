from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "cluster_data"
ARTIFACT_DIR = ROOT_DIR / "artifacts"
MODEL_DIR = ARTIFACT_DIR / "models"
REPORTS_DIR = ARTIFACT_DIR / "reports"
FEATURE_IMPORTANCE_DIR = ARTIFACT_DIR / "feature_importance"
LOCAL_STORAGE_DIR = ROOT_DIR / "local_storage"

for directory in [
    DATA_DIR,
    MODEL_DIR,
    REPORTS_DIR,
    FEATURE_IMPORTANCE_DIR,
    LOCAL_STORAGE_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)

CLUSTER_CENTROIDS_PATH = DATA_DIR / "cluster_centroids.csv"
CLUSTER_DISTRIBUTION_PATH = DATA_DIR / "cluster_distribution.csv"
CLUSTER_FEATURES_PATH = DATA_DIR / "cluster_features.csv"
CLUSTER_METADATA_PATH = DATA_DIR / "cluster_metadata.csv"
EXECUTIVE_CLUSTER_PROFILES_PATH = DATA_DIR / "executive_cluster_personas.csv"
FEATURE_DICTIONARY_PATH = DATA_DIR / "feature_dictionary.csv"
JOURNEY_ENGINEERED_PATH = DATA_DIR / "journey_df_engineered.csv"
PATIENT_JOURNEY_SEGMENTS_PATH = DATA_DIR / "patient_journey_segments.csv"

REQUIRED_CLUSTER_ARTIFACTS = {
    "cluster_centroids": CLUSTER_CENTROIDS_PATH,
    "cluster_distribution": CLUSTER_DISTRIBUTION_PATH,
    "cluster_features": CLUSTER_FEATURES_PATH,
    "cluster_metadata": CLUSTER_METADATA_PATH,
    "executive_cluster_personas": EXECUTIVE_CLUSTER_PROFILES_PATH,
    "feature_dictionary": FEATURE_DICTIONARY_PATH,
    "journey_df_engineered": JOURNEY_ENGINEERED_PATH,
    "patient_journey_segments": PATIENT_JOURNEY_SEGMENTS_PATH,
}

XGB_MODEL_PATH = MODEL_DIR / "xgboost.pkl"
LGBM_MODEL_PATH = MODEL_DIR / "lightgbm.pkl"
RF_MODEL_PATH = MODEL_DIR / "random_forest.pkl"

ADMISSION_MODEL_NAME = "UnscheduledCare_XGBoost"
OPERATIONAL_MODEL_NAME = "UnscheduledCare_LightGBM"
POLICY_MODEL_NAME = "UnscheduledCare_RandomForest"

MODEL_REGISTRY = {
    "XGBoost": ADMISSION_MODEL_NAME,
    "LightGBM": OPERATIONAL_MODEL_NAME,
    "RandomForest": POLICY_MODEL_NAME,
}

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

S3_BUCKET_NAME = os.getenv(
    "S3_BUCKET_NAME",
    "unscheduled-care-patient-pathway-intelligence"
)

USE_S3 = os.getenv("USE_S3", "false").lower() == "true"
MODEL_LOADING_MODE = os.getenv("MODEL_LOADING_MODE", "auto").lower()

S3_CLUSTER_ARTIFACT_PREFIX = "cluster-artifacts/"
S3_METADATA_PREFIX = "metadata/"
S3_MODEL_REGISTRY_PREFIX = "model-registry/"