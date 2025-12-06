import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Risk Groups", page_icon="🔥", layout="wide")

st.markdown("""
<h1 style='text-align:center; color:#b91c1c;'>🔥 Student Risk Groups</h1>
<p style='text-align:center; font-size:1.1rem;'>Identify patterns and segment students into low, medium, and high risk groups.</p>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("StressLevelDataset.csv")
    return df

df = load_data()

numcols=df.select_dtypes(include=np.number).columns
scaler=StandardScaler()
scaled=scaler.fit_transform(df[numcols])
kmeans=KMeans(n_clusters=3, random_state=42)
df["cluster"]=kmeans.fit_predict(scaled)

cluster_mean=df.groupby("cluster")["stress_level"].mean().sort_values()
risk_mapping={cluster_mean.index[0]:"Low Risk", cluster_mean.index[1]:"Medium Risk", cluster_mean.index[2]:"High Risk"}
df["risk_group"]=df["cluster"].map(risk_mapping)

col1,col2,col3=st.columns(3)
col1.metric("Low-risk Students",(df["risk_group"]=="Low Risk").sum())
col2.metric("Medium-risk Students",(df["risk_group"]=="Medium Risk").sum())
col3.metric("High-risk Students",(df["risk_group"]=="High Risk").sum())

st.dataframe(df[["stress_level","risk_group"]].head(), use_container_width=True)

st.subheader("Visualisation")
fig, ax = plt.subplots(figsize=(5,4))
sns.boxplot(data=df, x="risk_group", y="stress_level", palette="Set2", ax=ax)
ax.set_title("Stress Level Distribution by Risk Group")
st.pyplot(fig)