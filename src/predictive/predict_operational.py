import pandas as pd

from src.utils.model_loader import load_operational_model


def predict_operational(patient_data: dict):

    model = load_operational_model()

    if "cluster_name" not in patient_data:
        patient_data["cluster_name"] = "Unknown"

    patient_df = pd.DataFrame([patient_data])

    probability = model.predict_proba(patient_df)[0][1]

    # Operational
    if probability >= 0.85:
        pressure = "Critical"
    elif probability >= 0.70:
        pressure = "High"
    elif probability >= 0.55:
        pressure = "Moderate"
    else:
        pressure = "Low"


    return {
        "probability": float(probability),
        "pressure": pressure
    }