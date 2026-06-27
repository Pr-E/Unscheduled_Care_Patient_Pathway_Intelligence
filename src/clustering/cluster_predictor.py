import numpy as np
import pandas as pd

from pathlib import Path

from src.clustering.cluster_mapper import (
    CLUSTER_NAMES,
    CLUSTER_DESCRIPTIONS
)

# =====================================================
# LOAD CENTROIDS
# =====================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

CENTROID_PATH = (

    ROOT_DIR
    / "cluster_data"
    / "cluster_centroids.csv"

)

CENTROIDS = pd.read_csv(
    CENTROID_PATH
)

# =====================================================
# SOFTMAX
# =====================================================

def softmax(values):

    exp_values = np.exp(

        values
        -
        np.max(values)

    )

    return (

        exp_values
        /
        exp_values.sum()

    )

# =====================================================
# Z SCORE HELPER
# =====================================================

def calculate_z_score(
    value,
    mean_value,
    std_value
):

    if std_value == 0:

        return 0

    return (

        value
        -
        mean_value

    ) / std_value

# =====================================================
# CLUSTER PREDICTION
# =====================================================

def predict_cluster(

    age_z,

    clinical_acuity,

    flow_pressure_z

):

    patient_vector = np.array([

        flow_pressure_z,

        clinical_acuity,

        age_z

    ])

    distances = []

    for _, row in CENTROIDS.iterrows():

        centroid_vector = np.array([

            row["flow_pressure_z"],

            row["clinical_acuity"],

            row["age_z"]

        ])

        distance = np.linalg.norm(

            patient_vector
            -
            centroid_vector

        )

        distances.append(
            distance
        )

    distances = np.array(
        distances
    )

    probabilities = softmax(
        -distances
    )

    best_cluster = (

        np.argmax(
            probabilities
        ) + 1

    )

    confidence = float(

        probabilities[
            best_cluster - 1
        ]

    )

    cluster_probabilities = {

        CLUSTER_NAMES[
            idx + 1
        ]:

        round(
            float(prob),
            4
        )

        for idx, prob

        in enumerate(
            probabilities
        )

    }

    return {

        "cluster_id":
            best_cluster,

        "cluster_name":
            CLUSTER_NAMES[
                best_cluster
            ],

        "cluster_description":
            CLUSTER_DESCRIPTIONS[
                best_cluster
            ],

        "confidence":
            confidence,

        "cluster_probabilities":
            cluster_probabilities

    }