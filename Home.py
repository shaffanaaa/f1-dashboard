#main page
import streamlit as st

st.set_page_config(
    page_title="F1 Dashboard Project",
    page_icon="🏎",
)

st.title("F1 Dashboard Project 🏎🏁  ")

st.sidebar.success("Select a page to see visualizations!")

st.markdown(
    """
    F1 is my favorite sport so I thought I would combine my 
    passion for this sport with my interests in data science 
   and analysis! I used the fastf1-api for the data and
    Im working on this passion project on the side so 
    some of the stuff does need work, any feedback is appreciated!


    Future Features: 
    - Prediction model to predict race wins and optimal pit windows
    - Driver point progression through different seasons
    - Detailed technical statistical analysis

    Note: Some of the data does take a while to load as 
    Im still figuring out how to streamline that process

    Forza Ferrari!
    

"""
)

