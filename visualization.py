import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

st.set_page_config(
    page_title="Stress Monitor - Educational Institutions",
    page_icon="🧠",
    layout="wide",
)

# -------- SIDEBAR --------
with st.sidebar:
    st.markdown("### 🧠 Stress Monitor")

    with st.expander("ℹ️ How to use this app", expanded=True):
        st.markdown(
            """
            - Start in **Visualization** to see overall stress patterns.  
            - Open **Alerts** to view automatically detected risk cases.  
            - Check **Distribution** for breakdowns by age, gender, and category.  
            - Use **Recommendations** to explore suggested interventions.  
            - Visit **Risk groups** to inspect clusters of students needing attention.
            """
        )

    with st.expander("📂 About the data", expanded=False):
        st.markdown(
            """
            - **Stress_Dataset.csv** – survey‑based stress indicators and demographics.  
            - **StressLevelDataset.csv** – categorized stress levels across five domains.
            """
        )

    with st.expander("💡 Tips", expanded=False):
        st.markdown(
            """
            - Hover charts to view exact values.  
            - Use filters on each page to focus on specific groups.  
            - Download tables (where enabled) for offline analysis.
            """
        )

# -------- GLOBAL STYLES --------
st.markdown(
    """
    <style>
        .hero-card {
            background: linear-gradient(135deg, #e0f2fe 0%, #eef2ff 100%);
            padding: 2.5rem 2rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            border: 1px solid #dbeafe;
            text-align: center;
        }
        .hero-title {
            font-size: 2.6rem;
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .hero-subtitle {
            font-size: 1.1rem;
            color: #4b5563;
            text-align: center;
            max-width: 780px;
            margin: 0 auto;
            line-height: 1.6;
        }
        .metric-card-1 {
            background-color: #dbeafe;
            padding: 1.2rem 1.3rem;
            border-radius: 14px;
            border: 1px solid #93c5fd;
            box-shadow: 0 6px 18px rgba(37,99,235,0.15);
            text-align: center;
        }
        .metric-card-2 {
            background-color: #dcfce7;
            padding: 1.2rem 1.3rem;
            border-radius: 14px;
            border: 1px solid #86efac;
            box-shadow: 0 6px 18px rgba(22,163,74,0.15);
            text-align: center;
        }
        .metric-card-3 {
            background-color: #fef9c3;
            padding: 1.2rem 1.3rem;
            border-radius: 14px;
            border: 1px solid #facc15;
            box-shadow: 0 6px 18px rgba(234,179,8,0.15);
            text-align: center;
        }
        .metric-card-1 h3, .metric-card-2 h3, .metric-card-3 h3 {
            margin: 0 0 0.3rem 0;
            font-size: 1rem;
            text-align: center;
            color: #111827;
        }
        .metric-card-1 p, .metric-card-2 p, .metric-card-3 p {
            margin: 0;
            font-size: 0.95rem;
            color: #111827;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------- HERO SECTION --------
st.markdown(
    """
    <div style="display:flex; justify-content:center; width:100%;">
        <div class="hero-card" style="max-width: 1100px; width:100%; text-align: center;">
            <div class="hero-title">🧠 Stress Monitor app</div>
            <p class="hero-subtitle">
                A dashboard for educational institutions to understand and manage student stress levels.
                Navigate through the pages to detect at-risk students, explore stress distributions, and access tailored recommendations for intervention.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------- DATASET OVERVIEW --------

st.markdown("""
    <div style='text-align:center; margin-top:1.5rem;'>
        <h2 style='color:#1e3a8a; font-size:2.1rem; font-weight:700; margin-bottom:0.2rem;'>📊 Dataset Overview</h2>
        <p style='color:#4b5563; font-size:1.05rem; margin-top:0.3rem;'>
            Explore the two datasets used to monitor and understand student stress.<br>
            Each dataset provides complementary insights into <b>stress indicators</b> and <b>stress categories</b> 🧠💬
        </p>
    </div>
""", unsafe_allow_html=True)

# Dataset cards row
try:
    df1 = pd.read_csv("Stress_Dataset.csv")
    df2 = pd.read_csv("StressLevelDataset.csv")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            f"""
            <div style="
                background:linear-gradient(135deg,#dbeafe,#eff6ff);
                padding:1.4rem 1.3rem;
                border-radius:18px;
                border:1px solid #bfdbfe;
                box-shadow:0px 8px 20px rgba(59,130,246,0.18);
                text-align:center;
            ">
                <h3 style="margin:0; font-size:1.2rem; color:#1e3a8a;">📄 Dataset 1: <i>Stress_Dataset.csv</i></h3>
                <p style="margin:0.5rem 0 0; font-size:0.98rem; color:#1f2937;">
                    <b>Records:</b> {df1.shape[0]}<br>
                    <b>Features:</b> {df1.shape[1]}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div style="
                background:linear-gradient(135deg,#dcfce7,#f0fdf4);
                padding:1.4rem 1.3rem;
                border-radius:18px;
                border:1px solid #86efac;
                box-shadow:0px 8px 20px rgba(34,197,94,0.17);
                text-align:center;
            ">
                <h3 style="margin:0; font-size:1.2rem; color:#166534;">📄 Dataset 2: <i>StressLevelDataset.csv</i></h3>
                <p style="margin:0.5rem 0 0; font-size:0.98rem; color:#1f2937;">
                    <b>Records:</b> {df2.shape[0]}<br>
                    <b>Features:</b> {df2.shape[1]}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # -------- PREVIEW SECTION HEADER --------
    st.markdown("""
        <div style='text-align:center; margin-bottom:1rem;'>
            <h2 style="color:#1e3a8a; font-size:2rem; font-weight:700;">📄 Preview Datasets</h2>
            <p style="color:#4b5563; font-size:1rem; margin-top:-0.2rem;">
                Browse the content of each dataset and inspect their structure 👀📘
            </p>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📄 Stress_Dataset.csv", "📄 StressLevelDataset.csv"])

    with tab1:
        st.subheader("Dataset 1: Stress_Dataset.csv")

        with st.container(border=True):
            st.markdown(
                """
                **Overview**  
                This dataset contains information about students' **self‑reported stress** 
                and demographics.

                **Key details**  
                - 🎯 Students aged **18–21 years old**  
                - 📊 Item responses typically range from **0 to 5**  
                - 🧠 Covers **emotional well‑being**  
                - 💓 Includes **physical symptoms**  
                - 🎓 Captures **academic experiences**  
                - 👤 Contains **demographic information**
                """
            )

        df1_clean = df1[(df1["Age"] >= 18) & (df1["Age"] <= 21)].copy()
        df1_clean.rename(
            columns={"Which type of stress do you primarily experience?": "stress_type"},
            inplace=True,
        )

        st.markdown("### Preview of the first few rows")
        st.dataframe(df1_clean.head(), use_container_width=True)

        st.markdown(
            f"**Target variable:** `stress_type` "
            f"({df1_clean['stress_type'].nunique()} categories)"
        )
        stress_types = df1_clean["stress_type"].unique()
        st.markdown("\n".join([f"- 🔸 **{s}**" for s in stress_types]))

    with tab2:
        st.subheader("Dataset 2: StressLevelDataset.csv")

        with st.container(border=True):
            st.markdown(
                """
                **Overview**  
                This dataset includes **categorized stress levels** and additional 
                information related to students' academic context.

                **Five stress categories**  
                - 🧠 **Psychological** – anxiety, self‑esteem, mood, mental health history  
                - 💓 **Physiological** – headaches, sleep quality, blood pressure  
                - 🌍 **Environmental** – noise, living conditions, safety, basic needs  
                - 🎓 **Academic** – workload, grades, teacher relationships, future concerns  
                - 🤝 **Social** – social support, peer pressure, bullying, activities
                """
            )

        st.markdown("### Preview of the first few rows")
        st.dataframe(df2.head(), use_container_width=True)

        st.markdown(
            f"**Target variable:** `stress_level` (0–{df2['stress_level'].nunique() - 1})"
        )

except Exception as e:
    st.error(f"Error loading datasets: {e}")
