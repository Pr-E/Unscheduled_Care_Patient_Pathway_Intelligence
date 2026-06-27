def build_cluster_features(
    patient_data
):

    age_z = (

        patient_data["age"]

        - 60

    ) / 20

    return {

        "age_z":
            age_z,

        "clinical_acuity":
            patient_data[
                "clinical_acuity"
            ],

        "flow_pressure_z":
            patient_data[
                "flow_pressure_z"
            ]

    }