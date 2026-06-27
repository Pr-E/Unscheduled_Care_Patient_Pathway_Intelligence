from mlflow.tracking import MlflowClient

from src.utils.mlflow_config import (
    setup_mlflow
)

setup_mlflow()

client = MlflowClient()

models = client.search_registered_models()

print("\nREGISTERED MODELS\n")

for model in models:

    print(

        f"Name: {model.name}"

    )

    print(
        "-" * 50
    )