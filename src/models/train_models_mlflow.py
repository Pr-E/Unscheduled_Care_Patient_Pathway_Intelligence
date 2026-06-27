import logging
import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score
)

from sklearn.ensemble import (
    RandomForestClassifier
)

from xgboost import (
    XGBClassifier
)

from lightgbm import (
    LGBMClassifier
)

from src.utils.mlflow_config import (
    setup_mlflow
)

from src.models.data_preprocessing import (
    processing_engine,
    create_train_test_split

)

from src.utils.config import (
    MODEL_REGISTRY
)

# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =====================================================
# MLFLOW
# =====================================================

setup_mlflow()

# =====================================================
# DIRECTORIES
# =====================================================

Path(
    "artifacts/models"
).mkdir(
    parents=True,
    exist_ok=True
)

Path(
    "artifacts/reports"
).mkdir(
    parents=True,
    exist_ok=True
)

Path(
    "artifacts/feature_importance"
).mkdir(
    parents=True,
    exist_ok=True
)

# =====================================================
# LOAD DATA
# =====================================================

logging.info(
    "Loading training data..."
)

X, y, patient_df, preprocessor = (
    processing_engine()
)

X_train, X_test, y_train, y_test = (

    create_train_test_split(
        X,
        y
    )

)


dataset_metadata = {

    "training_rows":
        len(X_train),

    "testing_rows":
        len(X_test),

    "feature_count":
        X_train.shape[1],

    "target_positive_rate":
        float(y.mean())

}

# =====================================================
# CLASS BALANCE
# =====================================================

negative_class = (
    y_train == 0
).sum()

positive_class = (
    y_train == 1
).sum()


scale_pos_weight = (

    negative_class /

    max(
        positive_class,
        1
    )

)

logging.info(
    f"Scale Pos Weight: {scale_pos_weight:.2f}"
)

# =====================================================
# EXECUTIVE FEATURE MAPPING
# =====================================================

FEATURE_GROUPS = {

    "age": "Age",

    "gender": "Gender",

    "ethnicity": "Ethnicity",

    "race": "Race",

    "lang": "Language",

    "employstatus": "Employment",

    "insurance_status": "Insurance",

    "arrivalmode": "Arrival Mode",

    "arrivalmonth": "Arrival Month",

    "arrivalday": "Arrival Day",

    "arrivalhour_bin": "Arrival Time",

    "previousdispo": "Previous Disposition",

    "flow_pressure_z": "Flow Pressure",

    "clinical_acuity": "Clinical Acuity",

    "vitals_documented": "Vitals Documentation",

    "cluster_name": "Patient Segment"

}

def executive_feature_mapper(feature):

    feature = str(feature)

    for raw_name, executive_name in FEATURE_GROUPS.items():

        if raw_name in feature:

            return executive_name

    return feature


MODEL_PURPOSES = {

    "XGBoost":
        "Admission Prediction Intelligence",

    "RandomForest":
        "Policy Planning Intelligence",

    "LightGBM":
        "Operational Flow Intelligence"

}


# =====================================================
# MODELS
# =====================================================

models = {

    "RandomForest":

        RandomForestClassifier(

            n_estimators=300,

            max_depth=12,

            class_weight="balanced",

            random_state=42,

            n_jobs=-1

        ),

    "XGBoost":

        XGBClassifier(

            n_estimators=300,

            max_depth=6,

            learning_rate=0.05,

            subsample=0.8,

            colsample_bytree=0.8,

            scale_pos_weight=
                scale_pos_weight,

            random_state=42,

            eval_metric="logloss"

        ),

    "LightGBM":

        LGBMClassifier(

            n_estimators=300,

            learning_rate=0.05,

            class_weight="balanced",

            random_state=42

        )

}

# =====================================================
# TRAINING LOOP
# =====================================================

results = []

best_auc = 0

best_model = None

best_model_name = None

best_run_id = None

for model_name, model in models.items():

    logging.info(
        f"Training {model_name}"
    )

    with mlflow.start_run(
        run_name=model_name
    ):

        pipeline = Pipeline(

            [

                ("prep", preprocessor),

                ("model", model)

            ]

        )

        pipeline.fit(
            X_train,
            y_train
        )


        transformed = (

            pipeline

            .named_steps["prep"]

            .transform(

                X_train.head(100)

            )

        )

        logging.info(

            f"{model_name} "

            f"transformed shape: "

            f"{transformed.shape}"

        )



        predictions = pipeline.predict(
            X_test
        )

        probabilities = pipeline.predict_proba(
            X_test
        )[:, 1]

        metrics = {

            "accuracy":
                accuracy_score(
                    y_test,
                    predictions
                ),

            "precision":

                precision_score(
                    y_test,
                    predictions,
                    zero_division=0
                ),   

            "recall":
                recall_score(
                    y_test,
                    predictions,
                    zero_division=0
                ),

            "f1":
                f1_score(
                    y_test,
                    predictions,
                    zero_division=0
                ),

            "roc_auc":
                roc_auc_score(
                    y_test,
                    probabilities
                ),

            "pr_auc":
                average_precision_score(
                    y_test,
                    probabilities
                )

        }

        for metric_name, value in metrics.items():

            mlflow.log_metric(
                metric_name,
                value
            )

        mlflow.log_param(
            "model_type",
            model_name
        )

        for key, value in dataset_metadata.items():

            mlflow.log_param(
                key,
                value
            )

        mlflow.log_param(

            "business_purpose",

            MODEL_PURPOSES[
                model_name
            ]

        )    


        # ==================================
        # FEATURE IMPORTANCE
        # ==================================

        transformed_names = (

            pipeline

            .named_steps["prep"]

            .get_feature_names_out()

        )


        logging.info(

            f"{model_name} feature count: "

            f"{len(transformed_names)}"

        )

        feature_names_df = pd.DataFrame(

            {

                "feature":
                    transformed_names

            }

        )

        feature_names_path = (

            f"artifacts/reports/"
            f"{model_name}_feature_names.csv"

        )

        feature_names_df.to_csv(

            feature_names_path,

            index=False

        )

        mlflow.log_artifact(
            feature_names_path
        )

        importances = pd.DataFrame(

            {

                "feature":
                    transformed_names,

                "importance":
                    pipeline
                    .named_steps["model"]
                    .feature_importances_

            }

        )


        importances = (

            importances

            .sort_values(
                "importance",
                ascending=False
            )

        )

        technical_path = (

            f"artifacts/feature_importance/"
            f"{model_name}_technical_importance.csv"

        )

        importances.to_csv(
            technical_path,
            index=False
        )

        mlflow.log_artifact(
            technical_path
        )

        executive_importance = (

            importances

            .assign(

                executive_feature=

                importances["feature"]

                .apply(
                    executive_feature_mapper
                )

            )

            .groupby(
                "executive_feature"
            )["importance"]

            .sum()

            .reset_index()

            .sort_values(
                "importance",
                ascending=False
            )

        )

        executive_csv = (

            f"artifacts/feature_importance/"
            f"{model_name}_executive_importance.csv"

        )

        executive_importance.to_csv(

            executive_csv,

            index=False

        )

        mlflow.log_artifact(
            executive_csv
        )

        plt.figure(
            figsize=(10, 6)
        )

        top_features = (

            executive_importance

            .head(15)

            .sort_values(
                "importance"
            )

        )

        plt.barh(

            top_features[
                "executive_feature"
            ],

            top_features[
                "importance"
            ]

        )

        plt.title(
            f"{model_name} Executive Feature Importance"
        )

        plt.tight_layout()

        executive_png = (

            f"artifacts/feature_importance/"
            f"{model_name}_executive_importance.png"

        )

        plt.savefig(
            executive_png
        )

        plt.close()

        mlflow.log_artifact(
            executive_png
        )

        # ==================================
        # REGISTER MODEL
        # ==================================


        registry_name = (
            MODEL_REGISTRY[
                model_name
            ]
        )

        mlflow.sklearn.log_model(

            sk_model=pipeline,

            artifact_path="model",

            registered_model_name=
                registry_name

        )

        logging.info(

            f"{model_name}"

            f" registered as "

            f"{registry_name}"

        )

        # ==================================
        # RESULTS
        # ==================================

        results.append(

            {

                "Model":
                    model_name,

                **metrics

            }

        )

        if metrics["roc_auc"] > best_auc:

            best_auc = metrics["roc_auc"]

            best_model = pipeline

            best_model_name = model_name

            best_run_id = (

                mlflow.active_run()

                .info

                .run_id

            )

# =====================================================
# SAVE REPORT
# =====================================================

results_df = pd.DataFrame(
    results
)

comparison_path = (
    "artifacts/reports/model_comparison.csv"
)

results_df.to_csv(

    comparison_path,

    index=False

)

mlflow.log_artifact(
    comparison_path
)


best_model_metadata = pd.DataFrame(

    [

        {

            "best_model":
                best_model_name,

            "roc_auc":
                best_auc,

            "run_id":
                best_run_id

        }

    ]

)

metadata_path = (

    "artifacts/reports/"
    "best_model_metadata.csv"

)

best_model_metadata.to_csv(

    metadata_path,

    index=False

)

mlflow.log_artifact(
    metadata_path
)


registry_summary = pd.DataFrame(

    [

        {

            "model":
                model,

            "registry":
                registry

        }

        for model, registry

        in MODEL_REGISTRY.items()

    ]

)

registry_path = (

    "artifacts/reports/"
    "model_registry.csv"

)

registry_summary.to_csv(

    registry_path,

    index=False

)

mlflow.log_artifact(
    registry_path
)



# =====================================================
# SAVE BEST MODEL
# =====================================================

joblib.dump(

    best_model,

    "artifacts/models/best_admission_model.pkl"

)

joblib.dump(

    best_model,

    f"artifacts/models/{best_model_name}.pkl"

)


# =====================================================
# SUMMARY
# =====================================================

print(
    "\n===================================="
)

print(
    f"Best Model: {best_model_name}"
)

print(
    f"ROC AUC: {best_auc:.4f}"
)

print(
    f"Run ID: {best_run_id}"
)

print(
    f"Registry: {MODEL_REGISTRY}"
)

print(
    "===================================="
)



if mlflow.active_run():

    mlflow.end_run()

with mlflow.start_run(

    run_name="Training_Summary"

):

    mlflow.log_artifact(
        comparison_path
    )

    mlflow.log_artifact(
        metadata_path
    )

    mlflow.log_artifact(
        registry_path
    )


