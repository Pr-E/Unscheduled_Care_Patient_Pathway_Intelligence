from pathlib import Path
from typing import Optional

import boto3
import pandas as pd
import streamlit as st

from src.utils.config import (
    AWS_REGION,
    S3_BUCKET_NAME,
    USE_S3,
    S3_CLUSTER_ARTIFACT_PREFIX,
    PATIENT_JOURNEY_SEGMENTS_PATH,
    EXECUTIVE_CLUSTER_PROFILES_PATH,
    CLUSTER_DISTRIBUTION_PATH,
    FEATURE_DICTIONARY_PATH,
)


def _download_s3_file(local_path: Path, s3_key: str) -> Path:
    local_path = Path(local_path)

    if local_path.exists():
        return local_path

    if not USE_S3:
        raise FileNotFoundError(
            f"Local artifact not found and USE_S3=false: {local_path}"
        )

    local_path.parent.mkdir(parents=True, exist_ok=True)

    s3 = boto3.client("s3", region_name=AWS_REGION)

    s3.download_file(
        S3_BUCKET_NAME,
        s3_key,
        str(local_path)
    )

    return local_path


def _load_csv(
    local_path: Path,
    s3_key: str,
    nrows: Optional[int] = None
) -> pd.DataFrame:
    resolved_path = _download_s3_file(
        local_path=local_path,
        s3_key=s3_key
    )

    return pd.read_csv(
        resolved_path,
        nrows=nrows
    )


@st.cache_data(show_spinner=False)
def load_patient_data() -> pd.DataFrame:
    return _load_csv(
        local_path=PATIENT_JOURNEY_SEGMENTS_PATH,
        s3_key=f"{S3_CLUSTER_ARTIFACT_PREFIX}patient_journey_segments.csv"
    )


@st.cache_data(show_spinner=False)
def load_persona_data() -> pd.DataFrame:
    return _load_csv(
        local_path=EXECUTIVE_CLUSTER_PROFILES_PATH,
        s3_key=f"{S3_CLUSTER_ARTIFACT_PREFIX}executive_cluster_personas.csv"
    )


@st.cache_data(show_spinner=False)
def load_cluster_distribution() -> pd.DataFrame:
    return _load_csv(
        local_path=CLUSTER_DISTRIBUTION_PATH,
        s3_key=f"{S3_CLUSTER_ARTIFACT_PREFIX}cluster_distribution.csv"
    )


@st.cache_data(show_spinner=False)
def load_feature_dictionary() -> pd.DataFrame:
    return _load_csv(
        local_path=FEATURE_DICTIONARY_PATH,
        s3_key=f"{S3_CLUSTER_ARTIFACT_PREFIX}feature_dictionary.csv"
    )