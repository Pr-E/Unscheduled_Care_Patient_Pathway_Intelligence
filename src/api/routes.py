from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    PatientInput,
    FullPredictionResponse,
    DashboardKPIResponse,
    GovernanceSummaryResponse,
)
from src.pipeline.prediction import PredictionPipeline
from src.pipeline.training import TrainingPipeline
from src.artifacts.artifact_loader import (
    load_patient_journey_segments,
    load_executive_cluster_profiles,
)


router = APIRouter()


@router.post(
    "/predict/all",
    response_model=FullPredictionResponse
)
def predict_all(patient: PatientInput):

    try:
        pipeline = PredictionPipeline(
            patient.model_dump()
        )

        return pipeline.predict_all()

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.post("/predict/admission")
def predict_admission_only(patient: PatientInput):

    try:
        result = PredictionPipeline(
            patient.model_dump()
        ).predict_all()

        return result["admission"]

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.post("/predict/operational")
def predict_operational_only(patient: PatientInput):

    try:
        result = PredictionPipeline(
            patient.model_dump()
        ).predict_all()

        return result["operational"]

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.post("/predict/policy")
def predict_policy_only(patient: PatientInput):

    try:
        result = PredictionPipeline(
            patient.model_dump()
        ).predict_all()

        return result["policy"]

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.post("/segment/patient")
def segment_patient(patient: PatientInput):

    try:
        result = PredictionPipeline(
            patient.model_dump()
        ).assign_cluster()

        return result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@router.get(
    "/dashboard/kpis",
    response_model=DashboardKPIResponse
)
def dashboard_kpis():

    journey_df = load_patient_journey_segments()

    return {
        "patients": int(len(journey_df)),
        "cluster_segments": int(journey_df["cluster_name"].nunique()),
        "registered_models": 3,
        "intelligence_layers": [
            "Cluster Intelligence",
            "Patient Pathways",
            "Admission Intelligence",
            "Operational Intelligence",
            "Policy Intelligence",
            "Governance Intelligence",
        ],
    }


@router.get(
    "/governance/model-summary",
    response_model=GovernanceSummaryResponse
)
def governance_model_summary():

    return {
        "platform": "NHS Unscheduled Care Patient Pathway Intelligence Platform",
        "records": 558018,
        "cluster_segments": 4,
        "registered_models": [
            "UnscheduledCare_XGBoost",
            "UnscheduledCare_LightGBM",
            "UnscheduledCare_RandomForest",
        ],
        "governance_controls": [
            "MLflow model registry",
            "DagsHub experiment tracking",
            "S3 artifact storage",
            "SHAP explainability",
            "Feature importance reporting",
            "Prediction traceability",
            "Responsible AI governance dashboard",
        ],
    }


@router.post("/train")
def retrain_models():

    try:
        pipeline = TrainingPipeline()

        result = pipeline.train()

        return {
            "status": "success",
            "message": "Three intelligence models retrained, registered and stored individually.",
            "results": result,
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )