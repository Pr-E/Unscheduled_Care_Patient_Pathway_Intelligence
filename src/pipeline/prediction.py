from src.clustering.cluster_feature_builder import build_cluster_features
from src.clustering.cluster_predictor import predict_cluster
from src.predictive.predict_patient import predict_admission
from src.predictive.predict_operational import predict_operational
from src.predictive.predict_policy import predict_policy


class PredictionPipeline:

    def __init__(self, patient_data: dict):
        self.patient_data = patient_data.copy()


    def assign_cluster(self):
        cluster_features = build_cluster_features(
            self.patient_data
        )

        cluster_result = predict_cluster(
            **cluster_features
        )

        self.patient_data["cluster_name"] = (
            cluster_result["cluster_name"]
        )

        return cluster_result


    def predict_all(self):
        cluster_result = self.assign_cluster()

        admission_prediction = predict_admission(
            self.patient_data
        )

        operational_prediction = predict_operational(
            self.patient_data
        )

        policy_prediction = predict_policy(
            self.patient_data
        )

        return {
            "patient_profile": self.patient_data,
            "cluster": cluster_result,
            "admission": admission_prediction,
            "operational": operational_prediction,
            "policy": policy_prediction,
        }


if __name__ == "__main__":

    sample_patient = {
        "age": 76,
        "gender": "Female",
        "ethnicity": "Non-Hispanic",
        "race": "White",
        "lang": "English",
        "employstatus": "Retired",
        "insurance_status": "Public",
        "arrivalmode": "Ambulance",
        "arrivalmonth": "January",
        "arrivalday": "Monday",
        "arrivalhour_bin": "Day",
        "previousdispo": "Home",
        "flow_pressure_z": 1.2,
        "clinical_acuity": 4,
        "vitals_documented": 1,
    }

    pipeline = PredictionPipeline(
        sample_patient
    )

    result = pipeline.predict_all()

    print(result)