import logging
import joblib
import mlflow
import mlflow.sklearn

from mlflow.tracking import MlflowClient

from src.utils.mlflow_config import setup_mlflow

from src.utils.config import (
    MODEL_LOADING_MODE,
    ADMISSION_MODEL_NAME,
    POLICY_MODEL_NAME,
    OPERATIONAL_MODEL_NAME,
    XGB_MODEL_PATH,
    RF_MODEL_PATH,
    LGBM_MODEL_PATH,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_local_model(model_path):
    if not model_path.exists():
        raise FileNotFoundError(
            f"Local model not found at: {model_path}"
        )

    model = joblib.load(model_path)

    logging.info(
        f"Loaded local model from {model_path}"
    )

    return model


def load_registered_model(model_name):
    setup_mlflow()

    client = MlflowClient()

    versions = client.search_model_versions(
        f"name='{model_name}'"
    )

    if not versions:
        raise ValueError(
            f"No registered model found in MLflow: {model_name}"
        )

    latest_version = max(
        versions,
        key=lambda version: int(version.version)
    )

    model_uri = (
        f"models:/{model_name}/{latest_version.version}"
    )

    model = mlflow.sklearn.load_model(model_uri)

    logging.info(
        f"Loaded MLflow model {model_name} v{latest_version.version}"
    )

    return model


def load_admission_model():
    if MODEL_LOADING_MODE == "local":
        return load_local_model(XGB_MODEL_PATH)

    return load_registered_model(ADMISSION_MODEL_NAME)


def load_policy_model():
    if MODEL_LOADING_MODE == "local":
        return load_local_model(RF_MODEL_PATH)

    return load_registered_model(POLICY_MODEL_NAME)


def load_operational_model():
    if MODEL_LOADING_MODE == "local":
        return load_local_model(LGBM_MODEL_PATH)

    return load_registered_model(OPERATIONAL_MODEL_NAME)


def load_all_models():
    return {
        "admission": load_admission_model(),
        "policy": load_policy_model(),
        "operational": load_operational_model(),
    }


if __name__ == "__main__":
    models = load_all_models()

    print("\nLoaded Models")
    print(list(models.keys()))