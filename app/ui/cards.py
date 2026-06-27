import streamlit as st


def executive_metric(
    label: str,
    value: str
):

    st.markdown(
        f"""
        <div class="metric-card">

            <div class="metric-value">
                {value}
            </div>

            <div class="metric-label">
                {label}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )