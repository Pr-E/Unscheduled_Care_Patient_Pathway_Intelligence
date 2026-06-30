# Cloud Deployment Architecture

```mermaid
flowchart TD
    A[Developer Push to Main Branch] --> B[GitHub Repository]
    B --> C[GitHub Actions CI/CD]

    C --> D[Build Docker Image]
    D --> E[Tag Image]
    E --> F[Push Image to Amazon ECR]

    F --> G[AWS Systems Manager]
    G --> H[Amazon EC2 Instance]

    H --> I[Docker Runtime]
    I --> J1[FastAPI<br/>Port 8000]
    I --> J2[Streamlit<br/>Port 8501]

    J1 --> K[Prediction Endpoints]
    J2 --> L[Executive Dashboard]

    I --> M[Amazon S3]
    M --> N1[Model Registry Artefacts]
    M --> N2[Cluster Artefacts]
    M --> N3[Metadata & Reports]

    I --> O[MLflow + DagsHub]
    O --> P[Experiment Tracking<br/>Model Governance]
```

## Deployment Flow

```text
GitHub Push
   ↓
GitHub Actions
   ↓
Docker Build
   ↓
Amazon ECR
   ↓
AWS SSM
   ↓
EC2 Docker Container
   ↓
FastAPI + Streamlit
   ↓
CareFlow IQ Live Platform
```