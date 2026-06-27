import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import plotly.express as px
import streamlit as st

from src.utils.data_loader import (
    load_patient_data,
    load_persona_data
)

from utils.styling import load_css

from utils.ui_components import (
    page_header,
    section_label,
    kpi_card,
    narrative_card
)


st.set_page_config(
    page_title="Cluster Explorer",
    page_icon="",
    layout="wide"
)

load_css()

journey_df = load_patient_data()
persona_df = load_persona_data()

page_header(
    "Cluster",
    "Explorer",
    """
    Explore demographic, clinical and operational profiles
    across patient journey segments.
    """
)

selected_cluster = st.selectbox(
    "Select Patient Segment",
    persona_df["segment_name"].tolist()
)

cluster_info = persona_df[
    persona_df["segment_name"] == selected_cluster
]

cluster_df = journey_df[
    journey_df["cluster_name"] == selected_cluster
]

section_label("Executive Segment KPIs")

k1, k2, k3, k4 = st.columns(4)

with k1:
    kpi_card(
        "Patients",
        f"{len(cluster_df):,}",
        "Segment volume"
    )

with k2:
    kpi_card(
        "Admission Rate",
        f"{cluster_df['admit_flag'].mean() * 100:.1f}%",
        "Outcome burden"
    )

with k3:
    kpi_card(
        "Average Age",
        f"{cluster_df['age'].mean():.1f}",
        "Population profile"
    )

with k4:
    kpi_card(
        "Average Acuity",
        f"{cluster_df['clinical_acuity'].mean():.2f}",
        "Clinical intensity"
    )

section_label("AI Segment Assessment")

if not cluster_info.empty:

    admission_rate = (
        cluster_df["admit_flag"]
        .mean()
        * 100
    )

    average_age = cluster_df["age"].mean()

    average_acuity = cluster_df["clinical_acuity"].mean()

    top_arrival = (
        cluster_df["arrivalmode"]
        .value_counts()
        .idxmax()
    )

    opportunity = cluster_info[
        "pathway_opportunity"
    ].iloc[0]

    narrative_card(
        f"""
        <b>{selected_cluster}</b> represents a distinct patient
        pathway profile with identifiable clinical, demographic and
        operational characteristics.
        <br><br>
        This segment has an admission rate of
        <b>{admission_rate:.1f}%</b>, an average age of
        <b>{average_age:.1f}</b>, and an average acuity score of
        <b>{average_acuity:.2f}</b>.
        <br><br>
        The dominant arrival mode is
        <b>{top_arrival}</b>, suggesting an important operational
        access pattern for this cohort.
        <br><br>
        <b>Executive opportunity:</b> {opportunity}.
        """
    )

section_label("Demographic Intelligence")

c1, c2 = st.columns(2)

with c1:

    gender_df = (
        cluster_df["gender"]
        .value_counts()
        .reset_index()
    )

    gender_df.columns = [
        "gender",
        "patients"
    ]

    fig = px.pie(
        gender_df,
        names="gender",
        values="patients",
        hole=0.58,
        title="Gender Distribution",
        template="plotly_dark"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    narrative_card(
        """
        This visual helps identify whether the selected pathway
        segment is concentrated within a specific gender group,
        supporting equity-aware service planning.
        """
    )

with c2:

    race_df = (
        cluster_df["race"]
        .value_counts()
        .reset_index()
    )

    race_df.columns = [
        "race",
        "patients"
    ]

    fig = px.bar(
        race_df,
        x="race",
        y="patients",
        color="patients",
        title="Race Distribution",
        template="plotly_dark"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    narrative_card(
        """
        Race distribution provides an equity lens into how
        different population groups are represented in this
        pathway segment.
        """
    )

section_label("Operational Arrival Profile")

arrival_df = (
    cluster_df["arrivalmode"]
    .value_counts()
    .reset_index()
)

arrival_df.columns = [
    "arrivalmode",
    "patients"
]

fig = px.bar(
    arrival_df.sort_values("patients"),
    x="patients",
    y="arrivalmode",
    orientation="h",
    text="patients",
    color="patients",
    title="Arrival Mode Burden",
    template="plotly_dark"
)

fig.update_layout(
    height=480,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis_title="",
    xaxis_title="Patients"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

narrative_card(
    """
    Arrival mode intelligence shows how this cohort enters
    unscheduled care. Higher ambulance or transfer burden may
    indicate stronger need for streaming, rapid assessment and
    capacity escalation.
    """
)

section_label("Clinical Acuity vs Flow Pressure")

sample_df = cluster_df.sample(
    min(
        10000,
        len(cluster_df)
    ),
    random_state=42
)

fig = px.scatter(
    sample_df,
    x="flow_pressure_z",
    y="clinical_acuity",
    color="disposition",
    opacity=0.6,
    title="Clinical Acuity vs Flow Pressure",
    template="plotly_dark"
)

fig.update_layout(
    height=560,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

narrative_card(
    """
    This plot shows how clinical acuity interacts with flow pressure.
    Patients located in higher acuity and higher pressure zones are
    more likely to require escalation, senior review and proactive
    pathway planning.
    """
)

# =====================================================
# EXECUTIVE ACTION FRAMEWORK
# =====================================================

section_label("Executive Action Framework")

if "Elderly" in selected_cluster:
    clinical_focus = "Frailty review, Comprehensive Geriatric Assessment and early senior decision-making"
    operational_focus = "Bed planning, discharge coordination, virtual ward and Hospital-at-Home review"
    strategic_focus = "Reduce avoidable elderly admissions and strengthen community frailty pathways"

elif "Ambulance" in selected_cluster:
    clinical_focus = "Rapid assessment, early diagnostics and escalation review"
    operational_focus = "Ambulance handover coordination, streaming and capacity buffer planning"
    strategic_focus = "Improve ambulance flow, reduce ED congestion and strengthen urgent response pathways"

elif "Ambulatory" in selected_cluster:
    clinical_focus = "Low-acuity streaming, community review and safe discharge planning"
    operational_focus = "Urgent treatment centre routing, virtual consultation and ambulatory care expansion"
    strategic_focus = "Reduce avoidable ED pressure and maximise community-based alternatives"

else:
    clinical_focus = "Senior review for borderline admissions and targeted observation"
    operational_focus = "Same Day Emergency Care, diagnostics coordination and pathway monitoring"
    strategic_focus = "Reduce unnecessary admissions while maintaining safe escalation routes"

a1, a2, a3 = st.columns(3)

with a1:
    narrative_card(
        f"""
        <b>Clinical Focus</b><br><br>
        {clinical_focus}
        """
    )

with a2:
    narrative_card(
        f"""
        <b>Operational Focus</b><br><br>
        {operational_focus}
        """
    )

with a3:
    narrative_card(
        f"""
        <b>Strategic Focus</b><br><br>
        {strategic_focus}
        """
    )

# =====================================================
# RAW DATA
# =====================================================

with st.expander(
    "View Segment Dataset"
):

    st.dataframe(
        cluster_df.head(1000),
        use_container_width=True
    )