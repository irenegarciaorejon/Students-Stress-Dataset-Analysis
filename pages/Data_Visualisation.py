import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score


st.title("📈 Exploratory Data Analysis")
@st.cache_data
def load_data():
    df1=pd.read_csv("../Stress_Dataset.csv")
    df2=pd.read_csv("../StressLevelDataset.csv")
    return df1, df2


df1, df2=load_data()

tab1, tab2=st.tabs(["📊Stress_Dataset.csv", "📊StressLevelDataset.csv"])
with tab1:
    st.header("Dataset 1 exploration")
    st.subheader("Preview")
    st.dataframe(df1.head())
    st.subheader("Statistical Summary")
    st.write(df1.describe(include='all'))   
    numerical_cols=df1.select_dtypes(include=[np.number]).columns.tolist()
    st.subheader("Histogram")
    col=st.selectbox("Select Numerical Column for Histogram", numerical_cols, key='hist1')
    
    fig, ax=plt.subplots()
    sns.histplot(df1[col], kde=True, ax=ax)
    ax.set_title(f'Histogram of {col}')
    st.pyplot(fig)

    st.subheader("Box Plot")
    col_box=st.selectbox("Select Numerical Column for Box Plot", numerical_cols, key='box1')
    fig_box, ax_box=plt.subplots()
    sns.boxplot(y=df1[col_box], ax=ax_box)
    ax_box.set_title(f'Box Plot of {col_box}')
    st.pyplot(fig_box)

    st.subheader("Correlation Heatmap")
    fig_corr, ax_corr=plt.subplots(figsize=(10, 8))
    sns.heatmap(df1[numerical_cols].corr(), annot=True, fmt=".2f", cmap='coolwarm', ax=ax_corr) 
    st.pyplot(fig_corr)

    st.subheader("Filtering tool")
    selected_cols=st.selectbox("Select variable to filter", numerical_cols, key='filter1')
    min_val, max_val=float(df1[selected_cols].min()), float(df1[selected_cols].max())
    filter_range=st.slider(f"Select range for {selected_cols}", min_val, max_val, (min_val, max_val), key='slider1')

    filtered_df1=df1[df1[selected_cols].between(filter_range[0], filter_range[1])]
    st.write("Filtered data:", filtered_df1)

with tab2:
    st.header("Dataset 2 exploration")
    st.subheader("Preview")
    st.dataframe(df2.head())
    st.subheader("Statistical Summary")
    st.write(df2.describe(include='all'))   
    numerical_cols2=df2.select_dtypes(include=[np.number]).columns.tolist()
    
    st.subheader("Histogram")
    col2=st.selectbox("Select Numerical Column for Histogram", numerical_cols2, key='hist2')
    fig, ax=plt.subplots()
    sns.histplot(df2[col2], kde=True, ax=ax)
    ax.set_title(f'Histogram of {col2}')
    st.pyplot(fig)

    st.subheader("Box Plot")
    col2_box=st.selectbox("Select Numerical Column for Box Plot", numerical_cols2, key='box2')
    fig, ax=plt.subplots()
    sns.boxplot(y=df2[col2_box], ax=ax)
    ax.set_title(f'Box Plot of {col2_box}')
    st.pyplot(fig)

    st.subheader("Correlation Heatmap")
    fig_corr, ax_corr=plt.subplots(figsize=(10, 8))
    sns.heatmap(df2[numerical_cols2].corr(), annot=True, fmt=".2f", cmap='coolwarm', ax=ax_corr) 
    st.pyplot(fig_corr)

    st.subheader("Filtering tool")
    selected_cols2=st.selectbox("Select variable to filter", numerical_cols2, key='filter2')
    min_val, max_val=float(df2[selected_cols2].min()), float(df2[selected_cols2].max())
    filter_range2=st.slider(f"Select range for {selected_cols2}", min_val, max_val, (min_val, max_val), key='slider1')

    filtered_df2=df2[df2[selected_cols2].between(filter_range2[0], filter_range2[1])]
    st.write("Filtered data:", filtered_df2)

