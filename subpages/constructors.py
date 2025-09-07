import streamlit as st
import pandas as pd
import datetime
from scripts.data_downloader import get_top_scorer_table

# load runs overview
reference_date = datetime.date.today()
runs_by_player = get_top_scorer_table(datetime.date(reference_date.year,1,1), reference_date)
runs_by_player.replace(to_replace="-", value=0, inplace=True)
# TODO: investigate Arrow serialization log message on type conversions
runs_by_player['Runs'] = runs_by_player['Runs'].astype(int)
runs_by_player['Inns'] = runs_by_player['Inns'].astype(int)
# load player county data
player_by_county = pd.read_csv("./data/county.csv")
# merge player county data with runs overview
raw_county_table = runs_by_player.join(player_by_county.set_index("Player"), how="left")
raw_county_table['County'] = raw_county_table['County'].fillna("Unassigned")
# aggregate runs by country
agg_county_table = raw_county_table.groupby("County").agg({'Runs': 'sum', 'Inns': 'sum'})
# TODO: add in Scotland if missing
# sort by runs total
agg_county_table.sort_values(by='Runs', inplace=True, ascending=False) # TODO: include more stats

st.title("Constructors' Championship")
st.header("Overview")
st.write("To be added.")
st.header("By County")
st.write(agg_county_table)
