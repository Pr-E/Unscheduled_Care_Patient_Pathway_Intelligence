import os
import mlflow


def setup_mlflow():
    repo_owner = os.getenv("DAGSHUB_REPO_OWNER")
    repo_name = os.getenv("DAGSHUB_REPO_NAME")

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")

    username = os.getenv("MLFLOW_TRACKING_USERNAME")
    password = (
        os.getenv("MLFLOW_TRACKING_PASSWORD")
        or os.getenv("MLFLOW_TOKEN")
        or os.getenv("DAGSHUB_TOKEN")
    )

    if tracking_uri is None:
        if not repo_owner or not repo_name:
            raise ValueError(
                "Missing MLflow configuration. Set either MLFLOW_TRACKING_URI "
                "or DAGSHUB_REPO_OWNER and DAGSHUB_REPO_NAME."
            )

        tracking_uri = f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"

    if username:
        os.environ["MLFLOW_TRACKING_USERNAME"] = username

    if password:
        os.environ["MLFLOW_TRACKING_PASSWORD"] = password

    mlflow.set_tracking_uri(tracking_uri)

    return tracking_uri