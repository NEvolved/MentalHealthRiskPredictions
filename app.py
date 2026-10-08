import streamlit as st

prediction_page = st.Page(
    page="pages/custom_data_page.py",
    title="Voorspellingen",
    icon="🔮",
    default=True
)

historical_page = st.Page(
    page="pages/historical_data_page.py",
    title="Historische Data",
    icon="📊"
)

pg = st.navigation([prediction_page, historical_page])

pg.run()