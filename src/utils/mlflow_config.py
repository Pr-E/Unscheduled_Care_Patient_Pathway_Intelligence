import os

import dagshub
import mlflow
from dotenv import load_dotenv

load_dotenv(override=True)


def setup_mlflow():
    dagshub_token = os.getenv("MLFLOW_TOKEN")

    if not dagshub_token:
        raise ValueError(
            "MLFLOW_TOKEN not found. Please add it to your .env file or GitHub Secrets."
        )

    repo_owner = os.getenv("DAGSHUB_REPO_OWNER", "ejirogoro27")
    repo_name = os.getenv("DAGSHUB_REPO_NAME", "Unscheduled_Care_Patient_Pathway_Intelligence")
    experiment_name = os.getenv("EXPERIMENT_NAME", "unscheduled_care_patient_pathway_intelligence")

    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    dagshub.init(repo_owner=repo_owner, repo_name=repo_name, mlflow=True)

    tracking_uri = f"https://dagshub.com/{repo_owner}/{repo_name}.mlflow"
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)

    return tracking_uri