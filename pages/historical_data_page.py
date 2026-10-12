import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Mentaal gezondheidsrisico voorspelling dashboard",
    layout="centered"
)

st.title('Mentaal gezondheidsrisico voorspelling dashboard')

@st.cache_data
def load_data():
    df = pd.read_csv("mental_health_dataset.csv")
    df["productivity_score"] = pd.to_numeric(df["productivity_score"], errors="coerce")
    return df

health_df = load_data()

st.sidebar.header("Filters")

gender_options = health_df["gender"].dropna().unique().tolist()
selected_genders = st.sidebar.multiselect("Selecteer Gender(s)", options=gender_options, default=gender_options)

emp_options = health_df["employment_status"].dropna().unique().tolist()
selected_emp = st.sidebar.multiselect("Selecteer Werk Status", options=emp_options, default=emp_options)

risk_options = health_df["mental_health_risk"].dropna().unique().tolist()
selected_risk = st.sidebar.multiselect("Selecteer Risico", options=risk_options, default=risk_options)

health_df = health_df[
    health_df["gender"].isin(selected_genders) &
    health_df["employment_status"].isin(selected_emp) &
    health_df["mental_health_risk"].isin(selected_risk)
]

st.title("Historische data")
st.markdown("Hieronder zie je een aantal grafieken die historische data tonen.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Aantal records", len(health_df))
with col2:
    avg_age = health_df["age"].mean()
    st.metric("Gemiddelde leeftijd", f"{avg_age:.1f} jaar" if not pd.isna(avg_age) else "N/A")

st.markdown("---")

st.subheader("Historische Data Visualisaties")

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

ax1 = axes[0, 0]
risk_counts = health_df['mental_health_risk'].value_counts()
if set(risk_counts.index).issubset({'Low', 'Medium', 'High'}):
    risk_order = [r for r in ['Low', 'Medium', 'High'] if r in risk_counts.index]
    risk_counts = risk_counts.reindex(risk_order)
risk_counts.plot(kind='bar', ax=ax1, color='skyblue')
ax1.set_title('Verdeling van gezondheidsrisico niveaus')
ax1.set_xlabel('Mentale gezondheidsrisico niveau')
ax1.set_ylabel('Aantal')
ax1.tick_params(axis='x', rotation=45)

ax2 = axes[0, 1]
gender_data = health_df['gender'].value_counts()
gender_data.plot(kind='bar', ax=ax2, color='salmon')
ax2.set_title('Verdeling van gender')
ax2.set_xlabel('Gender')
ax2.set_ylabel('Aantal')
ax2.tick_params(axis='x', rotation=45)

ax3 = axes[0, 2]
employment_status_data = health_df['employment_status'].value_counts()
employment_status_data.plot(kind='bar', ax=ax3, color='lightgreen')
ax3.set_title('Verdeling van werkstatus')
ax3.set_xlabel('Werkstatus')
ax3.set_ylabel('Aantal')
ax3.tick_params(axis='x', rotation=45)

ax4 = axes[1, 0]
work_environment_data = health_df['work_environment'].value_counts()
work_environment_data.plot(kind='bar', ax=ax4, color='orange')
ax4.set_title('Verdeling van werkomgeving')
ax4.set_xlabel('Werkomgeving')
ax4.set_ylabel('Aantal')
ax4.tick_params(axis='x', rotation=45)

ax5 = axes[1, 1]
history_mapped = health_df['mental_health_history'].map({'No': 'Nee', 'Yes': 'Ja'}).value_counts()
history_mapped.plot(kind='bar', ax=ax5, color='purple')
ax5.set_title('Verdeling van gezondheids geschiedenis')
ax5.set_xlabel('Heeft een geschiedenis')
ax5.set_ylabel('Aantal')
ax5.tick_params(axis='x', rotation=45)

ax6 = axes[1, 2]
treatment_mapped = health_df['seeks_treatment'].map({'No': 'Nee', 'Yes': 'Ja'}).value_counts()
treatment_mapped.plot(kind='bar', ax=ax6, color='teal')
ax6.set_title('Verdeling van hulp zoekende mensen')
ax6.set_xlabel('Zoekt hulp')
ax6.set_ylabel('Aantal')
ax6.tick_params(axis='x', rotation=45)

plt.tight_layout()

st.pyplot(fig)