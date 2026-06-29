import numpy as np

from src.clustering.cluster_predictor import predict_cluster
from src.clustering.cluster_feature_builder import build_cluster_features
from src.predictive.predict_patient import predict_admission
from src.explainability.patient_explainer import explain_patient
from src.intelligence.admission_narrative import generate_admission_narrative
from src.intelligence.admission_recommendations import generate_admission_recommendations


def clean_feature_name(feature):
    return (
        str(feature)
        .replace("categorical__", "")
        .replace("numerical__", "")
        .replace("cat__", "")
        .replace("num__", "")
        .replace("cluster_name_", "Patient Segment: ")
        .replace("arrivalmode_", "Arrival Mode: ")
        .replace("previousdispo_", "Previous Disposition: ")
        .replace("insurance_status_", "Insurance: ")
        .replace("employstatus_", "Employment: ")
        .replace("arrivalhour_bin_", "Arrival Time: ")
        .replace("arrivalmonth_", "Arrival Month: ")
        .replace("arrivalday_", "Arrival Day: ")
        .replace("clinical_acuity", "Clinical Acuity")
        .replace("flow_pressure_z", "Flow Pressure")
        .replace("vitals_documented", "Vitals Documented")
        .replace("_", " ")
        .title()
    )


def shap_to_scalar(value) -> float:
    arr = np.asarray(value)

    if arr.size == 0:
        return 0.0

    if arr.size == 1:
        return float(arr.reshape(-1)[0])

    return float(np.mean(arr.reshape(-1)))


def extract_shap_vector(explanation: dict):
    shap_values = explanation["shap_values"]

    if isinstance(shap_values, list):
        shap_values = shap_values[-1]

    shap_values = np.asarray(shap_values)

    if shap_values.ndim == 3:
        shap_values = shap_values[0, :, -1]

    elif shap_values.ndim == 2:
        if shap_values.shape[0] == 1:
            shap_values = shap_values[0]
        elif shap_values.shape[1] == 2:
            shap_values = shap_values[:, 1]
        else:
            shap_values = shap_values[0]

    elif shap_values.ndim != 1:
        shap_values = shap_values.reshape(-1)

    return shap_values


def generate_patient_intelligence(patient_data):
    cluster_features = build_cluster_features(patient_data)

    cluster_result = predict_cluster(**cluster_features)

    patient_record = patient_data.copy()
    patient_record["cluster_name"] = cluster_result["cluster_name"]

    prediction = predict_admission(patient_record)
    explanation = explain_patient(patient_record)

    shap_values = extract_shap_vector(explanation)
    transformed_df = explanation["transformed_df"]

    feature_names = transformed_df.columns.tolist()
    min_length = min(len(feature_names), len(shap_values))

    contributions = []

    for feature, value in zip(feature_names[:min_length], shap_values[:min_length]):
        scalar_value = shap_to_scalar(value)
        contributions.append((feature, scalar_value))

    contributions = sorted(
        contributions,
        key=lambda x: abs(x[1]),
        reverse=True
    )

    top_drivers = [
        clean_feature_name(feature)
        for feature, value in contributions[:5]
    ]

    executive_drivers = []

    for feature, value in contributions[:10]:
        executive_drivers.append(
            {
                "feature": clean_feature_name(feature),
                "impact": round(abs(value), 4),
                "direction": "Increase Risk" if value > 0 else "Reduce Risk",
            }
        )

    narrative = generate_admission_narrative(
        probability=prediction["probability"],
        risk_level=prediction["risk_level"],
        cluster_name=cluster_result["cluster_name"],
        top_drivers=top_drivers,
    )

    recommendations = generate_admission_recommendations(
        prediction["probability"],
        cluster_result["cluster_name"],
    )

    return {
        "cluster_name": cluster_result["cluster_name"],
        "cluster_description": cluster_result["cluster_description"],
        "cluster_confidence": cluster_result["confidence"],
        "cluster_probabilities": cluster_result["cluster_probabilities"],
        "probability": prediction["probability"],
        "risk_level": prediction["risk_level"],
        "top_drivers": top_drivers,
        "executive_drivers": executive_drivers,
        "narrative": narrative,
        "recommendations": recommendations,
        "shap_values": shap_values,
        "transformed_df": transformed_df,
    }