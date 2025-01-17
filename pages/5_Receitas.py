import streamlit as st
import pandas as pd
from pathlib import Path
import datetime
import plotly.figure_factory as ff
#########
#notas para alteração nessa pagina
# 
#
#########
st.set_page_config(
    layout='wide',
    page_title='Receitas'
)

cliente = (st.session_state.cliente)
st.markdown(f'## {cliente}')
