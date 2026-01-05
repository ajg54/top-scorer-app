import streamlit as st
import os
import pandas as pd

historical_top_scorers = {}
for file_name in os.listdir("./data/historical"):
    temp_year = int(file_name[12:-4])
    if temp_year < st.session_state.base_year:
        temp_top_scorers = pd.read_csv(os.path.join("./data/historical", file_name))
        temp_top_scorers.index = temp_top_scorers.index + 1
        temp_top_scorers.index.name = "Ranking"
        historical_top_scorers[temp_year] = temp_top_scorers

st.title("History")
st.header("Historical Results")
historical_years = list(historical_top_scorers.keys())
historical_years.sort(reverse=True)
selected_historical_year = st.selectbox(
    "Historical England top scorers:",
    historical_years,
    index=None,
    placeholder="Select year."
)
if selected_historical_year is not None:
    st.write(historical_top_scorers[selected_historical_year])