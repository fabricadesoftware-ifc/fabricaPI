import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

import options.filters as filters
import options.configs as configs

LOGGER = get_logger(__name__)

def runPage():
        st.markdown(
            """
            ## 📈 Projeto Campus PI  
            \\
            Projeto de pesquisa institucional do campus IFC Araquari com foco na visualização, análise e transparência de dados. Para utilziar basta fazer upload do arquivo .csv e começar a explorar os dados. Você pode filtrar, ordenar, visualizar e exportar os dados, além de gerar gráficos e relatórios.
            ##
            """
        )
            
        st.write(
            """
            **Um projeto desenvolvido por:**
            \
            """
        )
        col1, col2, col3 = st.columns(3, gap="large")

        with col1:
            st.image('./assets/img/logo-ifc.png', width=300)

        with col2:
            st.image('./assets/img/logo-fabrica.png')

def apply_filters(df, translate_label):
    filters = {
        'status': f"NO_STATUS_MATRICULA == '{translate_label.get(st.session_state.selected_filter_status, '')}'", 
        'year': f"CO_CICLO_MATRICULA != '{translate_label.get(st.session_state.selected_filter_year, '')}'", 
        'curse': f"NO_STATUS_MATRICULA != '{translate_label.get(st.session_state.selected_filter_curse, '')}'"
    }

    query = ' and '.join(f'({condition})' for condition in filters.values())

    if query:
        df = df.query(query)

    return df

def runGraph(translate_label):
    if not st.session_state.get('uploaded_files'):
        st.write("Nenhum arquivo foi enviado")
        return

    files = [pd.read_csv(i, encoding='latin-1', sep=';') for i in st.session_state.uploaded_files]

    if not files:
        st.write("Nenhum dado encontrado nos arquivos.")
        return

    st.session_state.df = pd.concat(files, ignore_index=True)
    filtered_df = apply_filters(st.session_state.df, translate_label)

    if filtered_df.empty:
        st.write("Nenhum dado encontrado com os filtros aplicados.")
    else:
        st.write(filtered_df)

def run():
    st.set_page_config(
        page_title="Campus PI App", 
        page_icon="📈", 
        layout="wide", 
        initial_sidebar_state="expanded", 
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': """
                Este é um Projeto de Pesquisa desenvolvido para visualização, análise e transparência de dados do ifc araquari.
                \\
                \\
                Professor Responsavel: [Fábio Longo de Moura](www.github.com/ldmfabio) 
                \\
                Aluno Responsavel: [Mateus Lopes Albano](www.github.com/mateus-lopes)
                \
                \

            """
        }
    )

    if "is_running" not in st.session_state:
        st.session_state.is_running = False       

    with st.sidebar:
        st.write("# Opções:")
    
        st.session_state.selected_filter_status = st.selectbox(
            label="Situação da Matrícula:",
            options=filters.filter_options_status,
        )
       
        st.session_state.selected_filter_year = st.selectbox(
            label="Ciclos:",
            options=filters.filter_options_year,
        )
        
        st.session_state.selected_filter_curse = st.selectbox(
            label="Cursos:",
            options=filters.filter_options_curse,
        )

        st.session_state.uploaded_files = st.file_uploader("Escolha os Arquivos CSV", accept_multiple_files=True, help="Arraste e solte os arquivos aqui ou clique para fazer upload.")
        
        col1, col2 = st.columns(2)

        with col1:
            if st.button('Gerar Pesquisa', type="primary"):
                st.session_state.is_running = True

        with col2:
             if st.button('Voltar ao Inicio', type="secondary"):
                st.session_state.is_running = False

        st.write("*Versão 1.0.1*")

    if st.session_state.is_running:
        runGraph(filters.translate_label)
    else:
        runPage()

if __name__ == "__main__":
    run()