import streamlit as st
import pandas as pd
import datetime
from scripts.data_downloader import get_top_scorer_table

# load runs overview
reference_date = datetime.date.today()
if reference_date.year != st.session_state.base_year:
    reference_date = st.session_state.base_date
runs_by_player = get_top_scorer_table(datetime.date(reference_date.year,1,1), reference_date)
runs_by_player.replace(to_replace="-", value=0, inplace=True)
# TODO: investigate Arrow serialization log message on type conversions
runs_by_player['Runs'] = runs_by_player['Runs'].astype(int)
runs_by_player['Inns'] = runs_by_player['Inns'].astype(int)
runs_by_player['NO'] = runs_by_player['NO'].astype(int)
# load player county data
player_by_county = pd.read_csv("./data/county.csv")
# merge player county data with runs overview
raw_county_table = runs_by_player.join(player_by_county.set_index("Player"), how="left")
raw_county_table['County'] = raw_county_table['County'].fillna("Unassigned")
# aggregate runs by country
agg_settings = {'Runs': 'sum', 'Inns': 'sum', 'NO': 'sum', 'Player Count': 'count', 'Players': ';'.join}
raw_county_table.reset_index(names="Players", inplace=True)
raw_county_table['Player Count'] = raw_county_table['Players']
agg_county_table = raw_county_table.groupby("County").agg(agg_settings)
agg_county_table['Ave'] = agg_county_table['Runs'] / (agg_county_table['Inns']-agg_county_table['NO'])
# sort by runs total
agg_county_table.sort_values(by='Runs', inplace=True, ascending=False)
agg_county_table = agg_county_table[['Runs', 'Ave', 'Inns', 'NO', 'Player Count', 'Players']]
# add in Scotland
short_county_table = agg_county_table.copy()
short_county_table['Logo'] = ""
region_selection = {
    "Yorkshire": "https://img1.hscicdn.com/image/upload/f_auto/lsci/db/PICTURES/CMS/313200/313281.logo.png",
    "Surrey": "https://d2dzjyo4yc2sta.cloudfront.net/?url=images.pitchero.com%2Fclub_logos%2F13643%2FpX7KF1tRo6HgpepV0Evn_Logo.png&bg=fff&w=1200&h=630&t=frame",
    "Scotland": "https://www.sportsyaari.com/images/team/logo/scotland-team-logo.png"}
for region in region_selection.keys():
    if region not in short_county_table.index:
        short_county_table.loc[region] = [0, None, 0, 0, 0, "", ""]
    short_county_table.loc[region, 'Logo'] = region_selection[region]
short_county_table = short_county_table.loc[region_selection.keys()]
short_county_table.reset_index(inplace=True)
short_county_table = short_county_table[['Logo', 'County', 'Runs']]
short_county_table.rename(columns={"County": "'County'"}, inplace=True)

st.title("Constructors' Championship")
st.header("Overview")
st.data_editor(short_county_table, column_config={"Logo": st.column_config.ImageColumn()}, hide_index=True)
st.header("By County")
st.write(agg_county_table)
