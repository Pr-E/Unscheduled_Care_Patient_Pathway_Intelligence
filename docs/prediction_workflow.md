# Prediction Workflow

```mermaid
flowchart TD
    A[User enters patient scenario] --> B[Feature Builder]
    B --> C[Cluster Predictor]
    C --> D[Patient Segment Assignment]

    D --> E[Admission Model<br/>Random Forest]
    E --> F[Admission Probability]
    F --> G[Risk Level]

    E --> H[SHAP Explainer]
    H --> I[Top Prediction Drivers]

    G --> J[Recommended Care Pathway]
    I --> K[Executive Narrative]
    J --> L[Recommended Actions]

    K --> M[Streamlit Admission Intelligence Page]
    L --> M
```

## Output Generated

The Admission Intelligence module produces:

- Admission probability
- Risk level
- Patient segment
- Segment confidence
- Recommended care pathway
- SHAP-based prediction drivers
- Executive narrative
- Recommended operational actions