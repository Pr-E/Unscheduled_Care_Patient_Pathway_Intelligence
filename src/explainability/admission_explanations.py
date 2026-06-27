import numpy as np

from src.explainability.shap_explainer import (
    generate_shap_values
)

def explain_patient(
    patient_df
):

    shap_values, transformed = (

        generate_shap_values(
            patient_df
        )

    )

    patient_shap = shap_values[0]

    features = transformed.columns

    explanation = []

    contributions = list(

        zip(
            features,
            patient_shap
        )

    )

    contributions = sorted(

        contributions,

        key=lambda x: abs(x[1]),

        reverse=True

    )

    top_factors = contributions[:5]

    for feature, value in top_factors:

        direction = (

            "increased"

            if value > 0

            else "reduced"

        )

        explanation.append(

            f"{feature} {direction} admission risk"

        )

    return explanation