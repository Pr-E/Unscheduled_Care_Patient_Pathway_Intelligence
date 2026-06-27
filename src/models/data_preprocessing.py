import logging
import pandas as pd

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.impute import (
    SimpleImputer
)

from sklearn.model_selection import (
    train_test_split
)

# =====================================================
# LOGGING
# =====================================================

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"

)

# =====================================================
# CONFIG
# =====================================================

DATA_PATH = (
    "cluster_data/patient_journey_segments.csv"
)

TARGET = "admit_flag"

# =====================================================
# FEATURES
# =====================================================

FEATURES = [

    "age",

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

    "clinical_acuity",

    "vitals_documented",

    "cluster_name"

]

# =====================================================
# FEATURE GROUPS
# =====================================================

CATEGORICAL_FEATURES = [

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

    "cluster_name"

]

NUMERICAL_FEATURES = [

    "age",

    "flow_pressure_z",

    "clinical_acuity",

    "vitals_documented"

]

# =====================================================
# DATA INGESTION
# =====================================================

def data_ingestion():

    try:

        logging.info(
            "Loading patient pathway dataset..."
        )

        dataframe = pd.read_csv(
            DATA_PATH
        )

        logging.info(
            f"Dataset Loaded: {dataframe.shape}"
        )

        return dataframe

    except Exception as e:

        logging.error(
            f"Data Ingestion Error: {e}"
        )

        raise


# =====================================================
# DATA VALIDATION
# =====================================================

def data_validation(
    dataframe
):

    try:

        logging.info(
            "Validating dataset..."
        )

        required_columns = (

            FEATURES

            + [TARGET]

        )

        missing_columns = [

            column

            for column

            in required_columns

            if column not in dataframe.columns

        ]

        if missing_columns:

            raise ValueError(

                f"Missing Columns: "
                f"{missing_columns}"

            )

        # =================================
        # HANDLE KNOWN MISSING VALUES
        # =================================

        dataframe["arrivalmode"] = (

            dataframe["arrivalmode"]

            .fillna(
                "Unknown"
            )

        )

        dataframe["race"] = (

            dataframe["race"]

            .fillna(
                "Unknown"
            )

        )

        logging.info(
            "Dataset validation completed"
        )

        return dataframe

    except Exception as e:

        logging.error(
            f"Validation Error: {e}"
        )

        raise


# =====================================================
# PREPROCESSOR
# =====================================================

def build_preprocessor():

    try:

        logging.info(
            "Building preprocessing pipeline..."
        )

        numeric_pipeline = Pipeline(

            steps=[

                (

                    "imputer",

                    SimpleImputer(
                        strategy="median"
                    )

                ),

                (

                    "scaler",

                    StandardScaler()

                )

            ]

        )

        categorical_pipeline = Pipeline(

            steps=[

                (

                    "imputer",

                    SimpleImputer(
                        strategy="most_frequent"
                    )

                ),

                (

                    "encoder",

                    OneHotEncoder(

                        handle_unknown="ignore",

                        sparse_output=False

                    )

                )

            ]

        )

        preprocessor = ColumnTransformer(

            transformers=[

                (

                    "categorical",

                    categorical_pipeline,

                    CATEGORICAL_FEATURES

                ),

                (

                    "numerical",

                    numeric_pipeline,

                    NUMERICAL_FEATURES

                )

            ]

        )

        logging.info(
            "Preprocessor created successfully"
        )

        return preprocessor

    except Exception as e:

        logging.error(
            f"Preprocessor Error: {e}"
        )

        raise


# =====================================================
# PROCESSING ENGINE
# =====================================================

def processing_engine():

    try:

        patient_df = (
            data_ingestion()
        )

        patient_df = (
            data_validation(
                patient_df
            )
        )

        X = patient_df[
            FEATURES
        ]

        y = patient_df[
            TARGET
        ]

        preprocessor = (
            build_preprocessor()
        )

        logging.info(
            "Processing pipeline completed"
        )

        return (

            X,

            y,

            patient_df,

            preprocessor

        )

    except Exception as e:

        logging.error(
            f"Processing Engine Error: {e}"
        )

        raise


# =====================================================
# TRAIN TEST SPLIT
# =====================================================

def create_train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42

):

    return train_test_split(

        X,

        y,

        stratify=y,

        test_size=test_size,

        random_state=random_state

    )


# =====================================================
# FEATURE NAMES
# =====================================================

def get_feature_names(

    fitted_preprocessor

):

    return (

        fitted_preprocessor

        .get_feature_names_out()

        .tolist()

    )


# =====================================================
# EXECUTION TEST
# =====================================================

if __name__ == "__main__":

    X, y, patient_df, preprocessor = (

        processing_engine()

    )

    print("\nFeature Sample")

    print(
        X.head()
    )

    print("\nTarget Sample")

    print(
        y.head()
    )

    print("\nDataset Shape")

    print(
        patient_df.shape
    )

    print("\nPreprocessor Ready")

    print(
        preprocessor
    )