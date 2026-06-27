import json
import logging
from pathlib import Path
from typing import Dict, Optional

import pandas as pd

from src.cloud.s3_storage import S3Storage
from src.utils.config import (
    REQUIRED_CLUSTER_ARTIFACTS,
    CLUSTER_CENTROIDS_PATH,
    CLUSTER_DISTRIBUTION_PATH,
    CLUSTER_FEATURES_PATH,
    CLUSTER_METADATA_PATH,
    EXECUTIVE_CLUSTER_PROFILES_PATH,
    FEATURE_DICTIONARY_PATH,
    JOURNEY_ENGINEERED_PATH,
    PATIENT_JOURNEY_SEGMENTS_PATH,
    S3_BUCKET_NAME,
    USE_S3,
    S3_CLUSTER_ARTIFACT_PREFIX,
    S3_METADATA_PREFIX,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_artifact_path(path: Path, artifact_name: str) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required artifact '{artifact_name}' at: {path}"
        )

    if not path.is_file():
        raise FileNotFoundError(
            f"Artifact path exists but is not a file for '{artifact_name}': {path}"
        )


def validate_all_cluster_artifacts() -> bool:
    logging.info("Validating exported R cluster artifacts...")

    for artifact_name, artifact_path in REQUIRED_CLUSTER_ARTIFACTS.items():
        validate_artifact_path(
            path=artifact_path,
            artifact_name=artifact_name
        )

    logging.info("All required R-exported cluster artifacts are available.")
    return True


def load_csv_artifact(
    path: Path,
    artifact_name: str,
    nrows: Optional[int] = None
) -> pd.DataFrame:
    validate_artifact_path(path, artifact_name)

    dataframe = pd.read_csv(path, nrows=nrows)

    logging.info(
        f"Loaded artifact '{artifact_name}' with shape {dataframe.shape}"
    )

    return dataframe


def load_cluster_centroids() -> pd.DataFrame:
    return load_csv_artifact(CLUSTER_CENTROIDS_PATH, "cluster_centroids")


def load_cluster_distribution() -> pd.DataFrame:
    return load_csv_artifact(CLUSTER_DISTRIBUTION_PATH, "cluster_distribution")


def load_cluster_features() -> pd.DataFrame:
    return load_csv_artifact(CLUSTER_FEATURES_PATH, "cluster_features")


def load_cluster_metadata() -> pd.DataFrame:
    return load_csv_artifact(CLUSTER_METADATA_PATH, "cluster_metadata")


def load_executive_cluster_profiles() -> pd.DataFrame:
    return load_csv_artifact(
        EXECUTIVE_CLUSTER_PROFILES_PATH,
        "executive_cluster_profiles"
    )


def load_feature_dictionary() -> pd.DataFrame:
    return load_csv_artifact(FEATURE_DICTIONARY_PATH, "feature_dictionary")


def load_journey_engineered(nrows: Optional[int] = None) -> pd.DataFrame:
    return load_csv_artifact(
        JOURNEY_ENGINEERED_PATH,
        "journey_df_engineered",
        nrows=nrows
    )


def load_patient_journey_segments(nrows: Optional[int] = None) -> pd.DataFrame:
    return load_csv_artifact(
        PATIENT_JOURNEY_SEGMENTS_PATH,
        "patient_journey_segments",
        nrows=nrows
    )


def load_all_cluster_artifacts(
    sample_large_files: bool = False
) -> Dict[str, pd.DataFrame]:
    validate_all_cluster_artifacts()

    nrows = 1000 if sample_large_files else None

    return {
        "cluster_centroids": load_cluster_centroids(),
        "cluster_distribution": load_cluster_distribution(),
        "cluster_features": load_cluster_features(),
        "cluster_metadata": load_cluster_metadata(),
        "executive_cluster_profiles": load_executive_cluster_profiles(),
        "feature_dictionary": load_feature_dictionary(),
        "journey_df_engineered": load_journey_engineered(nrows=nrows),
        "patient_journey_segments": load_patient_journey_segments(nrows=nrows),
    }


def get_artifact_summary() -> pd.DataFrame:
    summary_rows = []

    for artifact_name, artifact_path in REQUIRED_CLUSTER_ARTIFACTS.items():
        exists = artifact_path.exists()

        file_size_mb = None
        columns = None
        preview_shape = None

        if exists:
            file_size_mb = round(
                artifact_path.stat().st_size / (1024 * 1024),
                3
            )

            preview = pd.read_csv(artifact_path, nrows=5)
            columns = preview.columns.tolist()
            preview_shape = preview.shape

        summary_rows.append({
            "artifact_name": artifact_name,
            "path": str(artifact_path),
            "exists": exists,
            "file_size_mb": file_size_mb,
            "preview_shape": preview_shape,
            "columns": columns,
        })

    return pd.DataFrame(summary_rows)


def upload_cluster_artifacts_to_s3() -> pd.DataFrame:
    validate_all_cluster_artifacts()

    s3 = S3Storage(
        bucket_name=S3_BUCKET_NAME,
        use_local=not USE_S3
    )

    summary_df = get_artifact_summary()

    for artifact_name, artifact_path in REQUIRED_CLUSTER_ARTIFACTS.items():
        s3_key = (
            f"{S3_CLUSTER_ARTIFACT_PREFIX}"
            f"{artifact_path.name}"
        )

        s3.upload_file(
            local_path=str(artifact_path),
            key=s3_key
        )

    s3.upload_dataframe(
        dataframe=summary_df,
        key=f"{S3_METADATA_PREFIX}cluster_artifact_summary.csv"
    )

    s3.upload_json(
        data={
            "artifact_count": len(REQUIRED_CLUSTER_ARTIFACTS),
            "artifacts": list(REQUIRED_CLUSTER_ARTIFACTS.keys()),
            "description": (
                "R-exported production cluster artifacts for the NHS "
                "Unscheduled Care Patient Pathway Intelligence Platform."
            )
        },
        key=f"{S3_METADATA_PREFIX}cluster_artifact_manifest.json"
    )

    logging.info("Cluster artifacts uploaded to S3/local storage.")

    return summary_df


if __name__ == "__main__":
    upload_cluster_artifacts_to_s3()

    print("\nARTIFACT SUMMARY")
    print(get_artifact_summary())