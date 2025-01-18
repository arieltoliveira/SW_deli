import streamlit as st
import pandas as pd
from pathlib import Path
import os


#########
##notas para alteração nessa pagina
#   
#   
#   
#########
st.set_page_config(
    layout='wide',
    page_title='Project Status'
)


current_folder = Path(__file__).parent
#FILTROS DO PROJETO
listaclientes = [ f.name for f in os.scandir(current_folder / 'Dados') if f.is_dir() ]
listaclientes.sort()
listaclientes.remove('Template')
cliente = st.selectbox('Cliente', listaclientes)

st.session_state['cliente'] = cliente


x = '''

df = pd.read_csv('scada_pm_beta.csv', parse_dates=True)               #sheet name é a aba do excel, usecol seleciona a coluna, csv não tem abas, então não é possivel adicionar o sheet 

#FILTROS DO PROJETO
projects = list(df['Project'].value_counts().index)
projects.sort()
project = st.sidebar.selectbox('Project', projects)
df_filtered = df[df['Project'] == project]

#INFORMAÇÕES SIDEBAR
projecttype = df_filtered['Project_type'].values[0]
with st.sidebar:
    col4, col5 = st.columns(2)
    st.markdown(f"**Customer:** {df_filtered['Customer'].values[0]}")
    col4.markdown(f"**Country:** {df_filtered['Country'].values[0]}")
    col5.markdown(f"**State:** {df_filtered['State'].values[0]}")
    col4.markdown(f"**Turbines:** {df_filtered['Turbines'].values[0]}")
    col5.markdown(f"**Year:** {df_filtered['Year'].values[0]}")
    st.markdown(f"**PM:** {df_filtered['PM'].values[0]}")
    if projecttype in ['New project', 'Repower']:
        st.markdown(f"**Contruction PM (PE):** {df_filtered['Contruction PM (PE)'].values[0]}")
        st.markdown(f"**TPM:** {df_filtered['TPM'].values[0]}")
    st.markdown(f"**Site Manager Lead:** {df_filtered['Site Manager Lead'].values[0]}")
    if projecttype in ['New project', 'Repower']:
        st.markdown(f"**Comissioning lead:** {df_filtered['Comissioning lead'].values[0]}")
    st.markdown(f"**SCADA Configurator:** {df_filtered['SCADA Configurator'].values[0]}")
    st.markdown(f"**Network configurator:** {df_filtered['Network configurator'].values[0]}")
    st.markdown(f"**PPC configurator:** {df_filtered['PPC configurator'].values[0]}")
    if projecttype in ['New project', 'Repower']:
        st.markdown(f"**Customer SCADA:** {df_filtered['Customer SCADA'].values[0]}")
        st.markdown(f"**Customer PM:** {df_filtered['Customer PM'].values[0]}")
    if projecttype in ['After market full SCADA', 'After market only server']:
        st.markdown(f"**SO#:** {df_filtered['SO number'].values[0]}")
        st.link_button(df_filtered['SF case'].values[0], df_filtered['SF link'].values[0])
with tab2:
    #FUNCAO PARA FORMATACAO CONDICIONAL DA TABELA WORKBOOK, COLORINDO DE VERMELHO A VERDE
    def condformat (row):
        value = row.loc["Status"]
        if value == 'IFC':
            color = 'lightgreen'
        elif value == '90%':
            color = 'lightyellow'
        elif value == '60%':
            color = 'yellow'
        elif value == '30%':
            color = 'red'
        else:
            color = 'red'
        return ['background-color: %s' % color for r in row]

    #INFORMAÇÕES DO WORKBOOK
    mainfolder = str(df_filtered['Project folder'].values[0])
    dirname = mainfolder + '/SCADA Work Book'
    col3, col4 = st.columns(2)
    with col3:
        #CAMPO DE INFORMACOES DO PROJETO
        txt_info = st.text_area(f'Project general info (tools, special requiremtns, etc.):', f'{df_filtered['Project info'].values[0]}',height=200)
        row_index = df.index.get_loc(df[df['Project'] == df_filtered['Project'].values[0]].index[0])
        df.at[row_index, 'Project info'] = txt_info
        #info workbook
        col1, col2 = st.columns(2)
        if Path(dirname).exists():

            subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
            wb_index = []
            wb_folder = []
            wb_status = []
            for folders in subfolders:
                final = folders.replace(dirname + '\\', '')
                if final[:2] not in ('00','99'):
                    if final[-4:-3] == '_':
                        wb_index.append(final[:2])
                        wb_folder.append(final[3:-4])
                        wb_status.append(final[-3:])
            n = (len(wb_index)//2)
            if len(wb_index)%2 > 0:
                n = n+1

            wb_workbook1 = {
                            'Folder' : wb_folder[0:n],
                            'Status' : wb_status[0:n]
                            }
            wb_workbook2 = {
                            'Folder' : wb_folder[n:len(wb_index)],
                            'Status' : wb_status[n:len(wb_index)]
                            }
            df_workbook1 = pd.DataFrame(wb_workbook1)
            df_workbook2 = pd.DataFrame(wb_workbook2)
            #df_workbook1.style.map(condformat, axis=1)
            col1.dataframe(df_workbook1.style.apply(condformat, axis=1), width=None, hide_index=True)
            col2.dataframe(df_workbook2.style.apply(condformat, axis=1),  width=None, hide_index=True)
        else:
            col1.write('Workbook not found for this projects in the path below:')
            col1.write(dirname)


    #CAMPO DE NOTAS
    today = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
    weeknum = today.isocalendar()[1]
    txt = col4.text_area(f'Project notes (current week W{weeknum}):', f'{df_filtered['Notes'].values[0]}',height=750)
    row_index = df.index.get_loc(df[df['Project'] == df_filtered['Project'].values[0]].index[0])
    df.at[row_index, 'Notes'] = txt



    df.to_csv('scada_pm_beta.csv', index=False)

    #GANT CHART FOR PROJECT SCHEDULE

    def date_gantt(data):           #converte as datas de str para datetime
        return datetime.datetime.strptime(data, '%Y-%m-%d') # '%Y-%m-%d'     %m/%d/%Y

    def week(data):                 #gera o numero da semana baseado na data
        week = date_gantt(data)
        return week.isocalendar()[1]

    def data_gantt(label, start_date, end_date, resource, project_type):
        first =dict(Task=f'{label} - W{week(df_filtered[start_date].values[0])}', Start= date_gantt(df_filtered[start_date].values[0]), 
        Finish= date_gantt(df_filtered[end_date].values[0]), Resource=resource)
        end = (date_gantt(df_filtered[start_date].values[0]), first, project_type)
        return(end)

df_sc = pd.read_csv(f'Schedule/{project}.csv')
tasklist = list(df_sc['Task'])
startlist = []
endlist = []
reslist = list(df_sc['Resource'])

'''