import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Risk Groups", page_icon="🔥", layout="wide")

# ---- HEADER ----
st.markdown(
    """
    <h1 style='text-align:center; color:#b91c1c;'>🔥 Student Risk Groups</h1>
    <p style='text-align:center; font-size:1.05rem; color:#4b5563;'>
        Identify patterns and segment students into low, medium, and high risk groups.
    </p>
    <p style='text-align:center; font-size:0.95rem; color:#6b7280;'>
        Data source: <b>StressLevelDataset.csv</b>
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

@st.cache_data
def load_data():
    df = pd.read_csv("StressLevelDataset.csv")
    # ensure stress_level is integer (0,1,2)
    df["stress_level"] = df["stress_level"].astype(int)
    return df

df = load_data()

# ---- CLUSTERING ----
numcols = df.select_dtypes(include=np.number).columns
scaler = StandardScaler()
scaled = scaler.fit_transform(df[numcols])

kmeans = KMeans(n_clusters=3, random_state=42, n_init="auto")
df["cluster"] = kmeans.fit_predict(scaled)

cluster_mean = df.groupby("cluster")["stress_level"].mean().sort_values()
risk_mapping = {
    cluster_mean.index[0]: "Low risk",
    cluster_mean.index[1]: "Medium risk",
    cluster_mean.index[2]: "High risk",
}
df["risk_group"] = df["cluster"].map(risk_mapping)

palette = {"Low risk": "#22c55e", "Medium risk": "#fb923c", "High risk": "#ef4444"}
level_palette = {0: "#e5e7eb", 1: "#60a5fa", 2: "#f97316"}  # for stacked bars

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("### 🔥 Risk groups")

    with st.expander("🧭 How to use this page", expanded=True):
        st.markdown(
            """
            1. Review the **overall counts** of low, medium, and high‑risk students.  
            2. Check how each group is composed in terms of **stress levels 0/1/2**.  
            3. Select a risk group to **inspect example students** and details.
            """
        )

    with st.expander("📊 Data notes", expanded=False):
        st.markdown(
            """
            - Clusters are computed with **K‑Means (k=3)** on all numeric features.  
            - Risk groups are labeled by **average stress_level** (higher = higher risk).  
            - Stress levels are coded as <b>0 = low</b>, <b>1 = moderate</b>, <b>2 = high</b>.
            """
        )

# ---- TOP METRICS ----
st.subheader("Step 1 · Overview of risk groups")

col1, col2, col3 = st.columns(3)
col1.metric("Low‑risk students", int((df["risk_group"] == "Low risk").sum()))
col2.metric("Medium‑risk students", int((df["risk_group"] == "Medium risk").sum()))
col3.metric("High‑risk students", int((df["risk_group"] == "High risk").sum()))

st.markdown(
    """
    <div style="background-color:#ecfdf5; border-radius:12px; padding:0.9rem 1rem;
                border:1px solid #bbf7d0; font-size:0.9rem; color:#065f46;
                margin-top:0.7rem;">
        <b>What you can do here</b><br>
        • Get a quick sense of how many students fall into each risk group.<br>
        • Use these numbers to decide where to focus your attention first  
          (for example, if high‑risk counts are large).
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("&nbsp;")

# ---- STACKED BAR: COMPOSITION BY STRESS LEVEL ----
st.subheader("Step 2 · Stress level composition within each risk group")

# compute proportions of stress_level 0/1/2 per risk group
comp = (
    df.groupby(["risk_group", "stress_level"])
    .size()
    .reset_index(name="count")
)
total_per_group = comp.groupby("risk_group")["count"].transform("sum")
comp["pct"] = comp["count"] / total_per_group

# pivot to wide for stacked bars
pivot = comp.pivot(index="risk_group", columns="stress_level", values="pct").fillna(0)
pivot = pivot.reindex(["Low risk", "Medium risk", "High risk"])

fig_comp, ax_comp = plt.subplots(figsize=(7, 4))

bottom = np.zeros(len(pivot))
levels_sorted = sorted(pivot.columns)  # 0,1,2

for lvl in levels_sorted:
    values = pivot[lvl].values
    ax_comp.bar(
        pivot.index,
        values,
        bottom=bottom,
        label=f"Stress level {lvl}",
        color=level_palette[lvl],
    )
    bottom += values

ax_comp.set_ylabel("Proportion of students")
ax_comp.set_xlabel("")
ax_comp.set_title("Stress level composition per risk group")
ax_comp.set_ylim(0, 1)
ax_comp.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{int(y*100)}%"))
ax_comp.grid(axis="y", linestyle="--", alpha=0.3)
ax_comp.legend(title="Stress level")

st.pyplot(fig_comp)

st.markdown(
    """
    <div style="background-color:#eff6ff; border-radius:12px; padding:0.9rem 1rem;
                border:1px solid #bfdbfe; font-size:0.9rem; color:#1d4ed8;
                margin-top:0.4rem;">
        <b>What this chart shows</b><br>
        • Each bar is a risk group, split into the percentage of students at stress levels 0, 1, and 2.<br>
        • Darker segments (level 2) indicate a higher share of students with <b>high</b> stress.<br>
        • Compare groups to see which one concentrates more level‑2 students.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="background-color:#fef9c3; border-radius:12px; padding:0.9rem 1rem;
                border:1px solid #facc15; font-size:0.9rem; color:#854d0e;
                margin-top:0.6rem;">
        💡 <b>Key insights</b><br>
        • Look for groups where the <b>level‑2 (high)</b> segment dominates — those are your priority.<br>
        • A group with many level‑0 students is more stable, even if its size is large.<br>
        • Use this together with the counts above to balance <b>severity</b> and <b>volume</b>.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ---- GROUP DETAIL INSPECTOR ----
st.subheader("Step 3 · Inspect a specific risk group")

selected_group = st.selectbox(
    "Select a risk group to inspect:",
    options=["Low risk", "Medium risk", "High risk"],
)

group_df = df[df["risk_group"] == selected_group].copy()

st.markdown(
    f"Showing a sample of students classified as **{selected_group}** "
    f"(total: **{len(group_df)}**)."
)

# show all columns for that group (head)
st.dataframe(
    group_df.head(20),
    use_container_width=True,
)

st.markdown(
    """
    <div style="background-color:#fefce8; border-radius:12px; padding:0.9rem 1rem;
                border:1px solid #facc15; font-size:0.9rem; color:#854d0e;
                margin-top:0.4rem;">
        <b>What you can do here</b><br>
        • Inspect individual rows to see which features are common in this risk group.<br>
        • Use this to generate hypotheses (e.g., certain schedules or habits appearing in high‑risk groups).
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("&nbsp;")

with st.expander("📈 Stress distribution in this group", expanded=False):
    fig_strip, ax_strip = plt.subplots(figsize=(5, 3))

    sns.stripplot(
        data=group_df,
        x="risk_group",
        y="stress_level",
        jitter=0.15,
        size=6,
        color=palette[selected_group],
        ax=ax_strip,
    )

    ax_strip.set_xlabel("")
    ax_strip.set_ylabel("Stress level")
    ax_strip.set_title(f"Stress level distribution in {selected_group}")
    ax_strip.grid(axis="y", linestyle="--", alpha=0.3)

    st.pyplot(fig_strip)

    st.markdown(
        """
        <div style="background-color:#f5f3ff; border-radius:12px; padding:0.8rem 1rem;
                    border:1px solid #ddd6fe; font-size:0.9rem; color:#4c1d95;
                    margin-top:0.3rem;">
            <b>How to read this mini chart</b><br>
            • Each dot is a student in the selected risk group; its height is the stress_level value.<br>
            • If dots are tightly packed at one level, most students share that stress level.<br>
            • If dots appear at 0, 1 and 2, the group contains a mix of low, moderate and high stress.
        </div>
        """,
        unsafe_allow_html=True,
    )
