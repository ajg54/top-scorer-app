import streamlit as st
import pandas as pd

# parameters
cricinfo_url = "https://www.espncricinfo.com"
profile_path = cricinfo_url + "/cricketers/"
total_tests = 10
# load data
choices = pd.read_csv("./data/choices.csv")
choices.set_index('person', drop=True, inplace=True)
choices['cricinfo_path'] = profile_path + choices['cricinfo_path']
starting_stats = pd.read_csv("./data/starting_player_stats.csv")
starting_stats.set_index('player', drop=True, inplace=True)
starting_stats['runs_per_match'] = starting_stats['runs'] / starting_stats['matches']
starting_stats['initial_expected_runs'] = starting_stats['runs_per_match'] * total_tests

# layout
st.title("England Test Top Scorer 2025")
st.write("An app to keep track of a Cricket Cwappers bet.")
st.data_editor(
    choices,
    column_config={'cricinfo_path': st.column_config.LinkColumn()}
)
st.dataframe(starting_stats.style.format({'runs_per_match': "{:.2f}",
                                          'initial_expected_runs': "{:.0f}"}))
