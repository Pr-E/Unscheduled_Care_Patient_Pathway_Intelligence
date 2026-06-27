from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class PatientInput(BaseModel):

    age: int = Field(..., ge=0, le=120)

    gender: str

    ethnicity: str

    race: str

    lang: str = "English"

    employstatus: str

    insurance_status: str

    arrivalmode: str

    arrivalmonth: str

    arrivalday: str

    arrivalhour_bin: str

    previousdispo: str

    flow_pressure_z: float

    clinical_acuity: int = Field(..., ge=1, le=5)

    vitals_documented: int = Field(..., ge=0, le=1)


class ClusterResponse(BaseModel):

    cluster_id: int

    cluster_name: str

    cluster_description: Optional[str] = None

    confidence: float

    cluster_probabilities: Dict[str, float]


class AdmissionResponse(BaseModel):

    probability: float

    risk_level: str


class OperationalResponse(BaseModel):

    probability: float

    pressure: str


class PolicyResponse(BaseModel):

    probability: float

    priority: str


class FullPredictionResponse(BaseModel):

    patient_profile: Dict

    cluster: ClusterResponse

    admission: AdmissionResponse

    operational: OperationalResponse

    policy: PolicyResponse


class HealthResponse(BaseModel):

    status: str

    service: str

    version: str


class DashboardKPIResponse(BaseModel):

    patients: int

    cluster_segments: int

    registered_models: int

    intelligence_layers: List[str]


class GovernanceSummaryResponse(BaseModel):

    platform: str

    records: int

    cluster_segments: int

    registered_models: List[str]

    governance_controls: List[str]