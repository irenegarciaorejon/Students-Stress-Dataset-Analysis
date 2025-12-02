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


st.set_page_config(page_title="Stress Monitor - Institutions Educatives", layout="wide")



@st.cache_data
def preprocess_data(df):
    df=df.copy()
    df=df[(df['Age']>=18) & (df['Age']<=21)].reset_index(drop=True)
    return df

def detect_risk(df,score_cols='stress_level'):
    output=df.copy()
    if pd.api.types.is_numeric_dtype(output[score_cols]):
        q75=output[score_cols].quantile(0.75)
        q25=output[score_cols].quantile(0.25)
        output['Risk_Level']='Low'
        output.loc[output[score_cols]>q75,'Risk_Level']='High'
        output.loc[(output[score_cols]<=q75) & (output[score_cols]>=q25),'Risk_Level']='Medium'
    else:
        counts=output[score_cols].value_counts(normalize=True)
        rare=counts[counts<0.1].index.tolist()
        output['Risk_Level']=output[score_cols].apply(lambda x: 'High' if x in rare else 'Medium')
    return output

def cluster_risk(df,feature_cols, n_clusters=3 ):
    output=df.copy()
    X=output[feature_cols].select_dtypes(include=[np.number]).fillna(0)
    scaler=StandardScaler()
    X_scaled=scaler.fit_transform(X)
    kmeans=KMeans(n_clusters=n_clusters, random_state=42)
    labels=kmeans.fit_predict(X_scaled)
    output['cluster']=labels
    cluster_scores=output.groupby("cluster")[feature_cols[0]].mean().sort_values()
    mapping={cluster_scores.index[0]:'Low', cluster_scores.index[1]:'Medium'}
    if len(cluster_scores.index)>2:
        mapping[cluster_scores.index[2]]='High'
    output['Risk_Cluster']=output['cluster'].map(lambda x: mapping.get(x,'Medium'))
    return output, kmeans

def recommendations(row):
    if 'risk_level' in row and row['risk_level'] == 'High':
        return "Recommendation: refer to counselor and schedule an interview within a week."
    if 'cluster_risk' in row and row['cluster_risk'] == 'High':
        return "Recommendation:proactive contact and psychoeducational support."
    if 'stress_level' in row and pd.notna(row['stress_level']):
        if row['stress_level'] >= 3:
            return "Recommendation: continuous monitoring and early intervention."
        elif row['stress_level'] >= 2:
            return "Recommendation: offer self-help and monitoring resources."
    return "Recommendation: routine monitoring and access to emotional education resources."




st.title("Stress Monitor - Institutions Educatives Platform")
st.markdown("""
This application helps educational institutions monitor and manage student stress levels using data visualization, clustering, and classification techniques.
    Pages:
    - Overview
    - Data Visualization Analysis
    - Detection of risk groups
    - Alerts
    - Recommendations
    - Model Evaluation
""")
