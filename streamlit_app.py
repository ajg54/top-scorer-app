import streamlit as st
import pandas as pd


choices = pd.read_csv("./data/choices.csv")
choices.set_index('person', drop=True, inplace=True)

st.title("England Test Top Scorer 2025")
st.write("An app to keep track of a Cricket Cwappers bet.")
st.write(choices)
