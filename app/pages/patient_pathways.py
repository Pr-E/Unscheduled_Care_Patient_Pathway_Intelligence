import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.utils.data_loader import load_patient_data
from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, narrative_card


st.set_page_config(
    page_title="Patient Pathway Intelligence",
    page_icon="",
    layout="wide"
)

load_css()

journey_df = load_patient_data()

page_header(
    "Patient Pathway",
    "Intelligence",
    "Analyse patient movement from arrival source, through segment, to clinical disposition."
)

st.sidebar.header("Pathway Filters")

selected_clusters = st.sidebar.multiselect(
    "Patient Segments",
    options=sorted(journey_df["cluster_name"].dropna().unique()),
    default=sorted(journey_df["cluster_name"].dropna().unique())
)

filtered_df = journey_df[
    journey_df["cluster_name"].isin(selected_clusters)
]

section_label("Executive Pathway KPIs")

k1, k2, k3, k4 = st.columns(4)

with k1:
    kpi_card("Patients", f"{len(filtered_df):,}", "Filtered population")

with k2:
    kpi_card("Admission Rate", f"{filtered_df['admit_flag'].mean()*100:.1f}%", "Outcome burden")

with k3:
    kpi_card("Average Age", f"{filtered_df['age'].mean():.1f}", "Population profile")

with k4:
    kpi_card("Segments", f"{filtered_df['cluster_name'].nunique()}", "Active clusters")

section_label("Journey Heatmap")

heatmap_df = (
    filtered_df
    .groupby(["cluster_name", "disposition"])
    .size()
    .reset_index(name="patients")
)

fig = px.density_heatmap(
    heatmap_df,
    x="disposition",
    y="cluster_name",
    z="patients",
    text_auto=True,
    title="Segment-to-Disposition Heatmap",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

section_label("Pathway Flow View")

pathway_type = st.selectbox(
    "Select Pathway View",
    [
        "Arrival Mode → Segment → Disposition",
        "Clinical Acuity → Segment → Disposition",
        "Previous Disposition → Segment → Disposition",
        "Insurance → Segment → Disposition",
        "Age Band → Segment → Disposition",
        "Gender → Segment → Disposition",
        "Race → Segment → Disposition",
        "Employment → Segment → Disposition"
    ]
)

source_map = {
    "Arrival Mode → Segment → Disposition": "arrivalmode",
    "Clinical Acuity → Segment → Disposition": "acuity_band",
    "Previous Disposition → Segment → Disposition": "previousdispo",
    "Insurance → Segment → Disposition": "insurance_status",
    "Age Band → Segment → Disposition": "age_band",
    "Gender → Segment → Disposition": "gender",
    "Race → Segment → Disposition": "race",
    "Employment → Segment → Disposition": "employstatus"
}

source_col = source_map[pathway_type]

pathway_df = (
    filtered_df
    .groupby([source_col, "cluster_name", "disposition"])
    .size()
    .reset_index(name="count")
)

source_nodes = pathway_df[source_col].astype(str).unique().tolist()
cluster_nodes = pathway_df["cluster_name"].astype(str).unique().tolist()
outcome_nodes = pathway_df["disposition"].astype(str).unique().tolist()

all_nodes = source_nodes + cluster_nodes + outcome_nodes
node_map = {node: idx for idx, node in enumerate(all_nodes)}

source = []
target = []
value = []

for _, row in pathway_df.iterrows():

    source.append(node_map[str(row[source_col])])
    target.append(node_map[str(row["cluster_name"])])
    value.append(row["count"])

    source.append(node_map[str(row["cluster_name"])])
    target.append(node_map[str(row["disposition"])])
    value.append(row["count"])

fig = go.Figure(
    data=[
        go.Sankey(
            arrangement="snap",
            node=dict(
                pad=18,
                thickness=20,
                line=dict(color="rgba(255,255,255,0.35)", width=0.5),
                label=all_nodes,
                color="rgba(74,222,128,0.75)"
            ),
            link=dict(
                source=source,
                target=target,
                value=value,
                color="rgba(251,146,60,0.22)"
            )
        )
    ]
)

fig.update_layout(
    title=pathway_type,
    font_size=12,
    height=700,
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#f8fafc")
)

st.plotly_chart(fig, use_container_width=True)

section_label("Admission Burden Matrix")

burden_df = (
    filtered_df
    .groupby("cluster_name")
    .agg(
        patients=("admit_flag", "count"),
        admission_rate=("admit_flag", "mean"),
        admissions=("admit_flag", "sum"),
        average_age=("age", "mean"),
        average_acuity=("clinical_acuity", "mean")
    )
    .reset_index()
)

burden_df["admission_rate"] = burden_df["admission_rate"] * 100

fig = px.scatter(
    burden_df,
    x="patients",
    y="admission_rate",
    size="admissions",
    color="cluster_name",
    hover_data=["average_age", "average_acuity", "admissions"],
    title="Volume × Admission Burden Matrix",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

largest_segment = filtered_df["cluster_name"].value_counts().idxmax()
highest_admission_segment = filtered_df.groupby("cluster_name")["admit_flag"].mean().idxmax()
highest_admission_rate = filtered_df.groupby("cluster_name")["admit_flag"].mean().max() * 100

section_label("AI Executive Pathway Assessment")

narrative_card(
    f"""
    The largest current pathway segment is <b>{largest_segment}</b>.
    <br><br>
    The highest admission burden is concentrated in
    <b>{highest_admission_segment}</b>, with an admission rate of
    <b>{highest_admission_rate:.1f}%</b>.
    <br><br>
    This suggests that operational focus should prioritise high-burden
    segments while monitoring equity differences across race, employment,
    gender and insurance pathway views.
    """
)

with st.expander("View Pathway Dataset"):
    st.dataframe(pathway_df, use_container_width=True)