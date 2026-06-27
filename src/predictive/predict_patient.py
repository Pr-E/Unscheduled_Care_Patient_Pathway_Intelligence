import pandas as pd

from src.utils.model_loader import (
    load_admission_model
)


# =====================================================
# ADMISSION PREDICTION
# =====================================================

def predict_admission(
    patient_data: dict
):

    model = load_admission_model()

    # ==========================================
    # SAFETY CHECK
    # ==========================================

    if "cluster_name" not in patient_data:

        patient_data["cluster_name"] = (
            "Unknown"
        )

    patient_df = pd.DataFrame(
        [patient_data]
    )

    probability = (

        model.predict_proba(
            patient_df
        )[0][1]

    )

    # ==========================================
    # RISK BANDING
    # ==========================================


    # Admission
    if probability >= 0.85:
        risk_level = "Very High"
    elif probability >= 0.70:
        risk_level = "High"
    elif probability >= 0.55:
        risk_level = "Moderate"
    else:
        risk_level = "Low"

    return {

        "probability":
            float(probability),

        "risk_level":
            risk_level

    }