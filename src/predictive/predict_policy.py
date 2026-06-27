import pandas as pd

from src.utils.model_loader import load_policy_model


def predict_policy(patient_data: dict):

    model = load_policy_model()

    if "cluster_name" not in patient_data:
        patient_data["cluster_name"] = "Unknown"

    patient_df = pd.DataFrame([patient_data])

    probability = model.predict_proba(patient_df)[0][1]
        
    if probability >= 0.85:
        priority = "Critical"
    elif probability >= 0.70:
        priority = "High"
    elif probability >= 0.55:
        priority = "Moderate"
    else:
        priority = "Low"     

    return {
        "probability": float(probability),
        "priority": priority
    }



