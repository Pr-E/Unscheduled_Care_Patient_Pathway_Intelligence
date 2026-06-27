import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.compose import ColumnTransformer

from sklearn.pipeline import Pipeline

from sklearn.preprocessing import OneHotEncoder

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score
)

from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier

from lightgbm import LGBMClassifier


# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    "cluster_data/patient_journey_segments.csv"
)


# =====================================================
# FEATURES
# =====================================================

features = [

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

target = "admit_flag"

X = df[features]

y = df[target]


# =====================================================
# TRAIN TEST SPLIT
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    stratify=y,

    random_state=42

)


# =====================================================
# PREPROCESSING
# =====================================================

categorical_features = [

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

preprocessor = ColumnTransformer(

    transformers=[

        (

            "categorical",

            OneHotEncoder(
                handle_unknown="ignore"
            ),

            categorical_features

        )

    ],

    remainder="passthrough"

)


# =====================================================
# MODELS
# =====================================================

models = {

    "Random Forest":

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
# TRAIN MODELS
# =====================================================

results = []

best_auc = 0

best_model = None

best_model_name = None


for model_name, model in models.items():

    print(f"\nTraining {model_name}...")

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

    predictions = pipeline.predict(
        X_test
    )

    probabilities = pipeline.predict_proba(
        X_test
    )[:, 1]

    metrics = {

        "Model":
            model_name,

        "Accuracy":
            accuracy_score(
                y_test,
                predictions
            ),

        "Precision":
            precision_score(
                y_test,
                predictions
            ),

        "Recall":
            recall_score(
                y_test,
                predictions
            ),

        "F1":
            f1_score(
                y_test,
                predictions
            ),

        "ROC_AUC":
            roc_auc_score(
                y_test,
                probabilities
            ),

        "PR_AUC":
            average_precision_score(
                y_test,
                probabilities
            )

    }

    results.append(
        metrics
    )

    if metrics["ROC_AUC"] > best_auc:

        best_auc = metrics["ROC_AUC"]

        best_model = pipeline

        best_model_name = model_name


# =====================================================
# RESULTS
# =====================================================

results_df = pd.DataFrame(
    results
)

print("\n")
print(results_df)

results_df.to_csv(

    "models/model_comparison.csv",

    index=False

)


# =====================================================
# SAVE BEST MODEL
# =====================================================

joblib.dump(

    best_model,

    "models/best_admission_model.pkl"

)

print("\n")
print(f"Best Model: {best_model_name}")
print(f"Best ROC AUC: {best_auc:.4f}")
print("\nModel Saved Successfully")