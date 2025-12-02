import streamlit as st
import pandas as pd

st.tile("📁Overview")

@st.cache_data
def load_data():
    df1=pd.read_csv("../Stress_Dataset.csv")
    df2=pd.read_csv("../StressLevelDataset.csv")
    return df1, df2

df1, df2=load_data()

tab1, tab2=st.tabs(["📄Stress_Dataset.csv", "📄StressLevelDataset.csv"])

with tab1:
    st.header("Dataset 1: Stress_Dataset.csv")
    st.write("This dataset contains information about students' stress levels along with various demographic and lifestyle factors.")
    st.write(df1.head()) 
    st.write(df1.describe(include='all'))

with tab2:
    st.header("Dataset 2: StressLevelDataset.csv")
    st.write("This dataset includes additional information about students' academic performance and stress levels.")
    st.write(df2.head())
    st.write(df2.describe(include='all'))
