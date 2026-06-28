from pathlib import Path

import boto3
import joblib

from src.utils.config import (
    AWS_REGION,
    S3_BUCKET_NAME,
    USE_S3,
    MODEL_LOADING_MODE,
    XGB_MODEL_PATH,
    LGBM_MODEL_PATH,
    RF_MODEL_PATH,
)


MODEL_S3_KEYS = {
    "admission": "model-registry/RandomForest/RandomForest.pkl",
    "operational": "model-registry/LightGBM/LightGBM.pkl",
    "policy": "model-registry/XGBoost/XGBoost.pkl",
}


def _should_use_s3(local_path: Path) -> bool:
    if MODEL_LOADING_MODE == "s3":
        return True

    if MODEL_LOADING_MODE == "local":
        return False

    return USE_S3 and not Path(local_path).exists()


def _download_model_from_s3(model_type: str, local_path: Path) -> Path:
    local_path = Path(local_path)

    if local_path.exists():
        return local_path

    local_path.parent.mkdir(parents=True, exist_ok=True)

    s3 = boto3.client("s3", region_name=AWS_REGION)

    s3.download_file(
        S3_BUCKET_NAME,
        MODEL_S3_KEYS[model_type],
        str(local_path)
    )

    return local_path


def _load_model(model_type: str, local_path: Path):
    local_path = Path(local_path)

    if _should_use_s3(local_path):
        local_path = _download_model_from_s3(model_type, local_path)

    if not local_path.exists():
        raise FileNotFoundError(f"Model artifact not found: {local_path}")

    return joblib.load(local_path)


def load_admission_model():
    return _load_model("admission", RF_MODEL_PATH)


def load_operational_model():
    return _load_model("operational", LGBM_MODEL_PATH)


def load_policy_model():
    return _load_model("policy", XGB_MODEL_PATH)