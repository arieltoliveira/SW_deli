import streamlit as st
import pandas as pd

date = st.date_input('Data')

df = pd.DataFrame({date})

st.write(df)