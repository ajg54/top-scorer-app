import streamlit as st

st.title("Runners and Riders")
st.header("Runners")
st.write("To be implemented")
st.header("Riders")
tab_paul, tab_duncan, tab_matt, tab_alexis, tab_matt_snr = st.tabs(["Paul", "Duncan", "Matt", "Alexis", "Matt Snr."])

with tab_paul:
    st.header("Paul")
    st.write("Paul was quick out of the blocks taking less than a minute to make the 'obvious' choice of Root.")

with tab_duncan:
    st.header("Duncan")
    st.write("With Root already taken and the 'obvious' second choice being a Yorkshireman, "
             "Duncan also wasted no time in selecting Brook after Paul had already nabbed Root.")

with tab_matt:
    st.header("Matt")
    st.write("Having correctly predicting the score of a darts match at the start of 2025, "
             "Matt suggested having a friendly contest to predict the England Test top scorer for that year."
             " Charitably (or gormlessly) he allowed Paul and Duncan to pick before him "
             "and he couldn't resist his Surrey bias with his pick Pope "
             "despite the risk of being dropped for Bethell "
             "and with the natural 3rd choice of Duckett still being available.")

with tab_alexis:
    st.header("Alexis")
    st.write("Inspired by Matt's 'unorthodox' selection, Alexis went fully rogue in selecting Crawley.")

with tab_matt_snr:
    st.header("Matt Senior")
    st.write("A controversial late-joiner, Matt's Dad belatedly joined the contest also flying the Surrey flag."
             " Perhaps his admission was facilitated by the 'cwappers' thinking, "
             "incorrectly, that Smith bats too low to score sufficient runs.")
