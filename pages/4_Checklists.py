import streamlit as st
import pandas as pd
from pathlib import Path
import os

#########
#notas para alteração nessa pagina
# 
#
#########
st.set_page_config(
    layout='wide',
    page_title='Checklists'
)
newcheklist_list = []
cliente = (st.session_state.cliente)
st.markdown(f'## {cliente}')

current_folder = Path(__file__).parent.parent
checklistsfolder = current_folder / 'Dados' / cliente / 'Checklists'

listachecklist = [ f.name for f in os.scandir(checklistsfolder) if f.is_file() ]
for item in range(len(listachecklist)):
    listachecklist[item] = listachecklist[item][:-4]

checklist = st.selectbox('Cheklist a ser aplicado', listachecklist)
checklist =checklist + '.csv'

df = pd.read_csv(checklistsfolder / checklist, parse_dates=True) 

@st.dialog("Aplicar novo checklist")
def newcheklist(list):
    output_list = [None]
    for item in list:
        output_list.append(None)
    date = st.date_input('Data')
    output_list[0] = str(date)
    for items in range(len(list)):
        options = ["C", "N/C", "P/C", "NA"]
        selection = st.pills(list[items], options, selection_mode="single", key = items)
        output_list[items+1] = selection
        st.markdown(f"---------------------")
    if st.button("Submit"):
        st.session_state.newcheklist = output_list
        st.rerun()


newcheklist_list = []
collist = list(df.columns.values)
collist.remove('Data')

if "newcheklist" not in st.session_state:
    if st.button("Adicionar nova visita"):
        newcheklist(collist)
else:
    if st.button("Adicionar nova visita"):
        newcheklist(collist)
    newcheklist_list = st.session_state.newcheklist

#st.write(date_conv(newcheklist_list[0]))
if newcheklist_list != []:
    if newcheklist_list[0] not in list(df['Data'].value_counts().index):
        st.success('Novo checklist aplicado')
        df.loc[len(df)] = newcheklist_list #len mostra o numero de linhas então o valor esta sendo adicionado na ultima linha, a lista tem que conter todas as colunas
        df.to_csv(checklistsfolder / checklist, index=False)
    else:
        st.error(f'Checklist já existe')
newcheklist_list = []
if "newcheklist_list" in st.session_state:
    del st.session_state['newcheklist_list']
if "newcheklist" in st.session_state:
    del st.session_state['newcheklist']

st.write(df)