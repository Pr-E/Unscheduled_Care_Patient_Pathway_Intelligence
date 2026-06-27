import pandas as pd
import shap

from src.utils.model_loader import (
    load_admission_model
)

from src.models.data_preprocessing import (
    FEATURES
)


def explain_patient(
    patient_data
):

    model = load_admission_model()

    patient_df = pd.DataFrame(
        [patient_data]
    )

    probability = (

        model.predict_proba(
            patient_df
        )[0][1]

    )

    prep = model.named_steps[
        "prep"
    ]

    classifier = model.named_steps[
        "model"
    ]

    transformed = prep.transform(
        patient_df
    )

    feature_names = (

        prep.get_feature_names_out()
    )

    transformed_df = pd.DataFrame(

        transformed,

        columns=feature_names

    )

    explainer = shap.TreeExplainer(
        classifier
    )

    shap_values = explainer.shap_values(
        transformed_df
    )

    if isinstance(
        shap_values,
        list
    ):
        shap_values = shap_values[1]

    return {

        "probability":
            probability,

        "shap_values":
            shap_values,

        "transformed_df":
            transformed_df

    }