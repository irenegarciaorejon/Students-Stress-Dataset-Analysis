import streamlit as st
import pandas as pd

st.set_page_config(page_title="Recommendations", page_icon="💡", layout="wide")

# ---- HEADER ----
st.markdown(
    """
    <h1 style='text-align:center; color:#1d4ed8;'>💡 Personalized Stress Recommendations</h1>
    <p style='text-align:center; font-size:1.05rem; color:#4b5563;'>
        Explore practical actions for students and institutions based on stress type.
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

@st.cache_data
def load_data():
    df = pd.read_csv("Stress_Dataset.csv")
    df.rename(
        columns={"Which type of stress do you primarily experience?": "stress_type"},
        inplace=True,
    )
    df = df[(df["Age"] >= 18) & (df["Age"] <= 21)]
    return df

df = load_data()

# ---- RECOMMENDATION DATA ----
recommendations_dict = {
    "Academic Stress": {
        "student": [
            "Create a structured, realistic study schedule.",
            "Break large assignments into smaller, manageable tasks.",
            "Ask for support from tutors, teachers, or study groups.",
        ],
        "institution": [
            "Offer workshops or templates on effective study planning.",
            "Give guidance on workload management and prioritization.",
            "Provide accessible tutoring, office hours, or peer‑support groups.",
        ],
    },
    "Physiological Stress": {
        "student": [
            "Maintain a balanced diet and drink enough water.",
            "Follow a consistent sleep schedule and limit late‑night screens.",
            "Include regular light exercise (walks, stretching, sports).",
        ],
        "institution": [
            "Share simple nutrition and sleep‑hygiene materials.",
            "Avoid scheduling demanding tasks very early or very late.",
            "Promote sports facilities, movement breaks, or wellness programs.",
        ],
    },
    "Social Stress": {
        "student": [
            "Join healthy social activities that feel safe and supportive.",
            "Set boundaries with peers when feeling overwhelmed.",
            "Seek help from trusted adults if facing bullying or exclusion.",
        ],
        "institution": [
            "Promote inclusive clubs, events, and student communities.",
            "Train staff to recognize signs of isolation and peer pressure.",
            "Implement anti‑bullying policies and confidential reporting channels.",
        ],
    },
    "Psychological Stress": {
        "student": [
            "Use techniques (journaling, reframing) to manage negative thoughts.",
            "Schedule time for hobbies and activities that feel rewarding.",
            "Reach out to a counselor or mental‑health professional if needed.",
        ],
        "institution": [
            "Organize awareness sessions on stress and emotional wellbeing.",
            "Offer low‑pressure creative or recreational activities.",
            "Ensure clear access to counseling and crisis‑support services.",
        ],
    },
    "Environmental Stress": {
        "student": [
            "Organize study space to reduce clutter and distractions.",
            "Use simple tools (earplugs, headphones) to manage noise.",
            "Spend regular time in calm outdoor or green spaces.",
        ],
        "institution": [
            "Provide quiet, well‑lit study areas and clear desk policies.",
            "Limit noise in learning spaces where possible.",
            "Highlight nearby parks or campus green areas as ‘reset’ zones.",
        ],
    },
    "Other / Mixed": {
        "student": [
            "List main personal stressors and address them step by step.",
            "Combine movement with relaxation (e.g., walks plus breathing).",
            "Track stress over time to notice patterns and triggers.",
        ],
        "institution": [
            "Support students in building individualized coping plans.",
            "Offer mixed programs (mindfulness + light activity).",
            "Use brief check‑in surveys to monitor wellbeing trends.",
        ],
    },
}

# ---- SIDEBAR ----
with st.sidebar:
    st.markdown("### 💡 Recommendations")

    with st.expander("🧭 How to use this page", expanded=True):
        st.markdown(
            """
            - **Step 1**: Choose a primary stress type to see example actions  
              for students and institutions.  
            - **Step 2**: Use the mixed toolbox to combine stress types and  
              tick only the actions that make sense for this case.
            """
        )

    with st.expander("📊 Filter & data context", expanded=False):
        st.markdown("**Stress types present in the dataset:**")
        type_counts = df["stress_type"].value_counts()
        for s, c in type_counts.items():
            st.write(f"- {s}: **{c}** students")
        st.markdown("Start with the most frequent stress types if you are designing global interventions.")

# =========================================================
# MAIN RECOMMENDATIONS
# =========================================================
st.subheader("Step 1 · Choose a primary stress type")

selected_stress_type = st.selectbox(
    "Select stress type:",
    options=list(recommendations_dict.keys()),
    index=0,
    help="This defines the main cards shown below.",
)

st.markdown("&nbsp;")

student_recs = recommendations_dict[selected_stress_type]["student"]
inst_recs = recommendations_dict[selected_stress_type]["institution"]

col_student, col_inst = st.columns(2)

with col_student:
    st.markdown("#### 👤 For students")
    st.markdown(
        "<div style='background-color:#dcfce7; border-radius:14px; padding:0.9rem 1rem;"
        "border:1px solid #86efac; font-size:0.93rem; color:#065f46; "
        "box-shadow:0 6px 18px rgba(16,185,129,0.18);'>"
        + "<br>".join([f"• {r}" for r in student_recs])
        + "</div>",
        unsafe_allow_html=True,
    )

with col_inst:
    st.markdown("#### 🏫 For institutions")
    st.markdown(
        "<div style='background-color:#dbeafe; border-radius:14px; padding:0.9rem 1rem;"
        "border:1px solid #93c5fd; font-size:0.93rem; color:#1d4ed8; "
        "box-shadow:0 6px 18px rgba(59,130,246,0.18);'>"
        + "<br>".join([f"• {r}" for r in inst_recs])
        + "</div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# =========================================================
# MIXED TOOLBOX WITH INTERACTIVE SELECTION
# =========================================================
st.subheader("Step 2 · Mixed toolbox for combined stress types")


st.markdown(
    """
    People can experience more than one type of stress at the same time.  
    Pick all stress types that apply and then choose the specific actions that feel most useful.
    """
)


mode = st.radio(
    "Mode:",
    options=["Student mode (👤)", "Institution mode (🏫)"],
    horizontal=True,
    key="toolbox_mode",
)


selected_types = st.multiselect(
    "Select one or more relevant stress types:",
    options=list(recommendations_dict.keys()),
    default=[selected_stress_type],
    help="You can pick just one type, or several if multiple apply.",
)


if selected_types:
    chosen_actions = []


    st.markdown("#### 🎯 Pick the actions you want to apply for each type")


    for t in selected_types:
        if "Student" in mode:
            actions = recommendations_dict[t]["student"]
        else:
            actions = recommendations_dict[t]["institution"]


        st.markdown(f"**{t}**")


        checked = []
        for i, a in enumerate(actions):
            is_checked = st.checkbox(
                a,
                value=True,
                key=f"{mode}_{t}_{i}",
            )
            if is_checked:
                checked.append(a)


        chosen_actions.extend([(t, a) for a in checked])
        st.markdown("&nbsp;")


    st.markdown("### ✅ Your personalized selection")


    if chosen_actions:
       # group actions by stress type
       grouped = {}
       for t, a in chosen_actions:
        grouped.setdefault(t, []).append(a)


       # build HTML with one section per stress type
       sections_html = []
       for t, acts in grouped.items():
        items_html = "".join([f"<li>{a}</li>" for a in acts])
        section = f"""
            <div style="margin-bottom:0.8rem;">
            <div style="font-weight:600; margin-bottom:0.2rem; color:#1f2937;">{t}</div>
            <ul style="margin:0 0 0.2rem 1.1rem; padding:0; color:#374151; font-size:0.9rem;">
            {items_html}
                </ul>
            </div>
            """
        sections_html.append(section)


    st.markdown(
            """
            <div style="background:linear-gradient(135deg,#eef2ff,#f9fafb); border-radius:16px;
                        padding:1rem 1.2rem; border:1px solid #e5e7eb;
                        font-size:0.93rem; color:#111827; box-shadow:0 8px 22px rgba(15,23,42,0.12);">
                <p style="margin:0 0 0.6rem 0; font-weight:600;">Your chosen actions by stress type</p>
            """
            + "".join(sections_html)
            + "</div>",
            unsafe_allow_html=True,
)
else:
    st.caption("Select at least one stress type above to see and choose actions.")