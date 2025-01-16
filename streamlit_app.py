import streamlit as st
import pandas as pd
import numpy as np
import requests
import os

# parameters
agent = {"User-Agent": "Mozilla/5.0"}
cricinfo_url = "https://www.espncricinfo.com"
profile_path = cricinfo_url + "/cricketers/"
stats_url_prefix = "https://stats.espncricinfo.com/ci/engine/player/"
recent_matches_suffix = ".html?class=1;filter=advanced;orderby=start;orderbyad=reverse;template=results;type=batting;view=match"
total_tests = 10
sample_size = 1000000
# load local data
choices = pd.read_csv("./data/choices.csv")
choices.set_index('person', drop=True, inplace=True)
choices['player_id'] = choices['cricinfo_path'].str.split("-").str[-1]
choices['cricinfo_path'] = profile_path + choices['cricinfo_path']
starting_stats = pd.read_csv("./data/starting_player_stats.csv")
starting_stats.set_index('player', drop=True, inplace=True)
historical_top_scorers = {}
for file_name in os.listdir("./data/historical"):
    temp_year = file_name[12:-4]
    historical_top_scorers[temp_year] = pd.read_csv(os.path.join("./data/historical", file_name))
# load remote data, we use session state to avoid reloading this from source each time
player_history = {}
for player_name in choices['player']:
    if player_name not in st.session_state:
        player_id = choices[choices['player'] == player_name]['player_id'].iloc[0]
        url = stats_url_prefix + str(player_id) + recent_matches_suffix
        player_history[player_name] = past_matches = pd.read_html(requests.get(url, headers=agent).text)[3]
        st.session_state[player_name] = player_history[player_name]
    else:
        player_history[player_name] = st.session_state[player_name]
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
starting_stats['form'] = starting_stats.apply(lambda row: player_history[row.name]['Runs'].iloc[:10].sum(), axis=1)
random_samples = pd.DataFrame()
for player in starting_stats.index:
    inverse_mean = 1 / (1+starting_stats.loc[player, 'form']/10)
    random_samples[player] = np.random.negative_binomial(n=total_tests, p=inverse_mean, size=sample_size)
random_samples['winner'] = random_samples.idxmax(axis=1)
winners = random_samples.groupby('winner').size()/sample_size
winners.name = "Form Prob."
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
                                          'Win Prob.': "{:.2%}",
                                          'Form Prob.': "{:.2%}"}))
st.write("Recent form:")
player_tabs = st.tabs(list(starting_stats.index))
for player_tab, player_name in zip(player_tabs, list(starting_stats.index)):
    with player_tab:
        player_id = choices[choices['player']==player_name]['player_id'].iloc[0]
        url = stats_url_prefix + str(player_id) + recent_matches_suffix
        st.write(url)
        past_matches = player_history[player_name]
        st.dataframe(past_matches[['Runs', 'Opposition', 'Ground', 'Start Date']], hide_index=True)
selected_historical_year = st.selectbox(
    "Historical England top scorers:",
    list(historical_top_scorers.keys())[::-1],
    index=None,
    placeholder="Select year."
)
if selected_historical_year is not None:
    st.write(historical_top_scorers[selected_historical_year])
