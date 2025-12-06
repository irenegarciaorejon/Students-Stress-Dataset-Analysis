import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

st.set_page_config(page_title="Exploratory Data Analysis", layout="wide")

st.markdown("""
<style>
    .main-title {
        font-size: 2rem !important;
        color: #1e3a8a !important;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .section-title {
        font-size: 1.3rem !important;
        color: #1e3a8a !important;
        margin-top: 1.2rem;
        font-weight: 600;
    }
            .info-box {
        background: #f0f4ff;
        border-left: 6px solid #1e3a8a;
        padding: 12px 16px;
        border-radius: 8px;
        margin: 0.6rem 0 1.2rem 0;
        font-size: 0.92rem;
        line-height: 1.4rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }

    .info-title {
        font-weight: 700;
        color: #1e3a8a;
        font-size: 1rem;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .info-title img {
        height: 18px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 style='text-align:center; color:#1e3a8a; font-weight:700;'>📈 Exploratory Data Analysis</h1>
<p style='text-align:center; font-size:1.1rem; margin-top:4px;'>
Explore datasets, visualize distributions, correlations, and filter data interactively.
</p>
""", unsafe_allow_html=True)
st.sidebar.title("📘 How to use this dashboard")

st.sidebar.markdown("""
    This page helps you explore both datasets interactively.  
    Follow these steps:

    ### 🔍 How to use the page
    1. Select a dataset from the tabs at the top.  
    2. Use dropdowns to choose which variable to visualize.  
    3. Read insights and chart explanations below each graph.  
    4. Use filters to interactively subset the data.  
    """)

@st.cache_data
def load_data():
    df1 = pd.read_csv("Stress_Dataset.csv")
    df2 = pd.read_csv("StressLevelDataset.csv")
    return df1, df2


df1, df2 = load_data()
df1.rename(columns={"Which type of stress do you primarily experience?":"stress_type"}, inplace=True)
df1 = df1[(df1["Age"]>=18) & (df1["Age"]<=21)]

tab1, tab2 = st.tabs(["📊 Stress_Dataset.csv", "📊 StressLevelDataset.csv"])


# ---------- TAB 1 ----------
with tab1:
    st.header("Dataset 1 exploration: Stress_Dataset")

    st.markdown("### Dataset summary")
    colsA,colsB,colsC=st.columns(3)
    colsA.metric("Rows",df1.shape[0])
    colsB.metric("Columns",df1.shape[1])
    colsC.metric("Missing values", df1.isna().sum().sum())

    st.divider()


    numerical_cols1 = df1.select_dtypes(include=[np.number]).columns.tolist()
    # Histogram
    st.markdown('<div class="section-title">📈 Histogram</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="info-box">
    <div class="info-title">How to interpret this histogram</div>
    • Shows the distribution of a variable.<br>
    • Look for peaks (common values), skewness, and spread.<br>
    • The smooth curve (KDE) helps you see the overall shape of the data.
</div>
""", unsafe_allow_html=True)

    col1,col2=st.columns([1,2])
    with col1:
        col_hist1 = st.selectbox("Select numerical column", numerical_cols1, key="hist_tab1")
    
    with col2:
        fig_hist1, ax_hist1 = plt.subplots(figsize=(6, 4)) 
        sns.histplot(df1[col_hist1], kde=True, ax=ax_hist1, color="#4f83cc")
        ax_hist1.tick_params(labelsize=8)
        st.pyplot(fig_hist1, use_container_width=True)
 
    st.divider()
    # Box plot
    st.markdown('<div class="section-title">📦 Box plot</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="info-box">
    <div class="info-title">How to interpret this box plot</div>
    • The box represents the middle 50% of values (IQR).<br>
    • The line inside the box is the median.<br>
    • Dots outside the whiskers indicate potential outliers.<br>
    • Longer whiskers/box = greater spread in the data.
</div>
""", unsafe_allow_html=True)
    
    col1,col2=st.columns([1,2])
    with col1:
        col_box1 = st.selectbox("Select numerical column", numerical_cols1, key="box_tab1")
    with col2:
        fig_box1, ax_box1 = plt.subplots(figsize=(6, 4))
        sns.boxplot(y=df1[col_box1], ax=ax_box1, color="#fb8072")
        ax_box1.set_ylabel(col_box1, fontsize=8)
        ax_box1.tick_params(axis="both", labelsize=7)  
        st.pyplot(fig_box1, use_container_width=True)
        
    st.divider()

    # Correlation heatmap
    st.markdown('<div class="section-title">Correlation heatmap (top 10)</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="info-box">
    <div class="info-title">🔗 How to interpret this heatmap</div>
    • Colors show how two variables move together.<br>
    • Red = positive correlation (variables rise together).<br>
    • Blue = negative correlation (one rises while the other falls).<br>
    • Light/white = weak or no relationship.<br>
    • Strong colors highlight pairs worth investigating.
</div>
""", unsafe_allow_html=True)


    # compute correlations and keep top 10 features by variance (or any criterion)
    corr1 = df1[numerical_cols1].corr()

    # optional: take only first/top 10 columns & rows
    top_cols1 = corr1.columns[:10]
    corr_small1 = corr1.loc[top_cols1, top_cols1]

    fig_corr1, ax_corr1 = plt.subplots(figsize=(4, 3))
    sns.heatmap(
        corr_small1,
        annot=False,          # <- no numbers to avoid clutter
        cmap="coolwarm",
        center=0,
        ax=ax_corr1,
        cbar_kws={"shrink": 0.6, "pad": 0.02},
    )

    ax_corr1.tick_params(axis="x", labelrotation=90, labelsize=6)
    ax_corr1.tick_params(axis="y", labelsize=6)
    st.pyplot(fig_corr1)

    st.markdown("""
<div class="info-box">
    <div class="info-title">💡 Insights</div>
    • Stress symptoms cluster together: palpitations, anxiety, sleep issues, headaches, irritability, and concentration problems.<br>
    • Emotional tension, poor sleep, and somatic symptoms are inter‑correlated.<br>
    • Irritability and concentration difficulties are linked to headaches and stress.<br>
    • Gender and age have little impact on these stress-related complaints.
</div>
""", unsafe_allow_html=True)

    st.divider()

    # Filtering tool (numeric)
    st.markdown('<div class="section-title">🔍 Filter data (numeric)</div>', unsafe_allow_html=True)
    selected_col1 = st.selectbox("Select variable", numerical_cols1, key="filter_tab1")
    min_val1, max_val1 = float(df1[selected_col1].min()), float(df1[selected_col1].max())
    filter_range1 = st.slider(
        f"Range for {selected_col1}",
        min_val1,
        max_val1,
        (min_val1, max_val1),
        key="slider_tab1",
    )
    filtered_df1 = df1[df1[selected_col1].between(filter_range1[0], filter_range1[1])]
    st.metric("Filtered records", len(filtered_df1))
    st.dataframe(filtered_df1.head(), use_container_width=True)

# ---------- TAB 2 ----------
with tab2:
    st.header("Dataset 2 exploration: StressLevelDataset")

    numerical_cols2 = df2.select_dtypes(include=[np.number]).columns.tolist()

    st.markdown("### Dataset summary")
    colsA,colsB,colsC=st.columns(3)
    colsA.metric("Rows",df2.shape[0])
    colsB.metric("Columns",df2.shape[1])
    colsC.metric("Missing values", df2.isna().sum().sum())

    st.divider()

    
    # Histogram
    st.markdown('<div class="section-title">📈 Histogram</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="info-box">
    <div class="info-title">How to interpret this histogram</div>
    • Shows the distribution of a variable.<br>
    • Look for peaks (common values), skewness, and spread.<br>
    • The smooth curve (KDE) helps you see the overall shape of the data.
</div>
""", unsafe_allow_html=True)
    col1,col2=st.columns([1,2])
    with col1:
        col_hist2 = st.selectbox("Select numerical column", numerical_cols2, key="hist_tab2")
    with col2:
        fig_hist2, ax_hist2 = plt.subplots(figsize=(6, 4))
        sns.histplot(df2[col_hist2], kde=True, ax=ax_hist2, color="#4f83cc")
        ax_hist2.tick_params(labelsize=8)
        st.pyplot(fig_hist2, use_container_width=False)

    st.divider()
    # Box plot
    st.markdown('<div class="section-title">📦 Box plot</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="info-box">
    <div class="info-title">How to interpret this box plot</div>
    • The box represents the middle 50% of values (IQR).<br>
    • The line inside the box is the median.<br>
    • Dots outside the whiskers indicate potential outliers.<br>
    • Longer whiskers/box = greater spread in the data.
</div>
""", unsafe_allow_html=True)
    
    col1,col2=st.columns([1,2])
    with col1:
        col_box2 = st.selectbox("Select numerical column", numerical_cols2, key="box_tab2")
    with col2:
        fig_box2, ax_box2 = plt.subplots(figsize=(6, 4))
        sns.boxplot(y=df2[col_box2], ax=ax_box2, color="#fb8072")
        ax_box2.tick_params(labelsize=8)
        st.pyplot(fig_box2, use_container_width=False)

    st.divider()
    # Correlation heatmap
    st.markdown('<div class="section-title">🔗 Correlation heatmap (top 10)</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="info-box">
    <div class="info-title">How to interpret this heatmap</div>
    • Colors show how two variables move together.<br>
    • Red = positive correlation (variables rise together).<br>
    • Blue = negative correlation (one rises while the other falls).<br>
    • Light/white = weak or no relationship.<br>
    • Strong colors highlight pairs worth investigating.
</div>
""", unsafe_allow_html=True)

    corr2 = df2[numerical_cols2].corr()
    top_cols2 = corr2.columns[:10]
    corr_small2 = corr2.loc[top_cols2, top_cols2]

    fig_corr2, ax_corr2 = plt.subplots(figsize=(4, 3))
    sns.heatmap(
        corr_small2,
        annot=False,
        cmap="coolwarm",
        center=0,
        ax=ax_corr2,
        cbar_kws={"shrink": 0.6, "pad": 0.02},
    )

    ax_corr2.tick_params(axis="x", labelrotation=90, labelsize=6)
    ax_corr2.tick_params(axis="y", labelsize=6)
    st.pyplot(fig_corr2, use_container_width=False)

    st.markdown("""
<div class="info-box">
    <div class="info-title">💡 Insights</div>
    • Anxiety clusters with depression, headache, breathing issues, noise, and poor living conditions.<br>
    • Higher self-esteem links to lower anxiety, depression, and mental-health concerns.<br>
    • Depression, headache, and blood pressure are positively inter‑correlated.<br>
    • Poor sleep associates with higher anxiety, depression, headaches, and breathing problems.<br>
    • Noise correlates with anxiety, depression, and breathing issues, and negatively with living conditions.
</div>
""", unsafe_allow_html=True)

    st.divider()
    # Filtering tool (numeric)
    st.markdown('<div class="section-title">🔍 Filter data (numeric)</div>', unsafe_allow_html=True)
    selected_col2 = st.selectbox("Select variable", numerical_cols2, key="filter_tab2")
    min_val2, max_val2 = float(df2[selected_col2].min()), float(df2[selected_col2].max())
    filter_range2 = st.slider(
        f"Range for {selected_col2}",
        min_val2,
        max_val2,
        (min_val2, max_val2),
        key="slider_tab2",
    )
    filtered_df2 = df2[df2[selected_col2].between(filter_range2[0], filter_range2[1])]
    st.metric("Filtered records", len(filtered_df2))
    st.dataframe(filtered_df2.head(), use_container_width=True)
