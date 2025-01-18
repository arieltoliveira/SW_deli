import streamlit as st
import pandas as pd
from pathlib import Path

#########
#notas para alteração nessa pagina
# 
#
#########
st.set_page_config(
    layout='wide',
    page_title='Visitas'
)

cliente = (st.session_state.cliente)
st.markdown(f'## {cliente}')

current_folder = Path(__file__).parent.parent
visitacsv = current_folder / 'Dados' / cliente / 'Visitas' / 'Visitas.csv'
df = pd.read_csv(visitacsv, parse_dates=True)  
 
sectorlist = ['COZINHA', 'ESTOQUE', 'SALÃO', 'ADEGA', 'SALA REFRIGERADA']

#POPUP PARA ADICONAR UMA NOVA DATA DE VISITA
newvisitlist = []

@st.dialog("Adicione uma nova visita")
def newvisit():
    date = st.date_input('data')
    sector = st.selectbox('Setor', sectorlist)
    comment = st.text_input("Comentarios")
    if st.button("Submit"):
        st.session_state.newvisit = [date, sector, 1 , comment]
        st.rerun()

if "newvisit" not in st.session_state:
    if st.button("Adicionar nova visita"):
        newvisit()
else:
    if st.button("Adicionar nova visita"):
        newvisit()
    newvisitlist = st.session_state.newvisit

if newvisitlist != []:
    if newvisitlist[0] not in list(df['data'].value_counts().index):
        st.success('Nova visita adicionada')
        df.loc[len(df)] = newvisitlist #len mostra o numero de linhas então o valor esta sendo adicionado na ultima linha, a lista tem que conter todas as colunas
        df.to_csv(visitacsv, index=False)
    else:
        st.error(f'Visita já existe')
newvisitlist = []
if "newvisit" in st.session_state:
    del st.session_state['newvisit']

data = list(df['data'].value_counts().index)
#data.sort()
visita = st.selectbox('Visita do dia', data)
df_filtered = df[df['data'] == visita]

#POPUP PARA ATUALIZAR VISITA
updatevisitlist = []
@st.dialog("Atualizar visita")
def updatevisit():
    sector = st.selectbox('Setor', sectorlist)
    comment = st.text_input("Comentarios")
    if st.button("Submit"):
        st.session_state.updatevisit = ['x', sector, 'x', comment]
        st.rerun()

if "updatevisit" not in st.session_state:
    if st.button("Atualizar visita"):
        updatevisit()
else:
    if st.button("Atualizar visita"):
        updatevisit()
    updatevisitlist = st.session_state.updatevisit

if updatevisitlist != []:
    x=0
    for item in range(len(df_filtered)):
        if df_filtered['setor'].values[item] == updatevisitlist[1]:
            x = x+1
    st.write(df_filtered)
    updatevisitlist[2] = x +1
    updatevisitlist[0] = visita
    df.loc[len(df)] = updatevisitlist #len mostra o numero de linhas então o valor esta sendo adicionado na ultima linha, a lista tem que conter todas as colunas
    df.to_csv(visitacsv, index=False)
updatevisitlist = []
if "updatevisit" in st.session_state:
    del st.session_state['updatevisit']

finlist = list(df_filtered['setor'].value_counts().index)
visitlist = []

for sector in range(len(finlist)):
    visitlist.append(finlist[sector])
    for items in range(len(df_filtered)):
        if df_filtered['setor'].values[items] == finlist[sector]:
            visitlist.append(df_filtered['comentario'].values[items])

    
finaldf = pd.DataFrame({f'visita do dia {visita}': visitlist})

#FUNCAO PARA FORMATACAO CONDICIONAL DA TABELA WORKBOOK, COLORINDO DE VERMELHO A VERDE
def condformat (row):
    value = row.loc[f'visita do dia {visita}']
    if value in sectorlist:
        color = 'lightgrey'
    else:
        color = ''
    return ['background-color: %s' % color for r in row]
st.dataframe(finaldf.style.apply(condformat, axis=1), width=None, hide_index=True)



x = '''
df = pd.read_csv('scada_pm_beta.csv', parse_dates=True)               #sheet name é a aba do excel, usecol seleciona a coluna, csv não tem abas, então não é possivel adicionar o sheet 
df_info = pd.read_csv('scada_info.csv')
df_ca = pd.read_csv('scada_ca_beta.csv', parse_dates=True)

#FILTROS DO PROJETO
projects = df['Project'].value_counts().index
project = st.sidebar.selectbox('Project', projects)
df_filtered = df[df['Project'] == project]



#EDITANDO CAIXAS DE TEXTO EM COLUNAS
def edit_text1(name, column_header):
    txt = (col1.text_input(name, f'{df_filtered[column_header].values[0]}'))
    row_index = df.index.get_loc(df[df['Project'] == df_filtered['Project'].values[0]].index[0])
    df.at[row_index, column_header] = txt
    return()


#EDITANDO AS DATAS
def edit_date1(label, start_date):
    def date_conv (data):           #converte as datas de str para datetime
        return datetime.datetime.strptime(data, '%Y-%d-%m')
    date = col4.date_input(label, date_conv(f'{df_filtered[start_date].values[0]}'), format="MM.DD.YYYY")
    row_index = df.index.get_loc(df[df['Project'] == df_filtered['Project'].values[0]].index[0])
    df.at[row_index, start_date] = date
    return()

col1, col2, col3 = st.columns(3)



#SELECT BOX LOGIC FOR UPDATE SHOWING IN 3 COLUNMS
def selbox1 (df_info_col, df_stat_col, label):
    df_info_list = list(df_info[df_info_col].value_counts().index)
    df_info_list.sort()
    test = df_info_list.index(df_filtered[df_stat_col].values[0])
    text_end = col4.selectbox(label, df_info_list, index=test)
    row_index = df.index.get_loc(df[df['Project'] == df_filtered['Project'].values[0]].index[0])
    df.at[row_index, df_stat_col] = text_end
    return()



#FILTRO PARA EXIBIÇÃO DOS TEXTOS
edit_text1('Customer','Customer')


#Adicioando select box em 3 colunas
col4, col5, col6 = st.columns(3)
selbox1('PM', 'PM', 'PM')


#def date_conv (data):           #converte as datas de str para datetime
#    return datetime.datetime.strptime(data, '%Y-%d-%m')
startdate = datetime.datetime.strptime((df_filtered['Project start'].values[0]), '%Y-%m-%d')
date = col4.date_input('Project start date', startdate, format="MM.DD.YYYY")
row_index = df.index.get_loc(df[df['Project'] == df_filtered['Project'].values[0]].index[0])
df.at[row_index,'Project start'] = date

#botao para atualizar o schedule no scada_ca
df_temp = []
df_list_temp = []

    df_ca.to_csv('scada_ca_beta.csv', index=False)

df.to_csv('scada_pm_beta.csv', index=False)
'''
