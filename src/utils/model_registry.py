import tempfile
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn

from src.cloud.s3_storage import S3Storage
from src.utils.mlflow_config import setup_mlflow
from src.utils.config import (
    S3_BUCKET_NAME,
    S3_MODEL_REGISTRY_PREFIX,
    USE_S3,
)


class ModelRegistry:

    def __init__(self):
        setup_mlflow()

        self.s3 = S3Storage(
            bucket_name=S3_BUCKET_NAME,
            use_local=not USE_S3
        )

    def register(
        self,
        model,
        model_name: str,
        params: dict,
        metrics: dict,
        tags: dict = None,
        artifacts: list = None
    ) -> dict:

        tags = tags or {}
        artifacts = artifacts or []

        with mlflow.start_run(
            run_name=model_name,
            tags={
                "model_name": model_name,
                **tags
            }
        ) as run:

            run_id = run.info.run_id

            mlflow.log_params(params)
            mlflow.log_metrics(metrics)

            for artifact_path in artifacts:
                artifact_path = Path(artifact_path)

                if artifact_path.exists():
                    mlflow.log_artifact(str(artifact_path))

            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                registered_model_name=model_name
            )

            with tempfile.TemporaryDirectory() as tmpdir:

                local_model_path = (
                    Path(tmpdir)
                    / f"{model_name}.joblib"
                )

                joblib.dump(
                    model,
                    local_model_path
                )

                s3_key = (
                    f"{S3_MODEL_REGISTRY_PREFIX}"
                    f"{model_name}/"
                    f"{run_id}/"
                    f"{model_name}.joblib"
                )

                s3_uri = self.s3.upload_file(
                    local_path=str(local_model_path),
                    key=s3_key
                )

        return {
            "run_id": run_id,
            "model_name": model_name,
            "s3_uri": s3_uri,
            "metrics": metrics,
        }