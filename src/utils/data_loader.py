import streamlit as st
import pandas as pd

from src.utils.config import (
    PATIENT_JOURNEY_SEGMENTS_PATH,
    EXECUTIVE_CLUSTER_PROFILES_PATH,
    CLUSTER_DISTRIBUTION_PATH,
    FEATURE_DICTIONARY_PATH,
)


@st.cache_data
def load_patient_data():
    return pd.read_csv(
        PATIENT_JOURNEY_SEGMENTS_PATH
    )


@st.cache_data
def load_persona_data():
    return pd.read_csv(
        EXECUTIVE_CLUSTER_PROFILES_PATH
    )


@st.cache_data
def load_cluster_distribution():
    return pd.read_csv(
        CLUSTER_DISTRIBUTION_PATH
    )


@st.cache_data
def load_feature_dictionary():
    return pd.read_csv(
        FEATURE_DICTIONARY_PATH
    )