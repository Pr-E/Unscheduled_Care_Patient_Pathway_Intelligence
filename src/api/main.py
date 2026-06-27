import logging

from fastapi import FastAPI

from src.api.routes import router


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


app = FastAPI(
    title="NHS Unscheduled Care Patient Pathway Intelligence API",
    version="1.0.0",
    description="""
    Production API for the NHS Unscheduled Care Patient Pathway
    Intelligence Platform.

    Capabilities:
    - Patient journey segmentation
    - Admission risk prediction
    - Operational pressure prediction
    - Policy redesign priority prediction
    - Dashboard KPI service
    - Governance and model summary service
    - Model retraining endpoint
    """
)


@app.on_event("startup")
def startup_event():
    logging.info("=" * 70)
    logging.info("NHS Unscheduled Care Intelligence API started")
    logging.info("=" * 70)


@app.get("/")
def home():
    return {
        "platform": "NHS Unscheduled Care Patient Pathway Intelligence API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "unscheduled-care-intelligence-api",
        "version": "1.0.0"
    }


@app.get("/info")
def info():
    return {
        "project": "NHS Unscheduled Care Patient Pathway Intelligence",
        "records": 558018,
        "cluster_segments": 4,
        "models": {
            "admission": "XGBoost",
            "operational": "LightGBM",
            "policy": "Random Forest"
        },
        "capabilities": [
            "Patient segmentation",
            "Admission prediction",
            "Operational pressure forecasting",
            "Policy priority prediction",
            "SHAP explainability",
            "Governance intelligence",
            "Model retraining"
        ]
    }


app.include_router(
    router,
    prefix="/api",
    tags=["NHS Intelligence"]
)