import streamlit as st

#########
#notas para alteração nessa pagina
# 
#
#########
st.set_page_config(
    layout='wide',
    page_title='Ficha Tecnica'
)

cliente = (st.session_state.cliente)
st.markdown(f'## {cliente}')
