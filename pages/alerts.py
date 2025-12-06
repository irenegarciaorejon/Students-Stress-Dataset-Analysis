import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="Alerts", page_icon="🚨",layout="wide")

st.markdown("""
<h1 style='text-align:center; color:#dc2626;'>🚨 Stress Alerts</h1>
<p style='text-align:center; font-size:1.1rem;'>Automatically detect students who may require immediate attention based on stress indicators.</p>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df1 = pd.read_csv("Stress_Dataset.csv")
    df1.rename(columns={"Which type of stress do you primarily experience?":"stress_type"}, inplace=True)
    df1 = df1[(df1["Age"]>=18) & (df1["Age"]<=21)]

    df2 = pd.read_csv("StressLevelDataset.csv")
    return df1, df2

df1, df2 = load_data()

st.subheader("Rule-Based Alerts")
#ADD SAMLL DESCRIPTION OF HOW THEY ARE ALERTS

df2["alert_flag"]=(df2["stress_level"]>=2) #add as many as we want

alerts=df2[df2["alert_flag"]==True]

st.metric("Students Needing Attention", value=len(alerts))
#maybe introducing the id of the student they can see ther details in the dataset (ADD)
st.dataframe(alerts.head(),use_container_width=True)

st.divider()

st.subheader("Machine Learning-Based Alerts")
#ADD SAMLL DESCRIPTION OF HOW THEY ARE ALERTS

X=df2.drop("stress_level", axis=1)
y=df2["stress_level"]

rf=RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)
df2["ml_pred"]=rf.predict(X)
high_stress_ml=df2[df2["ml_pred"]>=2]

st.metric("Students Needing Attention (ML)", value=len(high_stress_ml))
st.dataframe(high_stress_ml.head(), use_container_width=True)

st.info("Students appearing in both list should be prioritized for intervention.", icon="ℹ️")

