import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import plotly.express as px
import streamlit as st

from src.utils.data_loader import load_patient_data, load_persona_data
from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, narrative_card


st.set_page_config(
    page_title="Cluster Intelligence",
    page_icon="",
    layout="wide"
)

load_css()

journey_df = load_patient_data()
persona_df = load_persona_data()

page_header(
    "Cluster",
    "Intelligence",
    "Executive overview of patient journey segments, admission burden and service redesign opportunities."
)

largest_segment = persona_df.sort_values("patients", ascending=False).iloc[0]
highest_admission = persona_df.sort_values("admission_pct", ascending=False).iloc[0]

section_label("Executive Cluster KPIs")

k1, k2, k3, k4 = st.columns(4)

with k1:
    kpi_card("Segments", f"{persona_df.shape[0]}", "Patient pathway groups")

with k2:
    kpi_card("Largest Segment", largest_segment["segment_name"], "Highest volume")

with k3:
    kpi_card("Highest Admission", highest_admission["segment_name"], "Largest risk burden")

with k4:
    kpi_card("Patients", f"{len(journey_df):,}", "Records analysed")

section_label("Admission Burden by Segment")

fig = px.bar(
    persona_df.sort_values("admission_pct"),
    x="admission_pct",
    y="segment_name",
    orientation="h",
    text="admission_pct",
    color="admission_pct",
    title="Admission Burden by Segment",
    template="plotly_dark"
)

fig.update_layout(
    height=480,
    xaxis_title="Admission Rate (%)",
    yaxis_title="",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)

section_label("AI Executive Cluster Assessment")

narrative_card(
    f"""
    The cluster intelligence layer identifies <b>{persona_df.shape[0]}</b>
    operationally meaningful patient journey segments.
    <br><br>
    <b>{largest_segment['segment_name']}</b> represents the largest population burden,
    while <b>{highest_admission['segment_name']}</b> carries the highest admission burden.
    <br><br>
    These patterns support targeted pathway redesign, capacity planning,
    equity monitoring and admission avoidance strategy.
    """
)

section_label("Navigation")

c1, c2, c3 = st.columns(3)

with c1:
    st.page_link("pages/cluster_explorer.py", label="Open Cluster Explorer")

with c2:
    st.page_link("pages/patient_pathways.py", label="Open Patient Pathways")

with c3:
    st.page_link("pages/policy_insights.py", label="Open Policy Insights")