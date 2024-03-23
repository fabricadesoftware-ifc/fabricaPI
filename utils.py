import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def init_session_state():
    if "data_frames_students" not in st.session_state:
        st.session_state.data_frames_students = []
    if "data_frames_cycles" not in st.session_state:
        st.session_state.data_frames_cycles = []
    if not st.session_state.get('uploaded_files_students'):
        st.session_state.uploaded_files_students = []
    if not st.session_state.get('uploaded_files_cycles'):
        st.session_state.uploaded_files_cycles = []

def create_df_students():
    df = pd.concat(st.session_state.data_frames_students, ignore_index=True)
    df['CO_CICLO_MATRICULA'] = df['CO_CICLO_MATRICULA'].astype(str)
    return df

def create_df_cycles():
    df = pd.concat(st.session_state.data_frames_cycles, ignore_index=True)
    return df

def create_graph(df, y, x):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(df[y], df[x])
    ax.set_title('')
    ax.set_xlabel('Quantidade de alunos')
    ax.set_ylabel('')

    for i,v in enumerate(df[x]):
        ax.text(v + 1, i, str(v), color="black", fontsize=8, ha="left", va="center")

    ax.yaxis.set_tick_params(labelsize=12)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)

def create_df_status(ciclo, df_students):
    new_df = []

    st.write(ciclo)

    if ciclo != 0:
        filter = f'CÓDIGO CICLO DE MATRÍCULA == {ciclo}'
    else:
        filter = 'CÓDIGO CICLO DE MATRÍCULA != "teste"'

    labels_status = df_students.query(f'{filter}')["NO_STATUS_MATRICULA"].unique()
    
    for i in labels_status:
        count = df_students.query(f'{filter} & NO_STATUS_MATRICULA == "{i}"')["NO_STATUS_MATRICULA"].count()
        new_df.append({'Status da Matricula': i, 'Total': count})

    # retorna o dataframe e as labels de x e y
    return [pd.DataFrame(new_df), 'Total', 'Status da Matricula']

def create_df_merged(temporary_df, df_students):
    temporary_df['CÓDIGO CICLO DE MATRÍCULA'] = temporary_df['CÓDIGO CICLO DE MATRÍCULA'].astype(str)
    
    df_merged = pd.merge(temporary_df, df_students, left_on='CÓDIGO CICLO DE MATRÍCULA', right_on='CO_CICLO_MATRICULA', how='inner')

    return df_merged

def read_files(files):
    if not files:
        return []
    data_frames = []
    for file in files:
        try:
            data_frames.append(pd.read_csv(file, encoding='latin-1', sep=';'))
        except Exception as e:
            LOGGER.error(f"Error reading file {file.name}: {e}")
    return data_frames
 
def clean_df(df):
    if df.shape[0] > 1:
        # Removes column if it has only null values or more than 50% null values
        for column in df.columns:
            if len(df[column].unique()) == 1 or df[column].isnull().sum() > len(df) * 0.5:
                df = df.drop(column, axis=1)

        # Removes rows if it has more than 50% null values
        df = df.dropna(thresh=len(df.columns) * 0.5)

    return df

def get_subindicators(df):
    col2, col3, col4, col5, col6 = st.columns(5)

    with col2:
        number_of_ongoing = df.query('NO_STATUS_MATRICULA == "EM_CURSO"').shape[0]
        st.write(f" ### {number_of_ongoing}")
        st.caption("Total em curso")
    
    with col3:
        number_of_concluded = df.query('NO_STATUS_MATRICULA == "CONCLUÍDA"').shape[0]
        st.write(f" ### {number_of_concluded}")
        st.caption("Total de concluentes")
    
    with col4:
        number_of_transfer = df.query('NO_STATUS_MATRICULA == "TRANSF_EXT"').shape[0]
        st.write(f" ### {number_of_transfer}")
        st.caption("Total de transferidos")
    
    with col5:
        number_of_dropout = df.query('NO_STATUS_MATRICULA == "ABANDONO"').shape[0]
        st.write(f" ### {number_of_dropout}")
        st.caption("Total de desistentes")

    with col6:
        number_of_disconnected = df.query('NO_STATUS_MATRICULA == "DESLIGADO"').shape[0]
        st.write(f" ### {number_of_disconnected}")
        st.caption("Total de desligados")

    return number_of_ongoing, number_of_concluded, number_of_dropout, number_of_transfer, number_of_disconnected

def get_indicators(df):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        number_of_students = df.shape[0]
        st.write(f"## {number_of_students}")
        st.caption("Total de Alunos")

    with col2:
        df_status = get_table_status(df)
        number_of_critical_cycles =  df_status.query('EM_CURSO < 2').shape[0]
        st.write(f" ## {number_of_critical_cycles}")
        st.caption("Total de Ciclos Críticos")
        
    with col3:
        number_of_cycles = df["CICLO DE MATRÍCULA"].nunique()
        st.write(f"## {number_of_cycles}", color="primary")
        st.caption("Total de Ciclos")

    with col4:
        number_of_curses = df["NOME DO CURSO"].nunique()
        st.write(f"## {number_of_curses}")
        st.caption("Total de Cursos")

    with col5:
        number_of_municipalities = df["MUNICIPIO"].nunique()
        st.write(f"## {number_of_municipalities}")
        st.caption("Total de Municípios")

    return number_of_students, number_of_cycles, number_of_curses, number_of_municipalities, number_of_critical_cycles


def get_table_status(df):
    new_df = []

    for i in df["CICLO DE MATRÍCULA"].unique():
        new_df.append({
            'NOME DO CICLO': i, 
            'ABANDONO': df.query(f'`CICLO DE MATRÍCULA` == "{i}" and NO_STATUS_MATRICULA == "ABANDONO"').shape[0], 
            'TRANSF_EXT': df.query(f'`CICLO DE MATRÍCULA` == "{i}" and NO_STATUS_MATRICULA == "TRANSF_EXT"').shape[0],
            'CONCLUÍDA': df.query(f'`CICLO DE MATRÍCULA` == "{i}" and NO_STATUS_MATRICULA == "CONCLUÍDA"').shape[0], 
            'DESLIGADO': df.query(f'`CICLO DE MATRÍCULA` == "{i}" and NO_STATUS_MATRICULA == "DESLIGADO"').shape[0],
            'EM_CURSO': df.query(f'`CICLO DE MATRÍCULA` == "{i}" and NO_STATUS_MATRICULA == "EM_CURSO"').shape[0],
            'TOTAL': df.query(f'`CICLO DE MATRÍCULA` == "{i}"').shape[0]
        })
    
    new_df = pd.DataFrame(new_df)
    
    return new_df

def get_filters(df):
    col2, col3, col4, col5 = st.columns(4)
    
    with col2:
        cycle_options = df["CICLO DE MATRÍCULA"].unique()
        cycle_options = ['TODOS'] + cycle_options.tolist()
        cycle = st.selectbox('Ciclo de Matrícula', cycle_options)
        
        if cycle == 'TODOS':
            filter_cycle = '`CICLO DE MATRÍCULA` != "NT"'
        else:
            filter_cycle = f'`CICLO DE MATRÍCULA` == "{cycle}"'

    with col3:
        curse_options = df["NOME DO CURSO"].unique()
        curse_options = ['TODOS'] + curse_options.tolist()
        curse = st.selectbox('Curso', curse_options)

        if curse == 'TODOS':
            filter_curse = '`CICLO DE MATRÍCULA` != "NT"'
        else:
            filter_curse = f'`NOME DO CURSO` == "{curse}"'

    with col4:
        status_options = df["NO_STATUS_MATRICULA"].unique()
        status_options = ['TODOS'] + status_options.tolist()
        status = st.selectbox('Status da Matrícula', status_options)

        if status == 'TODOS':
            filter_status = '`CICLO DE MATRÍCULA` != "NT"'
        else:
            filter_status = f'`NO_STATUS_MATRICULA` == "{status}"'

    with col5:
        municipality_options = df["MUNICIPIO"].unique()
        municipality_options = ['TODOS'] + municipality_options.tolist()
        municipality = st.selectbox('Município', municipality_options)

        if municipality == 'TODOS':
            filter_municipality = '`CICLO DE MATRÍCULA` != "NT"'
        else:
            filter_municipality = f'`MUNICIPIO` == "{municipality}"'

    df_with_filters = df.query(f'{filter_cycle} and {filter_curse} and {filter_status} and {filter_municipality}')
    st.write(df_with_filters)

def get_critical_cycles(df, df_status):
    for i in df["CICLO DE MATRÍCULA"].unique():
        if df_status.query(f'`NOME DO CICLO` == "{i}" and EM_CURSO < 2').shape[0] > 0:
            st.write(f"#### Ciclo: {i.lower()}")
            isShow = st.toggle('Mostrar somente os alunos em curso', True)
            if isShow:
                st.write(clean_df(df.query(f'`CICLO DE MATRÍCULA` == "{i}" and NO_STATUS_MATRICULA == "EM_CURSO"')))
            else:
                st.write(clean_df(df.query(f'`CICLO DE MATRÍCULA` == "{i}"')))

def get_tables(df):
    tab1, tab2, tab3 = st.tabs(["SITUAÇÃO DA MATRÍCULA POR CURSO", "TODOS OS DADOS COLETADOS", "CICLOS CRÍTICOS"])

    with tab1:
        st.write(get_table_status(df))
        st.write("### Gráfico de Status da Matrícula por Ciclo")
        generate_chart(st.session_state.master_data_frame)
        
    with tab2:
        get_filters(df)
    
    with tab3:
        get_critical_cycles(df, get_table_status(df))

def create_df_students_for_chart(df, ciclo, curse):
    if ciclo in df['CICLO DE MATRÍCULA'].unique() and curse in df[df['CICLO DE MATRÍCULA'] == ciclo]['NOME DO CURSO'].unique():
        # Filtra os dados com base nos valores selecionados
        df_filtered = df[(df['CICLO DE MATRÍCULA'] == ciclo) & (df['NOME DO CURSO'] == curse)]
        
        # Conta os alunos por status de matrícula
        status_counts = df_filtered['NO_STATUS_MATRICULA'].value_counts().reset_index()
        
        # Renomeia as colunas
        status_counts.columns = ['Status da Matrícula', 'Total']
        return status_counts
    else:
        return pd.DataFrame({'Status da Matrícula': [], 'Total': []})

def generate_chart(df):
    col1, col2 = st.columns(2)

    with col1:
        cycle = st.selectbox('Ciclo de Matrícula', df['CICLO DE MATRÍCULA'].unique())
    with col2:
        curse_options = df[df['CICLO DE MATRÍCULA'] == cycle]['NOME DO CURSO'].unique()
        curse = st.selectbox('Nome do Curso', curse_options)

    df_filtro_NO_STATUS_MATRICULA = create_df_students_for_chart(df, cycle, curse)
    st.bar_chart(data=df_filtro_NO_STATUS_MATRICULA, y='Total', x='Status da Matrícula')   
