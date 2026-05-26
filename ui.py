'''
Run with:
    python -m streamlit run ui.py
'''

import streamlit as st
import pandas as pd

st.title("EV BMS Data Analysis")

df = pd.read_csv("data/bms_data.csv")

#show battery data
st.header("Battery Data")
st.dataframe(df)