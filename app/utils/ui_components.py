import textwrap
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


DARK_TEMPLATE = "plotly_dark"


def clean_html(text):

    return (
        textwrap.dedent(text)
        .strip()
        .replace("\n", " ")
    )


def page_header(title, accent, subtitle):

    st.markdown(
        f"""
        <div class="page-title">{title} <span>{accent}</span></div>
        <div class="page-subtitle">{clean_html(subtitle)}</div>
        """,
        unsafe_allow_html=True
    )


def section_label(text):

    st.markdown(
        f"<div class='section-label'>{text}</div>",
        unsafe_allow_html=True
    )


def kpi_card(label, value, note=""):

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def narrative_card(text):

    st.markdown(
        f"""
        <div class="narrative-card">
            {clean_html(text)}
        </div>
        """,
        unsafe_allow_html=True
    )


def gauge_chart(value, title):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "%"},
            title={"text": title},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#4ade80"},
                "steps": [
                    {"range": [0, 40], "color": "rgba(74,222,128,0.22)"},
                    {"range": [40, 60], "color": "rgba(234,179,8,0.22)"},
                    {"range": [60, 80], "color": "rgba(251,146,60,0.25)"},
                    {"range": [80, 100], "color": "rgba(239,68,68,0.25)"},
                ],
            },
        )
    )

    fig.update_layout(
        template=DARK_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=330,
        font=dict(color="#f8fafc"),
        margin=dict(l=20, r=20, t=55, b=20)
    )

    return fig


def beautiful_bar(fig):

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),
        margin=dict(l=20, r=20, t=55, b=30)
    )

    fig.update_traces(
        marker_line_width=0,
        textposition="outside"
    )

    return fig