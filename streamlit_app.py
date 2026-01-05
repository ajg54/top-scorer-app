import streamlit as st
import datetime
import os

pages_dir = "subpages"
pg = st.navigation(
    [st.Page(os.path.join(pages_dir, "main.py"), title="Homepage", icon=":material/house:"),
     st.Page(os.path.join(pages_dir, "runners.py"), title="Runners and Riders", icon=":material/sports_score:"),
     st.Page(os.path.join(pages_dir, "constructors.py"), title="Constructors' Championship",
             icon=":material/sports_motorsports:"),
     st.Page(os.path.join(pages_dir, "history.py"), title="History", icon=":material/history:")])
st.set_page_config(page_icon=":material/sports_cricket:", page_title="Top Scorer", layout="wide")
st.session_state['base_year'] = 2025
temp_date = datetime.date.today()
if temp_date.year == st.session_state['base_year']:
    st.session_state['base_date'] = temp_date
else:
    st.session_state['base_date'] = datetime.date(st.session_state['base_year'], 12, 31)
pg.run()
