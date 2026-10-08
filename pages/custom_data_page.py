import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Mentaal gezondheidsrisico Voorspellingen",
    layout="centered"
)

@st.cache_resource
def load_model():
    return joblib.load("model_pipeline.joblib")

model_pipeline = load_model()

st.title("Mentaal gezondheidsrisico Voorspellingen")
st.markdown("Vul hier de data in voor een voorspelling, of upload een CSV.")

st.subheader("Upload CSV")
uploaded_data = st.file_uploader("Selecteer data bestand.", type=["csv"])

if uploaded_data is not None:
    input_data = pd.read_csv(uploaded_data)

    if st.button("Voer voorspellingen uit op data."):
        try:
            predictions = model_pipeline.predict(input_data)

            result_df = input_data.copy()
            result_df["predicted_mental_health_risk"] = predictions

            st.success("Predictions completed successfully!")

            df_columns = result_df.columns.tolist()
            df_columns = df_columns[-1:] + df_columns[:-1]

            result_df = result_df[df_columns]
            st.dataframe(result_df, hide_index=True)

            csv_data = result_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Predictions as CSV",
                data=csv_data,
                file_name="mental_health_predictions.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"Er is iets fout gegaan tijdens het voorspellen: {e}")

st.subheader("Voer handmatig in")

with st.form("prediction_form"):
    st.subheader("Subject details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Leeftijd", min_value=18, max_value=100, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
        employment_status = st.selectbox("Werk Status", ["Employed", "Student", "Self-employed", "Unemployed"])
        work_environment = st.selectbox("Werk Omgeving", ["On-site", "Remote", "Hybrid"])
        mental_health_history = st.selectbox("Geschiedenis met mentale gezondheid", ["Yes", "No"])
        seeks_treatment = st.selectbox("Zoekt Hulp", ["Yes", "No"])

    with col2:
        stress_level = st.slider("Stress Level (1-10)", step=0.5, min_value=1.0, max_value=10.0, value=5.0)
        sleep_hours = st.slider("Slaap Uren", step=0.5, min_value=1.0, max_value=12.0, value=7.0)
        physical_activity_days = st.slider("Actieve Dagen Per Week", step=1, min_value=0, max_value=7, value=3)
        social_support_score = st.slider("Social Support Score", step=1, min_value=0, max_value=100, value=50)
        productivity_score = st.text_input("Productiviteit Score", value="75.0")

    submitted = st.form_submit_button("Voorspel risico")

if submitted:
    input_data = pd.DataFrame({
        "age": [age],
        "gender": [gender],
        "employment_status": [employment_status],
        "work_environment": [work_environment],
        "mental_health_history": [mental_health_history],
        "seeks_treatment": [seeks_treatment],
        "stress_level": [stress_level],
        "sleep_hours": [sleep_hours],
        "physical_activity_days": [physical_activity_days],
        "social_support_score": [social_support_score],
        "productivity_score": [productivity_score]
    })

    try:
        prediction = model_pipeline.predict(input_data)
        st.success(f"### Voorspeld Risico: **{prediction[0]}**")
    except Exception as e:
        st.error(f"Er ging iets fout tijdens het voorspellen: {e}")
