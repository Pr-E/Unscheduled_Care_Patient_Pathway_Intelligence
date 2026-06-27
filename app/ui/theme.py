import streamlit as st

BACKGROUND = "#061321"

SURFACE = "#0B2239"

SURFACE_LIGHT = "#13385A"

ACCENT = "#00C2FF"

TEXT = "#FFFFFF"

TEXT_SECONDARY = "#B7C9D8"

BORDER = "#1D4E89"


def apply_executive_theme():

    st.markdown(
        f"""
        <style>

        .stApp {{
            background:{BACKGROUND};
        }}

        .main {{
            background:{BACKGROUND};
        }}

        header {{
            visibility:hidden;
        }}

        [data-testid="stToolbar"] {{
            display:none;
        }}

        [data-testid="stDecoration"] {{
            display:none;
        }}

        [data-testid="stSidebar"] {{
            background:{BACKGROUND};
            border-right:1px solid {BORDER};
        }}

        [data-testid="stSidebar"] * {{
            color:{TEXT};
        }}

        h1,h2,h3,h4,h5 {{
            color:{TEXT};
        }}

        p,span,label {{
            color:{TEXT_SECONDARY};
        }}

        .hero-container {{

            background:linear-gradient(
                135deg,
                {SURFACE},
                {SURFACE_LIGHT}
            );

            padding:50px;

            border-radius:24px;

            border:1px solid {BORDER};

            margin-bottom:30px;
        }}

        .hero-title {{

            font-size:56px;

            font-weight:800;

            color:{TEXT};
        }}

        .hero-subtitle {{

            font-size:20px;

            margin-top:15px;

            color:{TEXT_SECONDARY};

            max-width:1000px;
        }}

        .metric-card {{

            background:{SURFACE};

            border:1px solid {BORDER};

            border-radius:20px;

            padding:25px;

            text-align:center;

            min-height:150px;
        }}

        .metric-value {{

            font-size:40px;

            font-weight:700;

            color:{ACCENT};
        }}

        .metric-label {{

            margin-top:10px;

            font-size:18px;

            color:{TEXT};
        }}

        .portfolio-card {{

            background:{SURFACE};

            border:1px solid {BORDER};

            border-radius:22px;

            padding:30px;

            min-height:580px;
        }}

        .section-title {{

            font-size:20px;

            font-weight:700;

            color:{TEXT};

            margin-top:20px;
        }}

        [data-testid="stPageLink"] a {{

            display:block;

            width:100%;

            text-align:center;

            padding:14px;

            background:{ACCENT};

            color:black !important;

            font-weight:700;

            border-radius:12px;

            text-decoration:none;

            margin-top:12px;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )