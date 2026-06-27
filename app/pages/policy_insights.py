import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT_DIR))

import streamlit as st
import plotly.express as px

from src.utils.data_loader import load_patient_data, load_persona_data
from utils.styling import load_css
from utils.ui_components import page_header, section_label, kpi_card, narrative_card, beautiful_bar


st.set_page_config(
    page_title="Policy Insights",
    page_icon="",
    layout="wide"
)

load_css()

journey_df = load_patient_data()
persona_df = load_persona_data()

page_header(
    "Policy",
    "Insights",
    "Cluster-led NHS service redesign intelligence for pathway optimisation and equity improvement."
)

total_patients = len(journey_df)
overall_admission_rate = journey_df["admit_flag"].mean() * 100
largest_segment = persona_df.sort_values("patients", ascending=False).iloc[0]
highest_admission_segment = persona_df.sort_values("admission_pct", ascending=False).iloc[0]

section_label("Executive Policy KPIs")

k1, k2, k3, k4 = st.columns(4)

with k1:
    kpi_card("Patients", f"{total_patients:,}", "Population analysed")

with k2:
    kpi_card("Admission Rate", f"{overall_admission_rate:.1f}%", "Overall burden")

with k3:
    kpi_card("Largest Segment", largest_segment["segment_name"], "Demand driver")

with k4:
    kpi_card("Highest Admission", highest_admission_segment["segment_name"], "Risk driver")

section_label("Admission Burden by Segment")

fig = px.bar(
    persona_df.sort_values("admission_pct"),
    x="admission_pct",
    y="segment_name",
    orientation="h",
    text="admission_pct",
    color="admission_pct",
    color_continuous_scale=["#4ade80", "#fb923c"],
    title="Admission Burden by Segment",
    template="plotly_dark"
)

fig.update_layout(
    height=460,
    xaxis_title="Admission Rate (%)",
    yaxis_title=""
)

st.plotly_chart(beautiful_bar(fig), use_container_width=True)

section_label("AI Policy Prioritisation Matrix")

priority_df = persona_df.copy()

priority_df["estimated_admissions"] = (
    priority_df["patients"]
    * priority_df["admission_pct"]
    / 100
)

fig = px.scatter(
    priority_df,
    x="patients",
    y="admission_pct",
    size="estimated_admissions",
    color="segment_name",
    hover_data=["pathway_opportunity"],
    title="Volume × Admission Burden Priority Matrix",
    template="plotly_dark"
)

fig.update_layout(
    height=520,
    xaxis_title="Patient Volume",
    yaxis_title="Admission Rate (%)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#f8fafc")
)

st.plotly_chart(fig, use_container_width=True)

section_label("AI Executive Policy Assessment")

narrative_card(
    f"""
    The strongest policy opportunity is concentrated in
    <b>{highest_admission_segment['segment_name']}</b>, where admission burden is highest.
    <br><br>
    The largest demand volume comes from
    <b>{largest_segment['segment_name']}</b>.
    <br><br>
    <b>Policy opportunity:</b>
    {highest_admission_segment['pathway_opportunity']}.
    <br><br>
    Recommended redesign focus should combine frailty pathways,
    community diversion, same-day emergency care, ambulance streaming,
    equity monitoring and proactive discharge coordination.
    """
)



section_label("Strategic Value Delivered")

value_map = {

    "Community Ambulatory Care": {
        "value": """
        <b>Strategic Insight</b><br><br>
        This is the largest patient population, representing a substantial proportion of
        unscheduled care attendances while maintaining the lowest admission burden.
        <br><br>
        <b>Business Value</b><br>
        • Opportunity to maximise ambulatory emergency care (AEC) and Same Day Emergency Care (SDEC).<br>
        • Reduce avoidable admissions through enhanced community pathways.<br>
        • Improve emergency department throughput and patient flow.<br>
        • Release inpatient capacity for higher-acuity patients.
        """
    },

    "Moderate Complexity Care": {
        "value": """
        <b>Strategic Insight</b><br><br>
        Patients within this segment demonstrate moderate admission risk with mixed clinical
        complexity, making them ideal candidates for targeted clinical decision support.
        <br><br>
        <b>Business Value</b><br>
        • Improve early senior clinical review.<br>
        • Optimise streaming decisions and observation pathways.<br>
        • Reduce unnecessary inpatient admissions.<br>
        • Support proactive operational planning during peak demand.
        """
    },

    "Acute Ambulance Pathways": {
        "value": """
        <b>Strategic Insight</b><br><br>
        This cohort contributes disproportionately to emergency department pressure due to
        ambulance arrivals and higher clinical urgency.
        <br><br>
        <b>Business Value</b><br>
        • Improve ambulance offload performance.<br>
        • Prioritise rapid assessment and treatment pathways.<br>
        • Strengthen emergency flow coordination.<br>
        • Support capacity escalation planning during periods of operational pressure.
        """
    },

    "Complex Elderly Admissions": {
        "value": """
        <b>Strategic Insight</b><br><br>
        This segment has the highest admission burden and represents the greatest opportunity
        for reducing avoidable hospitalisation among frail older adults.
        <br><br>
        <b>Business Value</b><br>
        • Prioritise frailty assessment and Comprehensive Geriatric Assessment (CGA).<br>
        • Expand Hospital-at-Home and virtual ward pathways.<br>
        • Strengthen multidisciplinary discharge planning.<br>
        • Improve system resilience through proactive elderly care management.
        """
    }

}

for _, row in persona_df.iterrows():

    a, b, c, d = st.columns([2.1, 1, 1, 3.5])

    with a:
        kpi_card(
            row["segment_name"],
            f"{row['patients']:,}",
            "Patients"
        )

    with b:
        kpi_card(
            "Population",
            f"{row['patient_pct']:.1f}%",
            "Population Share"
        )

    with c:
        kpi_card(
            "Admission",
            f"{row['admission_pct']:.1f}%",
            "Admission Burden"
        )

    with d:

        narrative_card(
            value_map.get(
                row["segment_name"],
                {
                    "value": f"""
                    <b>Strategic Insight</b><br><br>
                    {row['pathway_opportunity']}
                    """
                }
            )["value"]
        )
