import streamlit as st
import pandas as pd

# parameters
cricinfo_url = "https://www.espncricinfo.com"
profile_path = cricinfo_url + "/cricketers/"
# load data
choices = pd.read_csv("./data/choices.csv")
choices.set_index('person', drop=True, inplace=True)
choices['cricinfo_path'] = profile_path + choices['cricinfo_path']

# layout
st.title("England Test Top Scorer 2025")
st.write("An app to keep track of a Cricket Cwappers bet.")
st.data_editor(
    choices,
    column_config={'cricinfo_path': st.column_config.LinkColumn()}
)
