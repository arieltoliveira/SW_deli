import streamlit as st
from pathlib import Path
import shutil
import os

#########
##notas para alteração nessa pagina
#   
#   
#
#########

#SELECIONANDO A PASTA PARA COPIAR O TEMPLATE


st.set_page_config(
    layout='wide',
    page_title='New project'
)

novo_cliente = st.text_input('Nome do novo Cliente')
current_folder = Path(__file__).parent.parent

subfolderslist = [ f.name for f in os.scandir(current_folder / 'Dados') if f.is_dir() ]


if st.button('Adicionar Cliente'):
    if novo_cliente not in subfolderslist:
        st.success(f'Cliente {novo_cliente} adiconado ao banco de dados')
        shutil.copytree(current_folder / 'Dados' / 'Template', current_folder / 'Dados' / novo_cliente)
    else:
        st.error(f'Cliente {novo_cliente} já existe')
