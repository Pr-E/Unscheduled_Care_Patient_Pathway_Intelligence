# Unscheduled Care Patient Pathway Intelligence Platform

## Overview

The NHS Unscheduled Care Patient Pathway Intelligence Platform is an end-to-end healthcare analytics and machine learning system designed to identify, explain, and optimise emergency and unscheduled care pathways.

The platform combines patient journey segmentation, clinical acuity modelling, operational flow analytics, explainable machine learning, and executive-level visualisation to support data-driven service redesign and policy decision-making.

Using over 550,000 emergency department encounters, the project identifies distinct patient pathway archetypes, uncovers drivers of admission, and provides actionable insights for healthcare leaders, operational managers, and policymakers.

---

## Problem Statement

Emergency departments face increasing pressure from:

* Rising patient demand
* Complex clinical presentations
* Delayed admissions and discharge processes
* Resource constraints
* Variability in patient pathways

Traditional reporting focuses on aggregate metrics and often fails to reveal how different patient groups interact with the healthcare system.

This project addresses that challenge by:

* Discovering hidden patient pathway segments
* Quantifying clinical and operational risk
* Explaining admission decisions
* Identifying opportunities for pathway redesign

---

## Project Objectives

### Patient Journey Segmentation

Identify clinically and operationally distinct patient populations using unsupervised machine learning.

### Pathway Discovery

Understand how patients move through unscheduled care pathways.

### Operational Intelligence

Quantify emergency department flow pressure and resource demand.

### Explainable AI

Provide transparent explanations for admission predictions and patient pathway assignment.

### Decision Support

Generate evidence-based recommendations for service redesign and policy intervention.

---

## Dataset

### Scale

* 558,018 Emergency Department encounters

### Domains

#### Demographics

* Age
* Gender
* Ethnicity
* Race
* Language
* Employment Status
* Insurance Status

#### Operational Variables

* Arrival Mode
* Arrival Month
* Arrival Day
* Arrival Time
* Previous Disposition

#### Clinical Variables

* Emergency Severity Index (ESI)
* Vital Signs
* Physiological Instability Indicators
* Chief Complaint Severity

#### Outcomes

* Admission
* Discharge

---

## Feature Engineering

### Clinical Acuity Engine

A composite acuity framework combining:

* ESI severity
* Physiological instability
* Chief complaint severity

Clinical Acuity = f(ESI, Physiology, Complaint Severity)

---

### Flow Pressure Engine

A novel operational pressure metric combining:

* Arrival mode pressure
* Temporal demand pressure
* Previous pathway risk

Flow Pressure = f(Arrival Mode, Temporal Demand, Prior Disposition)

---

### Physiological Instability Engine

Derived indicators:

* Tachycardia
* Tachypnea
* Hypoxia
* Hypotension

---

## Patient Journey Segmentation

### Algorithm

K-Means Clustering

### Clustering Features

* Clinical Acuity
* Flow Pressure
* Age

### Validation

* Elbow Method
* Silhouette Analysis

### Final Segments

#### Acute Ambulance Pathways

Working-age patients arriving predominantly via ambulance with moderate acuity and elevated operational demand.

#### Community Ambulatory Care

Low-acuity ambulatory patients with high discharge rates and potential community diversion opportunities.

#### Complex Elderly Admissions

Older patients with the highest admission rates, significant ambulance utilisation, and substantial resource requirements.

#### Moderate Complexity Care

Older adults with mixed pathways and opportunities for same-day emergency care optimisation.

---

## Explainable Machine Learning

### Admission Prediction

Models:

* XGBoost
* LightGBM
* Random Forest

### Explainability

SHAP (SHapley Additive Explanations)

Used to explain:

* Drivers of admission
* Drivers of discharge
* Cluster assignment behaviour

---

## Visual Analytics

### Executive Dashboard

Built with Streamlit.

Features:

* Executive KPI cards
* Patient segment explorer
* Cluster comparison views
* Health inequality insights

### Patient Journey Visualisation

* Sankey Diagrams
* Alluvial Flows
* Pathway Transition Analysis
* Segment Distribution Dashboards

---

## API Layer

Built using FastAPI.

Capabilities:

* Real-time admission prediction
* Patient pathway classification
* Segment assignment
* Explainability endpoints

---

## Technology Stack

### Data Science

* Python
* Pandas
* NumPy
* Scikit-Learn

### Machine Learning

* XGBoost
* LightGBM
* SHAP

### Visualisation

* Plotly
* Streamlit

### API

* FastAPI
* Uvicorn

### Development

* VS Code
* Git
* GitHub

---

## Repository Structure

```text
project/
│
├── data/
├── notebooks/
├── models/
├── app/
├── api/
├── assets/
├── requirements.txt
└── README.md
```

---

## Key Outcomes

* Identification of distinct patient journey archetypes
* Quantification of operational flow pressure
* Explainable admission prediction
* Executive-level pathway analytics
* Data-driven service redesign recommendations
* Decision-support framework for healthcare operations

---

## Future Enhancements

* Real-time streaming analytics
* Hospital-at-home pathway optimisation
* Length-of-stay prediction
* Readmission risk modelling
* Capacity forecasting
* Digital twin simulation of emergency care pathways

---

## Author

Priscilla Ejiro

Data Scientist | Machine Learning Engineer | Healthcare Analytics

Building explainable AI systems that transform healthcare operations and patient outcomes.
