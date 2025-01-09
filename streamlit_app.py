import streamlit as st
import pandas as pd
import numpy as np

# parameters
cricinfo_url = "https://www.espncricinfo.com"
profile_path = cricinfo_url + "/cricketers/"
total_tests = 10
sample_size = 1000000
# load data
choices = pd.read_csv("./data/choices.csv")
choices.set_index('person', drop=True, inplace=True)
choices['cricinfo_path'] = profile_path + choices['cricinfo_path']
starting_stats = pd.read_csv("./data/starting_player_stats.csv")
starting_stats.set_index('player', drop=True, inplace=True)
# initial calculations
starting_stats['runs_per_match'] = starting_stats['runs'] / starting_stats['matches']
starting_stats['initial_expected_runs'] = starting_stats['runs_per_match'] * total_tests
random_samples = pd.DataFrame()
for player in starting_stats.index:
    inverse_mean = 1 / (1+starting_stats.loc[player, 'runs_per_match'])
    random_samples[player] = np.random.negative_binomial(n=total_tests, p=inverse_mean, size=sample_size)
random_samples['winner'] = random_samples.idxmax(axis=1)
winners = random_samples.groupby('winner').size()/sample_size
winners.name = "Win Prob."
starting_stats = starting_stats.join(other=winners)

# layout
st.set_page_config(page_title="Top Scorer")
st.title("England Test Top Scorer 2025")
st.write("An app to keep track of a Cricket Cwappers bet.")
st.data_editor(
    choices,
    column_config={'cricinfo_path': st.column_config.LinkColumn()}
)
st.dataframe(starting_stats.style.format({'runs_per_match': "{:.2f}",
                                          'initial_expected_runs': "{:.0f}",
                                          'Win Prob.': "{:.2%}"}))
