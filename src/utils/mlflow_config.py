import os
import mlflow


def setup_mlflow():
    repo_owner = os.getenv("DAGSHUB_REPO_OWNER")
    repo_name = os.getenv("DAGSHUB_REPO_NAME")

    username = os.getenv("MLFLOW_TRACKING_USERNAME")
    token = (
        os.getenv("MLFLOW_TRACKING_PASSWORD")
        or os.getenv("MLFLOW_TOKEN")
        or os.getenv("DAGSHUB_TOKEN")
    )

    if not repo_owner:
        raise ValueError("DAGSHUB_REPO_OWNER is missing.")

    if not repo_name:
        raise ValueError("DAGSHUB_REPO_NAME is missing.")

    if not username:
        raise ValueError("MLFLOW_TRACKING_USERNAME is missing.")

    if not token:
        raise ValueError("MLFLOW_TRACKING_PASSWORD or MLFLOW_TOKEN is missing.")

    tracking_uri = f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"

    os.environ["MLFLOW_TRACKING_USERNAME"] = username
    os.environ["MLFLOW_TRACKING_PASSWORD"] = token
    os.environ["GIT_PYTHON_REFRESH"] = "quiet"

    mlflow.set_tracking_uri(tracking_uri)

    return tracking_uri