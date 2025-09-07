import streamlit as st
import os

pages_dir = "subpages"
pg = st.navigation([st.Page(os.path.join(pages_dir, "main.py"), title="Homepage"),
                    st.Page(os.path.join(pages_dir, "history.py"), title="History")])
pg.run()
