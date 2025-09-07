import streamlit as st

st.title("Runners and Riders")
st.header("Runners")
runners_list = ["Root", "Brook", "Pope", "Crawley", "Smith", "Duckett", "Stokes", "Bethell"]
tab_root, tab_brook, tab_pope, tab_crawley, tab_smith, tab_duckett, tab_stokes, tab_bethell = st.tabs(runners_list)
with tab_root:
    st.header("Joe Root")
    st.write("Selected first by Paul.")
    st.write("In 2024, Joe Root became England's all time leading Test run-scorer."
             " Since 2014, he has been England's leading calendar year run-scorer every year "
             "with the exception of the COVID interrupted 2020 where Stokes took the honours."
             " With his batting powers showing no signs of waning, he is surely the pre-contest favourite.")
with tab_brook:
    st.header("Harry Brook")
    st.write("Selected second by Duncan.")
    st.write("Having debuted for England in 2022, "
             "Brook has had one of the most remarkable starts to a Test career in history."
             " With an average even higher than Root's (and with a runs per game stat to match), "
             "he was the only player that could realistically stake a claim to challenge Root's status as favourite.")
with tab_pope:
    st.header("Ollie Pope")
    st.write("Selected third by Matt.")
    st.write("At the start of 2025, "
             "there was talk of England's vice-captain's place in the starting line-up being under threat."
             " Despite a strong showing deputising with the gloves in New Zealand, "
             "Bethell's performance in Pope's usual slot at number three gave England a dilemma on Smith's return."
             "However, Bethell's absence for the first Test of the year (due to IPL commitments) "
             "gave Pope at least one more opportunity.")
with tab_crawley:
    st.header("Zak Crawley")
    st.write("Selected fourth by Alexis.")
    st.write("Despite a regular place in the Test side, "
             "Crawley's numbers as a top order batter are remarkable for all the wrong reasons."
             " By the end of 2024, "
             "he was on track to be the least productive opener / top three batter in Test history "
             "given his number of caps."
             " Will 2025 be his year?")
with tab_smith:
    st.header("Jamie Smith")
    st.write("Selected fifth by Matt Senior.")
    st.write("Smith has made an exceptional start to his Test career "
             "after England resolved the Foakes/Bairstow dilemma by answering 'neither'."
             " Will he be able to maintain his form "
             "and is he batting too low in the order to top the run scoring charts?")
with tab_duckett:
    st.header("Ben Duckett")
    st.write("Not selected.")
    st.write("A controversial non-selection given his remarkable second coming as an opener for England.")
with tab_stokes:
    st.header("Ben Stokes")
    st.write("Not selected.")
    st.write("Despite being the only player to knock Root off his calendar year top scorer perch in the last ten years,"
             " Stokes productivity with the bat has been rather limited since taking over the captaincy.")
with tab_bethell:
    st.header("Jacob Bethell")
    st.write("Not selected.")
    st.write("After a surprise Test debut in New Zealand at the back-end of 2024, "
             "there was genuine debate in the media about who to drop to accommodate him in England's top seven."
             " However, with IPL commitments making him unavailable for the first Test of the year, "
             "it seemed likely that he'd have to wait for his chance.")

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
             " Perhaps his admission to the contest was facilitated by the 'cwappers' thinking, "
             "incorrectly, that Smith bats too low to score sufficient runs to be a threat.")
