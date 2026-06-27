import shap
import pandas as pd

from src.utils.model_loader import (
    load_admission_model
)

from src.models.data_preprocessing import (
    processing_engine
)


# =====================================================
# LOAD MODEL
# =====================================================

def load_xgb_pipeline():

    return load_admission_model()


# =====================================================
# TRANSFORM FEATURES
# =====================================================

def transform_features(
    dataframe
):

    model = load_xgb_pipeline()

    preprocessor = (

        model.named_steps[
            "prep"
        ]

    )

    transformed = (

        preprocessor.transform(
            dataframe
        )

    )

    feature_names = (

        preprocessor
        .get_feature_names_out()
        .tolist()

    )

    transformed_df = pd.DataFrame(

        transformed,

        columns=feature_names

    )

    return transformed_df


# =====================================================
# GENERATE SHAP
# =====================================================

def generate_shap_values(
    dataframe
):

    model = load_xgb_pipeline()

    transformed_df = transform_features(
        dataframe
    )

    booster = (

        model.named_steps[
            "model"
        ]

    )

    explainer = shap.TreeExplainer(
        booster
    )

    shap_values = (

        explainer.shap_values(
            transformed_df
        )

    )

    return (

        shap_values,

        transformed_df,

        explainer

    )



