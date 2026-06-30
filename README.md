![Python](https://img.shields.io/badge/Python-3.11-blue)

![R](https://img.shields.io/badge/R-4.x-276DC3)

![FastAPI](https://img.shields.io/badge/FastAPI-Production-009688)

![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)

![Docker](https://img.shields.io/badge/Docker-Container-blue)

![AWS](https://img.shields.io/badge/AWS-Cloud-orange)

![MLflow](https://img.shields.io/badge/MLflow-MLOps-blue)

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI/CD-success)

![License](https://img.shields.io/badge/License-MIT-green)

![Healthcare AI](https://img.shields.io/badge/Healthcare-AI-success)

# CareFlow IQ

# Explainable AI for Data-Driven Intelligence in Unscheduled Care

> A production-ready healthcare intelligence platform that transforms emergency department patient journey data into clinical, operational and strategic decision support using Artificial Intelligence, Explainable Machine Learning and Cloud-Native MLOps.

---

## Executive Summary

CareFlow IQ is an end-to-end healthcare intelligence platform developed to improve patient journeys across unscheduled care.

Rather than producing traditional retrospective reports, the platform converts emergency department data into real-time intelligence capable of supporting clinicians, operational managers, service planners and healthcare executives.

The project combines:

- Patient pathway segmentation
- Clinical risk modelling
- Operational intelligence
- Policy intelligence
- Explainable Artificial Intelligence (XAI)
- Cloud-native MLOps
- Executive analytics

into one integrated decision support platform.

The solution demonstrates how machine learning can be responsibly deployed within healthcare using transparent governance, explainability and reproducible cloud deployment.

---

# Dataset

## Source

Department of Emergency Medicine

Yale School of Medicine

New Haven, Connecticut, USA

---

## Original Research

The original retrospective study included every adult Emergency Department attendance between

**March 2014 – July 2017**

across

- One Academic Emergency Department
- Two Community Emergency Departments

within the Yale New Haven Health System.

The original study extracted

**972 clinical, operational and demographic variables**

for every patient encounter.

---

## Original Objective

The original research aimed to

> Predict hospital admission at the point of Emergency Department triage.

This project significantly extends that work into a complete production healthcare intelligence platform.

---

# Project Evolution

The project progressed through six major phases.

```
Raw Clinical Dataset
        │
        ▼
R Analytics & Feature Engineering
        │
        ▼
Patient Journey Segmentation
        │
        ▼
Python Intelligence Platform
        │
        ▼
Explainable Machine Learning
        │
        ▼
Cloud-Native MLOps Deployment
```

---

# Phase 1 — Data Engineering (R)

All exploratory analytics, feature engineering and clustering were developed using **R**.

This stage transformed the original emergency department dataset into a structured intelligence dataset suitable for machine learning.

Major preprocessing activities included

- Missing value handling
- Clinical variable cleaning
- Temporal feature creation
- Operational feature engineering
- Demographic standardisation
- Metadata generation
- Feature dictionary creation
- Patient pathway aggregation
- Cluster dataset generation

The R pipeline exported reusable analytical artefacts consumed later by the Python production platform.

---

# Feature Engineering

Clinical, operational and demographic variables were transformed into intelligence-ready features.

## Demographic Features

- Age
- Gender
- Race
- Ethnicity
- Language
- Employment Status
- Insurance Status

---

## Clinical Features

- Emergency Severity Index (ESI)
- Physiological instability
- Vital sign summaries
- Chief complaint severity
- Previous admission history

---

## Operational Features

- Arrival mode
- Arrival month
- Arrival weekday
- Hour of arrival
- Previous disposition
- Historical utilisation

---

## Engineered Intelligence Features

### Clinical Acuity Score

A composite severity metric combining

- Emergency Severity Index
- Physiological instability
- Clinical presentation severity

```
Clinical Acuity

=

f(
    ESI,
    Physiology,
    Complaint Severity
)
```

---

### Flow Pressure Score

Designed to quantify operational demand using

- Arrival mode
- Temporal demand
- Previous pathway behaviour

```
Flow Pressure

=

f(
Arrival Mode,
Arrival Time,
Previous Disposition
)
```

---

### Physiological Instability

Derived indicators include

- Tachycardia
- Tachypnoea
- Hypotension
- Hypoxia

---

# Patient Journey Segmentation

Rather than analysing all emergency patients as one homogeneous population, the platform applies unsupervised learning to identify clinically meaningful pathway groups.

## Algorithm

K-Means Clustering

---

## Cluster Validation

- Elbow Method
- Silhouette Analysis

---

## Clustering Features

- Clinical Acuity
- Flow Pressure
- Age

---

## Identified Patient Segments

### Community Ambulatory Care

Patients with low clinical acuity and high discharge likelihood who may benefit from ambulatory pathways.

---

### Moderate Complexity Care

Patients requiring additional investigation with mixed admission outcomes.

---

### Acute Ambulance Pathways

Higher-acuity patients arriving predominantly by ambulance with increased operational burden.

---

### Complex Elderly Admissions

Older adults with the greatest admission probability and highest healthcare resource utilisation.

---

The clustering engine exports

- Cluster centroids
- Cluster metadata
- Executive personas
- Cluster distributions
- Feature summaries
- Patient assignments
- Feature dictionaries

These artefacts become reusable intelligence assets throughout the platform.

---

# Python Intelligence Platform

The exported R artefacts are imported into a Python production architecture developed in Visual Studio Code.

Python extends the analytical outputs into an end-to-end decision intelligence system.

---

# Intelligence Modules

## Cluster Intelligence

Provides

- Segment exploration
- Population profiling
- Demographic variation
- Admission burden
- Sankey pathway analysis
- Executive personas

---

## Admission Intelligence

Random Forest

Provides

- Admission probability
- Risk category
- Recommended care pathway
- SHAP explanations
- Executive narrative
- Clinical recommendations

---

## Operational Intelligence

LightGBM

Provides

- Operational pressure prediction
- Capacity intelligence
- Resource demand forecasting
- Executive operational guidance

---

## Policy Intelligence

XGBoost

Provides

- Strategic redesign priority
- Population-level opportunity identification
- Service planning intelligence

---

# Explainable Artificial Intelligence

Every prediction is fully explainable using SHAP.

The platform identifies

- strongest positive drivers

- strongest negative drivers

- patient-level reasoning

- executive summaries

- transparent feature attribution

This enables clinicians and operational leaders to understand **why** predictions were generated.

---

# Production MLOps

The project demonstrates a complete healthcare AI deployment workflow.

## Experiment Tracking

- MLflow

- DagsHub

---

## Model Registry

Production models

- Random Forest

- LightGBM

- XGBoost

are version controlled and registered through MLflow.

---

## Model Retraining

A governed retraining pipeline supports

- Dataset validation

- Preprocessing

- Feature generation

- Model training

- Evaluation

- Model registration

- Artefact publication

---

# Cloud Architecture

The complete platform is deployed using AWS.

## Amazon EC2

Production hosting

---

## Amazon S3

Model artefacts

Cluster artefacts

Reports

Metadata

---

## Amazon ECR

Docker image registry

---

## Docker

Application containerisation

---

## GitHub Actions

Continuous Integration

Continuous Deployment

---

## AWS Systems Manager

Secure deployment automation

---

## FastAPI

Production prediction API

---

## Streamlit

Executive intelligence dashboard

---
# Platform Intelligence Modules

```text
                    CareFlow IQ

            Executive Intelligence Platform
                         │
──────────────────────────────────────────────────

Cluster Intelligence

• Patient Segmentation

• Population Analytics

• Pathway Discovery

──────────────────────────────────────────────────

Admission Intelligence

• Admission Risk

• Recommended Care Pathway

• SHAP Explainability

──────────────────────────────────────────────────

Operational Intelligence

• Flow Pressure

• Capacity Prediction

• Resource Utilisation

──────────────────────────────────────────────────

Policy Intelligence

• Service Redesign

• Population Burden

• Strategic Planning

──────────────────────────────────────────────────

Governance Intelligence

• MLflow

• Model Registry

• AWS Infrastructure

• CI/CD

• Traceability
```
---

# Technology Stack

## Analytics

- R

- Python

---

## Machine Learning

- Scikit-Learn

- Random Forest

- XGBoost

- LightGBM

---

## Explainability

- SHAP

---

## Dashboard

- Streamlit

---

## API

- FastAPI

- Uvicorn

---

## Visualisation

- Plotly

---

## Cloud

- Amazon EC2

- Amazon S3

- Amazon ECR

- AWS Systems Manager

---

## DevOps

- Docker

- GitHub Actions

---

## Governance

- MLflow

- DagsHub

---

# Key Business Value Delivered

## Clinical

✔ Earlier identification of high-risk patients

✔ Explainable admission prediction

✔ Recommended care pathways

✔ Transparent AI-assisted decision support

---

## Operational

✔ Identification of pathway bottlenecks

✔ Flow pressure forecasting

✔ Improved resource planning

✔ Capacity management intelligence

---

## Strategic

✔ Patient segmentation

✔ Population health insight

✔ Admission avoidance opportunities

✔ Service redesign intelligence

---

## Executive

✔ Interactive executive dashboard

✔ AI-generated narratives

✔ Governance reporting

✔ Explainable decision support

---

## Technical

✔ Production-ready MLOps

✔ Cloud deployment

✔ Automated CI/CD

✔ Secure model governance

---

# Repository Structure

```text
CareFlow-IQ/
│
├── .github/
│   └── workflows/
│       └── deploy.yml                 # CI/CD pipeline
│
├── .vscode/                           # VS Code workspace configuration
│
├── app/
│   ├── assets/                        # Images and architecture diagrams
│   ├── pages/                         # Streamlit intelligence pages
│   │   ├── admission_intelligence.py
│   │   ├── cluster_explorer.py
│   │   ├── cluster_overview.py
│   │   ├── governance_intelligence.py
│   │   ├── model_retraining.py
│   │   ├── operational_intelligence.py
│   │   ├── patient_pathways.py
│   │   ├── policy_insights.py
│   │   ├── policy_intelligence.py
│   │   └── predictive_overview.py
│   │
│   ├── ui/                            # Custom UI components
│   ├── utils/                         # Streamlit utilities
│   └── home.py                        # Executive dashboard
│
├── artifacts/
│   ├── models/
│   ├── feature_importance/
│   ├── reports/
│   └── metadata/
│
├── cluster_data/                      # R-generated clustering artefacts
│
├── src/
│   ├── api/                           # FastAPI prediction services
│   ├── artifacts/                     # Artifact management
│   ├── cloud/                         # AWS S3 integration
│   ├── clustering/                    # Cluster loading and processing
│   ├── explainability/                # SHAP explanations
│   ├── intelligence/                  # Executive intelligence engine
│   ├── modelling/                     # Machine learning models
│   ├── models/                        # Model registry
│   ├── pipeline/                      # Training pipeline
│   ├── predictive/                    # Prediction engine
│   ├── utils/                         # Shared utilities
│   └── visualisations/                # Plot generation
│
├── Dockerfile                         # Production container
├── requirements.txt
├── setup.py
├── start.sh
├── LICENSE
├── README.md
└── .gitignore
```

---

# Future Work

Planned extensions include

- Real-time EHR integration

- HL7 FHIR interoperability

- Readmission prediction

- Length-of-stay prediction

- Hospital-at-Home pathway optimisation

- Reinforcement Learning for patient streaming

- Digital Twin simulation

- Fairness monitoring

- Model drift detection

---

# Author

**Priscillia Ejiro**

Health Data Scientist | Machine Learning Engineer | Medical Biochemist

Developing responsible Artificial Intelligence systems that improve healthcare delivery, patient outcomes and operational decision-making.

---

# Acknowledgements

This work extends research conducted using emergency department data from the Department of Emergency Medicine, Yale School of Medicine.

The platform transforms that research into a production-ready healthcare AI system demonstrating modern machine learning, explainable AI and cloud-native MLOps for healthcare.
