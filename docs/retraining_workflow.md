# Model Retraining Workflow

```mermaid
flowchart TD
    A[Start Retraining from Streamlit] --> B[Sync Cluster Artefacts from Amazon S3]
    B --> C[Validate Required Artefacts]
    C --> D[Run Training Pipeline<br/>python -m src.pipeline.training]

    D --> E[Load Patient Journey Dataset]
    E --> F[Preprocessing Pipeline]
    F --> G1[Train Random Forest<br/>Admission Intelligence]
    F --> G2[Train LightGBM<br/>Operational Intelligence]
    F --> G3[Train XGBoost<br/>Policy Intelligence]

    G1 --> H[Evaluate Metrics]
    G2 --> H
    G3 --> H

    H --> I[Generate Feature Importance]
    I --> J[Register Models in MLflow/DagsHub]
    J --> K[Upload Models and Reports to Amazon S3]
    K --> L[Production Validation Checklist]
```

## Governance Value

The retraining workflow supports reproducibility, auditability and controlled model lifecycle management. It ensures that refreshed models are validated, tracked and stored before being used in production decision support.