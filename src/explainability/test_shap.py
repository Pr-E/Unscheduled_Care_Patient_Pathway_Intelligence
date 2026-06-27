from src.models.data_preprocessing import (
    processing_engine
)

from src.explainability.shap_explainer import (
    generate_shap_values
)

print(
    "\nLoading data..."
)

X, y, patient_df, preprocessor = (
    processing_engine()
)

sample_df = X.sample(

    n=100,

    random_state=42

)

print(
    "Generating SHAP..."
)

shap_values, transformed_df, explainer = (

    generate_shap_values(
        sample_df
    )

)

print(
    "\nSUCCESS"
)

print(
    f"Input Shape: {sample_df.shape}"
)

print(
    f"Transformed Shape: "
    f"{transformed_df.shape}"
)

print(
    f"SHAP Shape: "
    f"{shap_values.shape}"
)