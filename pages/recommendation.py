import streamlit as st
import pandas as pd

st.set_page_config(page_title="Recommendations", page_icon="💡", layout="wide")

st.markdown("""
<h1 style='text-align:center; color:#1d4ed8;'>💡 Personalized Stress Recommendations</h1>
<p style='text-align:center; font-size:1.1rem;'>Receive tailored suggestions based on student stress type or stress-level predictions.</p>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("Stress_Dataset.csv")
    df.rename(columns={"Which type of stress do you primarily experience?":"stress_type"}, inplace=True)
    df = df[(df["Age"]>=18) & (df["Age"]<=21)]
    return df

df = load_data()


recommendations_dict = {
    "Academic Stress": [
        "Create a structured study schedule.--> Provide templates for study plans",
        "Break tasks into smaller, manageable parts.--> Teach time management skills",
        "Seek help from tutors or study groups. --> Offer tutoring services"
    ],
    "Physiological Stress": [
        "Maintain a balanced diet and stay hydrated.--> Share nutrition guides and hydration reminders",
        "Improve sleep hygiene by establishing a regular sleep schedule.--> Provide sleep tracking tools",
        "Incorporate regular physical activity into your routine. --> Suggest workout plans or fitness classes"
    ],
    "Social Stress": [
        "Engage in social ativitites. --> Suggest clubs or social events",
        "Engage in extracurricular activities to build connections.--> Provide information on campus organizations",
        " --> Anti-bullying workshops or counseling services"
        #add something about bullying
    ],
    "Pyschological Stress": [
        "Practice cognitive-behavioral techniques to manage negative thoughts.--> Share CBT resources",
        "Engage in hobbies and activities that bring joy.--> Suggest hobby ideas or workshops",
        "Seek professional help if stress becomes overwhelming. --> Provide access to mental health professionals"
    ],
    "Environmental Stress": [
        "Create a comfortable and organized living space.--> Share organization tips",
        "Use noise-cancelling headphones or earplugs to reduce distractions.--> Recommend products",
        "Spend time in nature to rejuvenate. --> Suggest local parks or outdoor activities"
    ],
    "Other": [
        "Identify specific stressors and address them directly.",
        "Incorporate regular physical activity into your routine.",
        "Practice relaxation techniques such as meditation or yoga."
    ]
}

st.subheader("Recommendations Based on Stress Type")
selected_stress_type = st.selectbox("Select Stress Type:", recommendations_dict.keys())

st.write("### Recommendations for " + selected_stress_type)
if selected_stress_type in recommendations_dict:
    for rec in recommendations_dict[selected_stress_type]:
        st.write("- " + rec)

st.success("You can combine multiple recommendations for better intervation strategies!", icon="✅")