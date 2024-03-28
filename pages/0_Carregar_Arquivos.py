import streamlit as st
import pandas as pd
from manager.dataframe_manager import DataframeManager

def run():
    df_manager = DataframeManager()
    df_manager.init_session_state()
    st.set_page_config(
        page_title="Campus PI App | Carregar Arquivos", 
        page_icon="📃", 
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
    st.write("## 📃 Carregar Arquivos")
    tab1, tab2 = st.tabs(["SISTEC ALUNOS", "SISTEC CICLOS"])

    with tab1:
        error_file = False
    
        files = st.file_uploader("Escolha os Arquivos CSV", accept_multiple_files=True, help="Arraste e solte os arquivos aqui ou clique para fazer upload.", key="file_uploader_students")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            if st.button('Carregar arquivos', type="secondary", key="load_files_students"):
                if files:
                    st.session_state.uploaded_files_students = files
                else:
                    error_file = True

        with col2:
            if st.session_state.uploaded_files_students:
                if st.button('Limpar Escolha', type="secondary", key="clean_files_"):
                    st.session_state.uploaded_files_students = []

        if error_file:
            st.write("( *Nenhum arquivo foi enviado* )")

        if st.session_state.uploaded_files_students:
            st.write("##### **Arquivos Carregados:**")
            st.write(f"( *{len(st.session_state.uploaded_files_students)} Arquivos Carregados* )")
            for obj in st.session_state.uploaded_files_students:
                st.write(f"- {obj.name}")

            if not st.session_state.data_frames_students:
                st.session_state.data_frames_students = [pd.read_csv(i, encoding='latin-1', sep=';') for i in st.session_state.uploaded_files_students]

    with tab2:
        error_file = False
    
        files = st.file_uploader("Escolha os Arquivos CSV", accept_multiple_files=True, help="Arraste e solte os arquivos aqui ou clique para fazer upload.", key="file_uploader_cycles")

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            if st.button('Carregar arquivos', type="secondary", key="load_files_cycles"):
                if files:
                    st.session_state.uploaded_files_cycles = files
                else:
                    error_file = True

        with col2:
            if st.session_state.uploaded_files_cycles:
                if st.button('Limpar Escolha', type="secondary", key="clean_files_cycles"):
                    st.session_state.uploaded_files_cycles = []

        if error_file:
            st.write("( *Nenhum arquivo foi enviado* )")

        if st.session_state.uploaded_files_cycles:
            st.write("##### **Arquivos Carregados:**")
            st.write(f"( *{len(st.session_state.uploaded_files_cycles)} Arquivos Carregados* )")
            for obj in st.session_state.uploaded_files_cycles:
                st.write(f"- {obj.name}")

            if not st.session_state.data_frames_cycles:
                st.session_state.data_frames_cycles = [pd.read_csv(i, encoding='latin-1', sep=';') for i in st.session_state.uploaded_files_cycles]
    

    
    

if __name__ == "__main__":
    run()