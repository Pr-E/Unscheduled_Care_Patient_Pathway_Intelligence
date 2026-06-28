import json
import logging
from datetime import datetime

import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
)
from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from src.artifacts.artifact_loader import upload_cluster_artifacts_to_s3
from src.cloud.s3_storage import S3Storage
from src.models.data_preprocessing import (
    processing_engine,
    create_train_test_split,
)
from src.utils.model_registry import ModelRegistry
from src.utils.config import (
    MODEL_REGISTRY,
    MODEL_DIR,
    REPORTS_DIR,
    FEATURE_IMPORTANCE_DIR,
    XGB_MODEL_PATH,
    RF_MODEL_PATH,
    LGBM_MODEL_PATH,
    S3_BUCKET_NAME,
    USE_S3,
    S3_MODEL_REGISTRY_PREFIX,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


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
    "cluster_name": "Patient Segment",
}


MODEL_PURPOSES = {
    "RandomForest": "Admission Intelligence",
    "LightGBM": "Operational Intelligence",
    "XGBoost": "Policy Intelligence",
}


LOCAL_MODEL_PATHS = {
    "RandomForest": RF_MODEL_PATH,
    "LightGBM": LGBM_MODEL_PATH,
    "XGBoost": XGB_MODEL_PATH,
}



def executive_feature_mapper(feature):

    feature = str(feature)

    for raw_name, executive_name in FEATURE_GROUPS.items():

        if raw_name in feature:
            return executive_name

    return "Other Factors"


class ModellingPipeline:

    def __init__(self):

        self.s3 = S3Storage(
            bucket_name=S3_BUCKET_NAME,
            use_local=not USE_S3
        )

        self.registry = ModelRegistry()

        MODEL_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        REPORTS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        FEATURE_IMPORTANCE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.results = []


    def load_data(self):

        logging.info(
            "Loading base training data from processing engine..."
        )

        X, y, patient_df, preprocessor = processing_engine()

        X_train, X_test, y_train, y_test = create_train_test_split(
            X,
            y
        )

        dataset_metadata = {
            "training_rows": len(X_train),
            "testing_rows": len(X_test),
            "feature_count": X_train.shape[1],
            "target_positive_rate": float(y.mean()),
            "source": "R-exported patient_journey_segments.csv",
        }

        return (
            X_train,
            X_test,
            y_train,
            y_test,
            preprocessor,
            dataset_metadata
        )


    def get_scale_pos_weight(self, y_train):

        negative_class = (
            y_train == 0
        ).sum()

        positive_class = (
            y_train == 1
        ).sum()

        return negative_class / max(
            positive_class,
            1
        )


    def build_models(self, scale_pos_weight):

        return {
            "XGBoost": XGBClassifier(
                n_estimators=300,
                max_depth=6,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=scale_pos_weight,
                random_state=42,
                eval_metric="logloss"
            ),

            "LightGBM": LGBMClassifier(
                n_estimators=300,
                learning_rate=0.05,
                class_weight="balanced",
                random_state=42
            ),

            "RandomForest": RandomForestClassifier(
                n_estimators=300,
                max_depth=12,
                class_weight="balanced",
                random_state=42,
                n_jobs=-1
            ),
        }


    def evaluate(self, pipeline, X_test, y_test):

        predictions = pipeline.predict(
            X_test
        )

        probabilities = (
            pipeline.predict_proba(
                X_test
            )[:, 1]
        )

        return {
            "accuracy": accuracy_score(
                y_test,
                predictions
            ),
            "precision": precision_score(
                y_test,
                predictions,
                zero_division=0
            ),
            "recall": recall_score(
                y_test,
                predictions,
                zero_division=0
            ),
            "f1": f1_score(
                y_test,
                predictions,
                zero_division=0
            ),
            "roc_auc": roc_auc_score(
                y_test,
                probabilities
            ),
            "pr_auc": average_precision_score(
                y_test,
                probabilities
            ),
        }


    def save_feature_importance(self, pipeline, model_name):

        feature_names = (
            pipeline
            .named_steps["prep"]
            .get_feature_names_out()
        )

        estimator = pipeline.named_steps[
            "model"
        ]

        importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": estimator.feature_importances_
        }).sort_values(
            "importance",
            ascending=False
        )

        technical_csv = (
            FEATURE_IMPORTANCE_DIR
            / f"{model_name}_technical_importance.csv"
        )

        importance_df.to_csv(
            technical_csv,
            index=False
        )

        executive_importance = (
            importance_df
            .assign(
                executive_feature=importance_df["feature"].apply(
                    executive_feature_mapper
                )
            )
            .groupby("executive_feature")["importance"]
            .sum()
            .reset_index()
            .sort_values(
                "importance",
                ascending=False
            )
        )

        executive_csv = (
            FEATURE_IMPORTANCE_DIR
            / f"{model_name}_executive_importance.csv"
        )

        executive_importance.to_csv(
            executive_csv,
            index=False
        )

        executive_png = (
            FEATURE_IMPORTANCE_DIR
            / f"{model_name}_executive_importance.png"
        )

        top_features = (
            executive_importance
            .head(15)
            .sort_values("importance")
        )

        plt.figure(
            figsize=(10, 6)
        )

        plt.barh(
            top_features["executive_feature"],
            top_features["importance"]
        )

        plt.title(
            f"{model_name} Executive Feature Importance"
        )

        plt.tight_layout()

        plt.savefig(
            executive_png
        )

        plt.close()

        self.s3.upload_file(
            str(technical_csv),
            f"{S3_MODEL_REGISTRY_PREFIX}{model_name}/technical_importance.csv"
        )

        self.s3.upload_file(
            str(executive_csv),
            f"{S3_MODEL_REGISTRY_PREFIX}{model_name}/executive_importance.csv"
        )

        self.s3.upload_file(
            str(executive_png),
            f"{S3_MODEL_REGISTRY_PREFIX}{model_name}/executive_importance.png"
        )

        return (
            importance_df,
            executive_importance,
            technical_csv,
            executive_csv,
            executive_png
        )


    def train_single_model(
        self,
        model_name,
        estimator,
        preprocessor,
        X_train,
        X_test,
        y_train,
        y_test,
        dataset_metadata
    ):

        registered_model_name = MODEL_REGISTRY[
            model_name
        ]

        logging.info(
            f"Training {model_name} for {MODEL_PURPOSES[model_name]}..."
        )

        pipeline = Pipeline([
            (
                "prep",
                preprocessor
            ),
            (
                "model",
                estimator
            )
        ])

        pipeline.fit(
            X_train,
            y_train
        )

        metrics = self.evaluate(
            pipeline,
            X_test,
            y_test
        )

        (
            importance_df,
            executive_importance,
            technical_csv,
            executive_csv,
            executive_png
        ) = self.save_feature_importance(
            pipeline,
            model_name
        )

        local_model_path = LOCAL_MODEL_PATHS[
            model_name
        ]

        joblib.dump(
            pipeline,
            local_model_path
        )

        self.s3.upload_file(
            str(local_model_path),
            f"{S3_MODEL_REGISTRY_PREFIX}{model_name}/{model_name}.pkl"
        )

        model_summary = {
            "model": model_name,
            "registered_model_name": registered_model_name,
            "business_purpose": MODEL_PURPOSES[model_name],
            "training_date": datetime.now().isoformat(),
            "local_model_path": str(local_model_path),
            "technical_importance_csv": str(technical_csv),
            "executive_importance_csv": str(executive_csv),
            "executive_importance_png": str(executive_png),
            "metrics": metrics,
            "dataset_metadata": dataset_metadata,
            "top_technical_features": (
                importance_df
                .head(15)
                .to_dict(orient="records")
            ),
            "top_executive_features": (
                executive_importance
                .head(15)
                .to_dict(orient="records")
            ),
        }

        summary_path = (
            REPORTS_DIR
            / f"{model_name}_model_summary.json"
        )

        with open(
            summary_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                model_summary,
                file,
                indent=4,
                default=str
            )

        self.s3.upload_file(
            str(summary_path),
            f"{S3_MODEL_REGISTRY_PREFIX}{model_name}/model_summary.json"
        )

        registry_result = self.registry.register(
            model=pipeline,
            model_name=registered_model_name,
            params=estimator.get_params(),
            metrics=metrics,
            tags={
                "model_family": model_name,
                "business_purpose": MODEL_PURPOSES[model_name],
                "stage": "production_candidate",
                "dataset": "nhs_unscheduled_care"
            },
            artifacts=[
                technical_csv,
                executive_csv,
                executive_png,
                summary_path
            ]
        )

        result_row = {
            "Model": model_name,
            "registered_model_name": registered_model_name,
            "business_purpose": MODEL_PURPOSES[model_name],
            "local_model_path": str(local_model_path),
            "feature_importance_png": str(executive_png),
            "run_id": registry_result["run_id"],
            "s3_uri": registry_result["s3_uri"],
            **metrics,
        }

        self.results.append(
            result_row
        )

        print("\n" + "=" * 80)
        print(f"{model_name.upper()} RESULTS")
        print("=" * 80)

        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")

        return pipeline


    def save_training_summary(self):

        results_df = pd.DataFrame(
            self.results
        )

        comparison_path = (
            REPORTS_DIR
            / "model_comparison.csv"
        )

        results_df.to_csv(
            comparison_path,
            index=False
        )

        self.s3.upload_file(
            str(comparison_path),
            f"{S3_MODEL_REGISTRY_PREFIX}model_comparison.csv"
        )

        summary_json = {
            "training_date": datetime.now().isoformat(),
            "registered_models": self.results,
            "note": (
                "No single best model is selected. "
                "Each model is retained because each serves a distinct "
                "intelligence layer: Admission, Operational and Policy."
            )
        }

        summary_path = (
            REPORTS_DIR
            / "training_summary.json"
        )

        with open(
            summary_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                summary_json,
                file,
                indent=4,
                default=str
            )

        self.s3.upload_file(
            str(summary_path),
            f"{S3_MODEL_REGISTRY_PREFIX}training_summary.json"
        )

        print("\n" + "=" * 80)
        print("TRAINING PIPELINE COMPLETE")
        print("=" * 80)
        print("Models saved, registered and backed up individually:")
        print("- XGBoost Admission model")
        print("- LightGBM Operational model")
        print("- Random Forest Policy model")


    def run(self):

        upload_cluster_artifacts_to_s3()

        (
            X_train,
            X_test,
            y_train,
            y_test,
            preprocessor,
            dataset_metadata
        ) = self.load_data()

        scale_pos_weight = self.get_scale_pos_weight(
            y_train
        )

        models = self.build_models(
            scale_pos_weight
        )

        for model_name, estimator in models.items():

            self.train_single_model(
                model_name=model_name,
                estimator=estimator,
                preprocessor=preprocessor,
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
                dataset_metadata=dataset_metadata
            )

        self.save_training_summary()

        return self.results


if __name__ == "__main__":

    pipeline = ModellingPipeline()

    pipeline.run()