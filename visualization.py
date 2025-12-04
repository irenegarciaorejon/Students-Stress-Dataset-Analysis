import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns



st.set_page_config(page_title="Stress Monitor - Institutions Educatives", page_icon="🧠",layout="wide")

st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        color: #1e3a8a !important;
        text-align: center;
        margin-bottom: 2rem;
    }
    .welcome-text {
        font-size: 1.3rem !important;
        color: #374151 !important;
        text-align: center;
        margin-bottom: 3rem;
        line-height: 1.6;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    .stMetric > label {
        color: white !important;
        font-size: 1.1rem !important;
    }
    .stMetric > div > div {
        color: white !important;
        font-size: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem; border-radius: 20px; margin-bottom: 2rem;">
        <h1 class="main-header">🧠Stress Monitor app</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="welcome-text">
    Welcome to the Stress Monitor application for educational institutions. 
    This platform is designed to help educators and administrators understand and manage student stress levels through comprehensive data analysis and visualization tools.
    Use interactive dashboards to identify at-risk groups, generate alerts, and receive recommendations for stress management interventions.
        """,unsafe_allow_html=True)

st.divider()
st.markdown("<h2 style='text-align: center; color: #1e3a8a;'>📊 Dataset Overview</h2>", unsafe_allow_html=True)
try:
    df1=pd.read_csv("Stress_Dataset.csv")
    df2=pd.read_csv("StressLevelDataset.csv")

    col1,col2,col3=st.columns(3)
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>Dataset 1: Stress_Dataset.csv</h3>
            <p>Number of Records: {}</p>
            <p>Number of Features: {}</p>
        </div>
        """.format(df1.shape[0], df1.shape[1]), unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>Dataset 2: StressLevelDataset.csv</h3>
            <p>Number of Records: {}</p>
            <p>Number of Features: {}</p>
        </div>
        """.format(df2.shape[0], df2.shape[1]), unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>Total Records</h3>
            <p>{}</p>
        </div>
        """.format(df1.shape[0]+df2.shape[0]), unsafe_allow_html=True)

    st.divider()
    st.markdown("<h2 style='text-align: center; color:  #1e3a8a;'>📄 Preview datasets</h2>", unsafe_allow_html=True)
    tab1, tab2=st.tabs(["📄Stress_Dataset.csv", "📄StressLevelDataset.csv"])
    with tab1:
        st.header("Dataset 1: Stress_Dataset.csv")
        with st.container(border=True):
            st.markdown("""
            **Overview** : This dataset contains information about **students' stress levels**, recorded as answers to various questions.
            
            **Key Details:**    
                - 🎯Students aged **18-21 years old**    
                - 📊Responses range from **0 to 5**  
                - 🧠Covers **emotional well-being**  
                - 💓Includes **physical symptoms**  
                - 🎓Details on **academic experiences**  
                - 👤Contains emographic information 
                    
            """)
        df1_clean = df1[(df1["Age"]>=18) & (df1["Age"]<=21)].copy()
        df1_clean.rename(columns={"Which type of stress do you primarily experience?": "stress_type"}, inplace=True)
        st.markdown("### Preview of the first few rows:")
        st.write(df1.head())
        st.write(f"**Target:** `stress_type` ({df1_clean['stress_type'].nunique()} categories):")
        stress_types = df1_clean["stress_type"].unique()
        st.markdown(
            "\n".join([f"🔸 **{s}**  " for s in stress_types])
        )
        
    with tab2:
        st.header("Dataset 2: StressLevelDataset.csv")
        with st.container(border=True):
            st.markdown("""
            **Overview** : "This dataset includes additional information about **students' academic performance** and **stress levels**. It consists in different stress categories based on various factors."
            
            **Five Stress Categories:**  
                - 🧠 **Psychological**: anxiety, self-esteem, depression, mental health history…  
                - 💓 **Physiological**: headache, blood pressure, sleep quality, respiratory problems…  
                - 🌍 **Environmental**: noise, living conditions, safety, basic needs…  
                - 🎓 **Academic**: academic performance, study load, student-teacher relationship, concern for the future…   
                - 🤝 **Social**: social support, peer pressure, extracurricular activities, bullying.  
                        
            """)
        
        st.markdown("### Preview of the first few rows:")
        st.write(df2.head())
        
        st.write(f"**Target variable**:`stress_level` (0-{df2['stress_level'].nunique()-1})")


except Exception as e:
    st.error(f"Error loading datasets: {e}")

