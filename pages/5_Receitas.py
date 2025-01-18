import streamlit as st
from pathlib import Path

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

current_folder = Path(__file__).parent.parent


st.image(current_folder / 'WIP_1.jpeg')