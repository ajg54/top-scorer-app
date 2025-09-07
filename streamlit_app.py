import streamlit as st
import os

pages_dir = "subpages"
pg = st.navigation(
    [st.Page(os.path.join(pages_dir, "main.py"), title="Homepage", icon=":material/house:"),
     st.Page(os.path.join(pages_dir, "history.py"), title="History", icon=":material/history:")])
st.set_page_config(page_icon=":material/sports_cricket:", page_title="Top Scorer", layout="wide")
pg.run()
