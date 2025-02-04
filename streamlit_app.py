import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from io import StringIO
import datetime
from scripts.data_downloader import get_top_scorer_table

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
    temp_year = int(file_name[12:-4])
    historical_top_scorers[temp_year] = pd.read_csv(os.path.join("./data/historical", file_name))
# load remote data, we use session state to avoid reloading this from source each time
player_history = {}
for player_name in choices['player']:
    if player_name not in st.session_state:
        player_id = choices[choices['player'] == player_name]['player_id'].iloc[0]
        url = stats_url_prefix + str(player_id) + recent_matches_suffix
        player_history[player_name] = past_matches = pd.read_html(StringIO(requests.get(url, headers=agent).text))[3]
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
current_date = datetime.date.today()
start_date = datetime.date(2025, 1,1)
end_date = min(current_date, datetime.date(2025,12,31))
current_scores = get_top_scorer_table(start_date, end_date)
if not current_scores.empty:
    choices = choices.join(current_scores[['Runs']], on='player', how='left')
    choices.rename(columns={'Runs': 'runs'}, inplace=True)
    choices.sort_values(by='runs', inplace=True, ascending=False)
    choices['ranking'] = choices.reset_index().index + 1
    choices = choices[['player', 'runs', 'ranking', 'selection_order', 'cricinfo_path', 'player_id']]
# layout
st.set_page_config(page_title="Top Scorer")
st.title("England Test Top Scorer 2025")
st.write("An app to keep track of a Cricket Cwappers bet.")
st.data_editor(
    choices,
    column_config={'cricinfo_path': st.column_config.LinkColumn()}
)
st.header("Current Performance")
reference_date = st.date_input("Select reference date "
                               "[gives run total for matches starting that year up to and including selected date]",
                               "today", max_value="today", format="DD/MM/YYYY")
current_table = get_top_scorer_table(datetime.date(reference_date.year,1,1), reference_date)
if current_table.empty:
    st.write("No data yet for selected time period")
else:
    st.write(current_table)
st.header("Initial Probabilities")
st.dataframe(starting_stats.style.format({'runs_per_match': "{:.2f}",
                                          'initial_expected_runs': "{:.0f}",
                                          'Win Prob.': "{:.2%}",
                                          'Form Prob.': "{:.2%}"}))
st.header("Recent form")
player_tabs = st.tabs(list(starting_stats.index))
for player_tab, player_name in zip(player_tabs, list(starting_stats.index)):
    with player_tab:
        player_id = choices[choices['player']==player_name]['player_id'].iloc[0]
        url = stats_url_prefix + str(player_id) + recent_matches_suffix
        st.write(url)
        past_matches = player_history[player_name]
        st.dataframe(past_matches[['Runs', 'Opposition', 'Ground', 'Start Date']], hide_index=True)
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
