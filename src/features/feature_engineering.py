import io
import json
import logging
from typing import Dict, Tuple

import numpy as np
import pandas as pd

from src.artifacts.artifact_loader import (
    load_patient_journey_segments
)

from src.utils.config import (
    FEATURE_STORE_DIR,
    PATIENT_FEATURE_STORE_PATH,
    OPERATIONAL_FEATURE_STORE_PATH,
    POLICY_FEATURE_STORE_PATH,
    FEATURE_METADATA_PATH,
    S3_BUCKET_NAME,
    USE_S3,
    S3_PATIENT_FEATURE_KEY,
    S3_OPERATIONAL_FEATURE_KEY,
    S3_POLICY_FEATURE_KEY,
    S3_FEATURE_METADATA_KEY,
)

from src.cloud.s3_storage import S3Storage


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class FeatureEngineering:
    """
    Production feature engineering layer for the NHS Unscheduled Care
    Patient Pathway Intelligence Platform.

    This creates three feature stores:
    1. Patient-level features for admission prediction.
    2. Operational-level features for pressure/flow prediction.
    3. Policy-level features for redesign/service priority prediction.
    """

    def __init__(self):

        self.s3 = S3Storage(
            bucket_name=S3_BUCKET_NAME,
            use_local=not USE_S3
        )

        self.df = None

        FEATURE_STORE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )


    # =====================================================
    # LOAD DATA
    # =====================================================

    def load_data(self) -> pd.DataFrame:

        logging.info(
            "Loading patient journey segment dataset..."
        )

        self.df = load_patient_journey_segments()

        logging.info(
            f"Dataset loaded: {self.df.shape}"
        )

        return self.df


    # =====================================================
    # BASIC CLEANING
    # =====================================================

    def clean_base_data(self) -> pd.DataFrame:

        logging.info(
            "Cleaning base data for feature engineering..."
        )

        dataframe = self.df.copy()

        # ---------------------------------------------
        # Normalize expected column names
        # ---------------------------------------------

        dataframe.columns = [
            column.strip()
            for column in dataframe.columns
        ]

        # ---------------------------------------------
        # Known missing categorical values
        # ---------------------------------------------

        categorical_defaults = {
            "gender": "Unknown",
            "ethnicity": "Unknown",
            "race": "Unknown",
            "lang": "Unknown",
            "employstatus": "Unknown",
            "insurance_status": "Unknown",
            "arrivalmode": "Unknown",
            "arrivalmonth": "Unknown",
            "arrivalday": "Unknown",
            "arrivalhour_bin": "Unknown",
            "previousdispo": "Unknown",
            "cluster_name": "Unknown",
            "disposition": "Unknown",
        }

        for column, default_value in categorical_defaults.items():

            if column in dataframe.columns:

                dataframe[column] = (
                    dataframe[column]
                    .fillna(default_value)
                    .astype(str)
                )

        # ---------------------------------------------
        # Numeric safety
        # ---------------------------------------------

        numeric_defaults = {
            "age": dataframe["age"].median() if "age" in dataframe.columns else 60,
            "clinical_acuity": 3,
            "flow_pressure_z": 0,
            "vitals_documented": 0,
        }

        for column, default_value in numeric_defaults.items():

            if column in dataframe.columns:

                dataframe[column] = pd.to_numeric(
                    dataframe[column],
                    errors="coerce"
                ).fillna(default_value)

        self.df = dataframe

        return self.df


    # =====================================================
    # PATIENT-LEVEL FEATURES
    # =====================================================

    def build_patient_level_features(
        self,
        dataframe: pd.DataFrame
    ) -> Tuple[pd.DataFrame, list]:

        logging.info(
            "Building patient-level engineered features..."
        )

        df = dataframe.copy()

        # ---------------------------------------------
        # Age and frailty style features
        # ---------------------------------------------

        df["age_z"] = (
            df["age"] - 60
        ) / 20

        df["elderly_flag"] = (
            df["age"] >= 75
        ).astype(int)

        df["working_age_flag"] = (
            (df["age"] >= 18)
            & (df["age"] < 65)
        ).astype(int)

        df["age_band"] = pd.cut(
            df["age"],
            bins=[0, 17, 44, 64, 74, 120],
            labels=[
                "Under 18",
                "18-44",
                "45-64",
                "65-74",
                "75+"
            ],
            include_lowest=True
        ).astype(str)

        # ---------------------------------------------
        # Clinical risk features
        # ---------------------------------------------

        df["high_acuity_flag"] = (
            df["clinical_acuity"] >= 4
        ).astype(int)

        df["very_high_acuity_flag"] = (
            df["clinical_acuity"] >= 5
        ).astype(int)

        df["vitals_missing_flag"] = (
            df["vitals_documented"] == 0
        ).astype(int)

        df["vitals_missing_high_acuity"] = (
            (df["vitals_documented"] == 0)
            & (df["clinical_acuity"] >= 4)
        ).astype(int)

        # ---------------------------------------------
        # Pathway history and route features
        # ---------------------------------------------

        df["ambulance_arrival_flag"] = (
            df["arrivalmode"]
            .str.lower()
            .str.contains("ambulance", na=False)
        ).astype(int)

        df["walk_in_flag"] = (
            df["arrivalmode"]
            .str.lower()
            .str.contains("walk", na=False)
        ).astype(int)

        df["previous_admission_flag"] = (
            df["previousdispo"]
            .str.lower()
            .str.contains("admission|admit", na=False)
        ).astype(int)

        df["previous_discharge_flag"] = (
            df["previousdispo"]
            .str.lower()
            .str.contains("home|discharge", na=False)
        ).astype(int)

        # ---------------------------------------------
        # Interaction features
        # ---------------------------------------------

        df["age_acuity_interaction"] = (
            df["age"]
            * df["clinical_acuity"]
        )

        df["flow_acuity_interaction"] = (
            df["flow_pressure_z"]
            * df["clinical_acuity"]
        )

        df["elderly_high_acuity_flag"] = (
            (df["elderly_flag"] == 1)
            & (df["high_acuity_flag"] == 1)
        ).astype(int)

        df["ambulance_high_acuity_flag"] = (
            (df["ambulance_arrival_flag"] == 1)
            & (df["high_acuity_flag"] == 1)
        ).astype(int)

        df["flow_pressure_abs"] = (
            df["flow_pressure_z"]
            .abs()
        )

        df["clinical_operational_stress_score"] = (
            df["clinical_acuity"]
            + df["flow_pressure_abs"]
            + df["ambulance_arrival_flag"]
            + df["vitals_missing_flag"]
        )

        df["admission_complexity_score"] = (
            df["clinical_acuity"]
            + df["elderly_flag"]
            + df["previous_admission_flag"]
            + df["ambulance_arrival_flag"]
            + df["vitals_missing_high_acuity"]
        )

        patient_features = [
            "age",
            "age_z",
            "age_band",
            "elderly_flag",
            "working_age_flag",
            "gender",
            "ethnicity",
            "race",
            "lang",
            "employstatus",
            "insurance_status",
            "arrivalmode",
            "arrivalmonth",
            "arrivalday",
            "arrivalhour_bin",
            "previousdispo",
            "flow_pressure_z",
            "flow_pressure_abs",
            "clinical_acuity",
            "vitals_documented",
            "cluster_name",
            "high_acuity_flag",
            "very_high_acuity_flag",
            "vitals_missing_flag",
            "vitals_missing_high_acuity",
            "ambulance_arrival_flag",
            "walk_in_flag",
            "previous_admission_flag",
            "previous_discharge_flag",
            "age_acuity_interaction",
            "flow_acuity_interaction",
            "elderly_high_acuity_flag",
            "ambulance_high_acuity_flag",
            "clinical_operational_stress_score",
            "admission_complexity_score",
        ]

        patient_features = [
            feature
            for feature in patient_features
            if feature in df.columns
        ]

        if "admit_flag" in df.columns:
            patient_features.append("admit_flag")

        return (
            df[patient_features].copy(),
            patient_features
        )


    # =====================================================
    # OPERATIONAL-LEVEL FEATURES
    # =====================================================

    def build_operational_level_features(
        self,
        dataframe: pd.DataFrame
    ) -> Tuple[pd.DataFrame, list]:

        logging.info(
            "Building operational-level engineered features..."
        )

        df = dataframe.copy()

        # ---------------------------------------------
        # Operational pressure signals
        # ---------------------------------------------

        df["flow_pressure_abs"] = (
            df["flow_pressure_z"]
            .abs()
        )

        df["high_flow_pressure_flag"] = (
            df["flow_pressure_z"] >= 1
        ).astype(int)

        df["low_flow_pressure_flag"] = (
            df["flow_pressure_z"] <= -1
        ).astype(int)

        df["high_acuity_flag"] = (
            df["clinical_acuity"] >= 4
        ).astype(int)

        df["ambulance_arrival_flag"] = (
            df["arrivalmode"]
            .str.lower()
            .str.contains("ambulance", na=False)
        ).astype(int)

        df["transfer_arrival_flag"] = (
            df["arrivalmode"]
            .str.lower()
            .str.contains("transfer", na=False)
        ).astype(int)

        df["vitals_missing_flag"] = (
            df["vitals_documented"] == 0
        ).astype(int)

        # ---------------------------------------------
        # Operational interaction features
        # ---------------------------------------------

        df["flow_acuity_interaction"] = (
            df["flow_pressure_z"]
            * df["clinical_acuity"]
        )

        df["arrival_acuity_pressure_score"] = (
            df["ambulance_arrival_flag"]
            + df["transfer_arrival_flag"]
            + df["high_acuity_flag"]
            + df["flow_pressure_abs"]
        )

        df["escalation_pressure_score"] = (
            df["clinical_acuity"]
            + df["flow_pressure_abs"]
            + df["ambulance_arrival_flag"]
            + df["vitals_missing_flag"]
        )

        df["operational_pressure_flag"] = (
            (
                df["escalation_pressure_score"]
                >= df["escalation_pressure_score"].quantile(0.75)
            )
        ).astype(int)

        operational_features = [
            "age",
            "age_band",
            "gender",
            "race",
            "employstatus",
            "insurance_status",
            "arrivalmode",
            "arrivalmonth",
            "arrivalday",
            "arrivalhour_bin",
            "previousdispo",
            "cluster_name",
            "clinical_acuity",
            "flow_pressure_z",
            "flow_pressure_abs",
            "vitals_documented",
            "high_flow_pressure_flag",
            "low_flow_pressure_flag",
            "high_acuity_flag",
            "ambulance_arrival_flag",
            "transfer_arrival_flag",
            "vitals_missing_flag",
            "flow_acuity_interaction",
            "arrival_acuity_pressure_score",
            "escalation_pressure_score",
            "operational_pressure_flag",
        ]

        operational_features = [
            feature
            for feature in operational_features
            if feature in df.columns
        ]

        return (
            df[operational_features].copy(),
            operational_features
        )


    # =====================================================
    # POLICY-LEVEL FEATURES
    # =====================================================

    def build_policy_level_features(
        self,
        dataframe: pd.DataFrame
    ) -> Tuple[pd.DataFrame, list]:

        logging.info(
            "Building policy-level engineered features..."
        )

        df = dataframe.copy()

        # ---------------------------------------------
        # Core policy signals
        # ---------------------------------------------

        df["elderly_flag"] = (
            df["age"] >= 75
        ).astype(int)

        df["high_acuity_flag"] = (
            df["clinical_acuity"] >= 4
        ).astype(int)

        df["ambulance_arrival_flag"] = (
            df["arrivalmode"]
            .str.lower()
            .str.contains("ambulance", na=False)
        ).astype(int)

        df["public_or_medicaid_flag"] = (
            df["insurance_status"]
            .str.lower()
            .str.contains("public|medicaid", na=False)
        ).astype(int)

        df["unemployed_or_unknown_flag"] = (
            df["employstatus"]
            .str.lower()
            .str.contains("unemployed|unknown", na=False)
        ).astype(int)

        df["previous_admission_flag"] = (
            df["previousdispo"]
            .str.lower()
            .str.contains("admission|admit", na=False)
        ).astype(int)

        df["flow_pressure_abs"] = (
            df["flow_pressure_z"]
            .abs()
        )

        # ---------------------------------------------
        # Policy opportunity scores
        # ---------------------------------------------

        df["equity_monitoring_score"] = (
            df["public_or_medicaid_flag"]
            + df["unemployed_or_unknown_flag"]
        )

        df["frailty_policy_score"] = (
            df["elderly_flag"]
            + df["high_acuity_flag"]
            + df["previous_admission_flag"]
        )

        df["urgent_flow_redesign_score"] = (
            df["ambulance_arrival_flag"]
            + df["high_acuity_flag"]
            + df["flow_pressure_abs"]
        )

        df["policy_burden_score"] = (
            df["frailty_policy_score"]
            + df["urgent_flow_redesign_score"]
            + df["equity_monitoring_score"]
        )

        df["policy_priority_flag"] = (
            df["policy_burden_score"]
            >= df["policy_burden_score"].quantile(0.75)
        ).astype(int)

        policy_features = [
            "age",
            "age_band",
            "gender",
            "ethnicity",
            "race",
            "employstatus",
            "insurance_status",
            "arrivalmode",
            "previousdispo",
            "arrivalmonth",
            "arrivalday",
            "arrivalhour_bin",
            "cluster_name",
            "clinical_acuity",
            "flow_pressure_z",
            "flow_pressure_abs",
            "vitals_documented",
            "elderly_flag",
            "high_acuity_flag",
            "ambulance_arrival_flag",
            "public_or_medicaid_flag",
            "unemployed_or_unknown_flag",
            "previous_admission_flag",
            "equity_monitoring_score",
            "frailty_policy_score",
            "urgent_flow_redesign_score",
            "policy_burden_score",
            "policy_priority_flag",
        ]

        policy_features = [
            feature
            for feature in policy_features
            if feature in df.columns
        ]

        return (
            df[policy_features].copy(),
            policy_features
        )


    # =====================================================
    # SAVE FEATURE STORES
    # =====================================================

    def save_local_feature_stores(
        self,
        patient_df: pd.DataFrame,
        operational_df: pd.DataFrame,
        policy_df: pd.DataFrame,
        metadata: Dict
    ) -> None:

        FEATURE_STORE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        patient_df.to_csv(
            PATIENT_FEATURE_STORE_PATH,
            index=False
        )

        operational_df.to_csv(
            OPERATIONAL_FEATURE_STORE_PATH,
            index=False
        )

        policy_df.to_csv(
            POLICY_FEATURE_STORE_PATH,
            index=False
        )

        with open(
            FEATURE_METADATA_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

        logging.info(
            "Local feature stores saved successfully."
        )


    def upload_feature_stores_to_s3(
        self,
        patient_df: pd.DataFrame,
        operational_df: pd.DataFrame,
        policy_df: pd.DataFrame,
        metadata: Dict
    ) -> None:

        self.s3.upload_dataframe(
            dataframe=patient_df,
            key=S3_PATIENT_FEATURE_KEY
        )

        self.s3.upload_dataframe(
            dataframe=operational_df,
            key=S3_OPERATIONAL_FEATURE_KEY
        )

        self.s3.upload_dataframe(
            dataframe=policy_df,
            key=S3_POLICY_FEATURE_KEY
        )

        self.s3.upload_json(
            data=metadata,
            key=S3_FEATURE_METADATA_KEY
        )

        logging.info(
            "Feature stores uploaded to S3/local storage successfully."
        )


    # =====================================================
    # RUN PIPELINE
    # =====================================================

    def run(self):

        self.load_data()

        self.clean_base_data()

        patient_df, patient_features = (
            self.build_patient_level_features(
                self.df
            )
        )

        operational_df, operational_features = (
            self.build_operational_level_features(
                patient_df
            )
        )

        policy_df, policy_features = (
            self.build_policy_level_features(
                patient_df
            )
        )

        metadata = {
            "patient_level_features": patient_features,
            "operational_level_features": operational_features,
            "policy_level_features": policy_features,
            "patient_level_shape": patient_df.shape,
            "operational_level_shape": operational_df.shape,
            "policy_level_shape": policy_df.shape,
            "description": (
                "Production feature stores for NHS Unscheduled Care "
                "Patient Pathway Intelligence."
            )
        }

        self.save_local_feature_stores(
            patient_df=patient_df,
            operational_df=operational_df,
            policy_df=policy_df,
            metadata=metadata
        )

        self.upload_feature_stores_to_s3(
            patient_df=patient_df,
            operational_df=operational_df,
            policy_df=policy_df,
            metadata=metadata
        )

        print("\n" + "=" * 80)
        print("FEATURE ENGINEERING COMPLETE")
        print("=" * 80)
        print(f"Patient-level feature store: {patient_df.shape}")
        print(f"Operational-level feature store: {operational_df.shape}")
        print(f"Policy-level feature store: {policy_df.shape}")
        print(f"Patient features: {len(patient_features)}")
        print(f"Operational features: {len(operational_features)}")
        print(f"Policy features: {len(policy_features)}")

        return {
            "patient_df": patient_df,
            "operational_df": operational_df,
            "policy_df": policy_df,
            "metadata": metadata,
        }


if __name__ == "__main__":

    pipeline = FeatureEngineering()

    pipeline.run()