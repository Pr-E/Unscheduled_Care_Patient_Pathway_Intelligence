import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


def check_api_health() -> bool:
    try:
        response = requests.get(
            f"{BASE_URL}/health",
            timeout=10
        )
        return response.status_code == 200
    except Exception as error:
        print(f"API health check failed: {error}")
        return False


def predict_all(patient_payload: dict) -> dict:
    response = requests.post(
        f"{BASE_URL}/api/predict/all",
        json=patient_payload,
        timeout=120
    )
    response.raise_for_status()
    return response.json()


def predict_admission(patient_payload: dict) -> dict:
    response = requests.post(
        f"{BASE_URL}/api/predict/admission",
        json=patient_payload,
        timeout=120
    )
    response.raise_for_status()
    return response.json()


def predict_operational(patient_payload: dict) -> dict:
    response = requests.post(
        f"{BASE_URL}/api/predict/operational",
        json=patient_payload,
        timeout=120
    )
    response.raise_for_status()
    return response.json()


def predict_policy(patient_payload: dict) -> dict:
    response = requests.post(
        f"{BASE_URL}/api/predict/policy",
        json=patient_payload,
        timeout=120
    )
    response.raise_for_status()
    return response.json()


def get_dashboard_kpis() -> dict:
    response = requests.get(
        f"{BASE_URL}/api/dashboard/kpis",
        timeout=60
    )
    response.raise_for_status()
    return response.json()


def get_governance_summary() -> dict:
    response = requests.get(
        f"{BASE_URL}/api/governance/model-summary",
        timeout=60
    )
    response.raise_for_status()
    return response.json()


def retrain_models() -> dict:
    response = requests.post(
        f"{BASE_URL}/train",
        timeout=900
    )
    response.raise_for_status()
    return response.json()