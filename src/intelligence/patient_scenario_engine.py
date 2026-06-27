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
        .replace("cluster_name_", "Patient Segment: ")
        .replace("arrivalmode_", "Arrival Mode: ")
        .replace("previousdispo_", "Previous Disposition: ")
        .replace("insurance_status_", "Insurance: ")
        .replace("employstatus_", "Employment: ")
        .replace("_", " ")
        .title()
    )


def generate_patient_intelligence(patient_data):

    cluster_features = build_cluster_features(patient_data)

    cluster_result = predict_cluster(
        **cluster_features
    )

    patient_record = patient_data.copy()

    patient_record["cluster_name"] = cluster_result[
        "cluster_name"
    ]

    prediction = predict_admission(patient_record)

    explanation = explain_patient(patient_record)

    shap_values = explanation["shap_values"][0]

    transformed_df = explanation["transformed_df"]

    contributions = list(
        zip(
            transformed_df.columns.tolist(),
            shap_values
        )
    )

    contributions = sorted(
        contributions,
        key=lambda x: abs(float(x[1])),
        reverse=True
    )

    top_drivers = [
        clean_feature_name(feature)
        for feature, value in contributions[:5]
    ]

    executive_drivers = []

    for feature, value in contributions[:10]:

        value = float(value)

        executive_drivers.append({

            "feature": clean_feature_name(feature),

            "impact": round(abs(value), 4),

            "direction": (
                "Increase Risk"
                if value > 0
                else "Reduce Risk"
            )
        })

    narrative = generate_admission_narrative(
        probability=prediction["probability"],
        risk_level=prediction["risk_level"],
        cluster_name=cluster_result["cluster_name"],
        top_drivers=top_drivers
    )

    recommendations = generate_admission_recommendations(
        prediction["probability"],
        cluster_result["cluster_name"]
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

        "transformed_df": transformed_df
    }