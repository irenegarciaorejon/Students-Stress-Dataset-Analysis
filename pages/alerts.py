import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="Alerts", page_icon="🚨", layout="wide")

# -------- SIDEBAR --------
with st.sidebar:
    st.markdown("### 🚨 Alerts overview")

    with st.expander("🎯 What is this page?", expanded=True):
        st.markdown(
            """
            - Detect students who may be under **high stress**.  
            - Compare a simple **rule** with a **Random Forest model**.  
            - Highlight **highest‑priority** cases flagged by both.
            """
        )

    with st.expander("📑 How to read the tabs", expanded=False):
        st.markdown(
            """
            - **⚖️ Rule‑based alerts** → uses recorded `stress_level` (0–2).  
            - **🤖 ML‑based alerts** → uses model‑predicted stress levels.  
            - **⭐ Prioritization** → students flagged by **both** methods.
            """
        )

    with st.expander("🎚️ Threshold tips", expanded=False):
        st.markdown(
            """
            - 🔽 Lower thresholds → **more** students flagged (higher sensitivity).  
            - 🔼 Higher thresholds → **fewer**, more **severe** cases.  
            - Use different thresholds to explore “what‑if” scenarios.
            """
        )

    with st.expander("💡 Tips for analysis", expanded=False):
        st.markdown(
            """
            - Start with default thresholds; adjust if lists are too long/short.  
            - Use the **inspectors** to review each student's feature profile.  
            - Export tables to share cases or document interventions.
            """
        )

# -------- HEADER --------
st.markdown(
    """
    <h1 style='text-align:center; color:#b91c1c; margin-bottom:0.4rem;'>🚨 Stress Alerts</h1>
    <p style='text-align:center; font-size:1.05rem; color:#4b5563;'>
        Automatically detect students who may require immediate attention based on rule-based thresholds and machine learning predictions.
    </p>
    <p style='text-align:center; font-size:0.95rem; color:#6b7280;'>
        Data sources: <b>Stress_Dataset.csv</b> and <b>StressLevelDataset.csv</b>
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

@st.cache_data
def load_data():
    df1 = pd.read_csv("Stress_Dataset.csv")
    df1.rename(
        columns={"Which type of stress do you primarily experience?": "stress_type"},
        inplace=True,
    )
    df1 = df1[(df1["Age"] >= 18) & (df1["Age"] <= 21)]

    df2 = pd.read_csv("StressLevelDataset.csv")
    return df1, df2

df1, df2 = load_data()

# --------- MODEL PREP  ----------
X = df2.drop(columns=["stress_level"])
y = df2["stress_level"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y,
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train_scaled, y_train)

y_pred_test = rf.predict(X_test_scaled)

df_test = X_test.copy()
df_test["true_stress_level"] = y_test
df_test["ml_pred"] = y_pred_test

# -------- TABS --------
tab_rule, tab_ml, tab_prior = st.tabs(
    ["⚖️ Rule‑based alerts", "🤖 ML‑based alerts", "⭐ Prioritization"]
)

# =====================================================
# TAB 1: RULE‑BASED ALERTS
# =====================================================
with tab_rule:
    col_rule_text, col_rule_controls = st.columns([2, 1])

    with col_rule_text:
        st.subheader("Rule‑Based Alerts")
        st.markdown(
            """
            This view flags students directly from the **observed** `stress_level` in the dataset (0–2).  
            It is transparent and easy to explain: anyone above the chosen threshold is marked as **at risk**.
            """
        )

    with col_rule_controls:
        st.markdown("#### Threshold settings")
        rule_threshold = st.slider(
            "Minimum stress level to raise an alert",
            min_value=0,
            max_value=2,
            value=2,
            step=1,
            help="Students with stress_level ≥ this value will be included in the rule-based alert list.",
            key="rule_threshold",
        )

    df2["alert_flag"] = df2["stress_level"] >= rule_threshold
    rule_alerts = df2[df2["alert_flag"]].copy()

    col_rule_metric, col_rule_info = st.columns([1, 2])

    with col_rule_metric:
        st.metric(
            "Students needing attention (rule‑based)",
            value=len(rule_alerts),
            help="Number of students whose recorded stress_level exceeds the selected threshold.",
        )

    with col_rule_info:
        st.empty()  

    st.dataframe(
        rule_alerts.head(20),
        use_container_width=True,
        height=260,
    )

    st.markdown("### 🔍 Inspect individual students (rule‑based)")

    if len(rule_alerts) > 0:
        selected_idx_rule = st.selectbox(
            "Select a student from the rule‑based alert list",
            options=rule_alerts.index.tolist(),
            format_func=lambda x: f"Student #{x}",
            key="rule_select",
        )

        student_rule = rule_alerts.loc[selected_idx_rule]

        st.markdown(
            f"""
            <div style="background-color:#eff6ff; border-radius:12px; padding:1rem 1.2rem;
                        border:1px solid #bfdbfe; margin-bottom:1rem;">
                <h4 style="margin:0 0 0.4rem 0; color:#1d4ed8;">Student #{selected_idx_rule}</h4>
                <p style="margin:0; color:#374151;">
                    <b>Recorded stress level:</b> {int(student_rule["stress_level"])}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("&nbsp;")  

        st.markdown("**Full feature profile**")
        st.dataframe(
            pd.DataFrame(student_rule).rename(columns={selected_idx_rule: "value"}),
            width=450,
            height=260,
        )

    else:
        st.caption("No students currently meet the rule‑based alert threshold.")

# =====================================================
# TAB 2: ML‑BASED ALERTS
# =====================================================
with tab_ml:
    col_ml_text, col_ml_controls = st.columns([2, 1])

    with col_ml_text:
        st.subheader("Machine Learning‑Based Alerts")
        st.markdown(
            """
            This view uses a **Random Forest** model trained on the dataset to predict `stress_level`  
            for a held‑out test set (30% of the data). Students with high **predicted** stress  
            are highlighted as potential risk cases.
            """
        )

        accuracy = (df_test["ml_pred"] == df_test["true_stress_level"]).mean()
        st.markdown(
            f"""
            <div style="background-color:#ecfdf5; border-radius:10px; padding:0.6rem 0.8rem;
                        border:1px solid #bbf7d0; font-size:0.9rem; color:#166534; margin-top:0.6rem;">
                <b>Model performance</b><br>
                ✅ Random Forest accuracy on the test set: <b>{accuracy:.2%}</b>.<br>
                📊 Trained on <b>70%</b> of the data, evaluated on <b>30%</b>.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("&nbsp;")  


    with col_ml_controls:
        st.markdown("#### Model settings")
        ml_threshold = st.slider(
            "Minimum predicted stress level (ML)",
            min_value=0,
            max_value=2,
            value=2,
            step=1,
            help="Students with predicted stress_level ≥ this value will be included in the ML alert list.",
            key="ml_threshold",
        )

    ml_alerts = df_test[df_test["ml_pred"] >= ml_threshold].copy()

    col_ml_metric, col_ml_info = st.columns([1, 2])

    with col_ml_metric:
        st.metric(
            "Students needing attention (ML)",
            value=len(ml_alerts),
            help="Number of students in the test set whose predicted stress_level exceeds the selected threshold.",
        )

    with col_ml_info:
        st.empty()

    st.dataframe(
        ml_alerts.head(20),
        use_container_width=True,
        height=260,
    )

    st.markdown("### 🔍 Inspect individual students (ML alerts)")

    if len(ml_alerts) > 0:
        selected_idx_ml = st.selectbox(
            "Select a student from the ML alert list",
            options=ml_alerts.index.tolist(),
            format_func=lambda x: f"Student #{x}",
            key="ml_select",
        )

        student_ml = ml_alerts.loc[selected_idx_ml]

        st.markdown(
            f"""
            <div style="background-color:#eff6ff; border-radius:12px; padding:1rem 1.2rem;
                        border:1px solid #bfdbfe; margin-bottom:1rem;">
                <h4 style="margin:0 0 0.4rem 0; color:#1d4ed8;">Student #{selected_idx_ml}</h4>
                <p style="margin:0; color:#374151;">
                    <b>True stress level:</b> {int(student_ml["true_stress_level"])}
                    &nbsp;|&nbsp;
                    <b>Predicted:</b> {int(student_ml["ml_pred"])}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("&nbsp;")  

        st.markdown("**Full feature profile**")
        feature_cols_ml = [c for c in ml_alerts.columns if c not in ["true_stress_level", "ml_pred"]]
        st.dataframe(
            pd.DataFrame(student_ml[feature_cols_ml]).rename(
                columns={selected_idx_ml: "value"}
            ),
            width=450,
            height=260,
        )

    else:
        st.caption("No students currently meet the ML alert threshold.")

# =====================================================
# TAB 3: PRIORITIZATION
# =====================================================
with tab_prior:
    st.subheader("Highest‑Priority Students")

    st.markdown(
        """
        This view focuses on students who are **flagged by both methods**  
        (rule‑based and ML‑based). Reviewing these cases first can help you  
        allocate limited support resources more efficiently.
        """
    )

    st.markdown(
        """
        <div style="background-color:#fffbeb; border-radius:10px; padding:0.8rem 1rem;
                    border:1px solid #fef3c7; color:#92400e; font-size:0.95rem; margin-top:0.6rem;">
            💡 <b>Why these students matter</b><br>
            • They are above the selected thresholds <b>in the data</b> (rule‑based).<br>
            • They are also above the thresholds <b>in the model prediction</b> (ML).<br>
            • Consider them your <b>top priority</b> for follow‑up and support.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("&nbsp;")  

    df2["alert_flag"] = df2["stress_level"] >= rule_threshold
    rule_alerts = df2[df2["alert_flag"]].copy()

    common_index = set(rule_alerts.index).intersection(set(df_test.index))
    overlap = df_test.loc[list(common_index)].copy()
    overlap = overlap[overlap["ml_pred"] >= ml_threshold]
    overlap = overlap[overlap["true_stress_level"] >= rule_threshold]

    col_prior_metric, col_prior_text = st.columns([1, 2])

    with col_prior_metric:
        st.metric(
            "Highest‑priority students",
            value=len(overlap),
            help="Students flagged by both rule-based and ML-based alerts.",
        )

    with col_prior_text:
        st.empty()

    if not overlap.empty:
        st.dataframe(
            overlap.head(20),
            use_container_width=True,
            height=260,
        )

        st.markdown("### 🔍 Inspect highest‑priority students")

        selected_idx_overlap = st.selectbox(
            "Select a student from the combined alert list",
            options=overlap.index.tolist(),
            format_func=lambda x: f"Student #{x}",
            key="prior_select",
        )

        overlap_row = overlap.loc[selected_idx_overlap]

        st.markdown(
            f"""
            <div style="background-color:#fffbeb; border-radius:12px; padding:1rem 1.2rem;
                        border:1px solid #fef3c7; margin-bottom:1rem;">
                <h4 style="margin:0 0 0.4rem 0; color:#a16207;">Student #{selected_idx_overlap}</h4>
                <p style="margin:0; color:#374151;">
                    <b>True stress level:</b> {int(overlap_row["true_stress_level"])}
                    &nbsp;|&nbsp;
                    <b>Predicted:</b> {int(overlap_row["ml_pred"])}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("&nbsp;")  

        st.markdown("**Full feature profile**")
        feature_cols_overlap = [c for c in overlap.columns if c not in ["true_stress_level", "ml_pred"]]
        st.dataframe(
            pd.DataFrame(overlap_row[feature_cols_overlap]).rename(
                columns={selected_idx_overlap: "value"}
            ),
            width=450,
            height=260,
        )

    else:
        st.caption(
            "Currently, no students are simultaneously flagged by the selected rule‑based and ML thresholds."
        )
