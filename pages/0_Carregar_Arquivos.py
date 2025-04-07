from manager.dataframe_manager import DataframeManager
import streamlit as st
import pandas as pd

def verify_files(files, one_file=False):
    if not files:
        st.toast("⚠️ Você não selecionou nenhum arquivo CSV. ⚠️")
        return False
    for f in files:
        if not f.name.endswith('.csv'):
            st.toast("⚠️ Os arquivos selecionados não são CSVs. ⚠️")
            return False
    if one_file and len(files) != 1:
        st.toast("⚠️ Você deve selecionar apenas um arquivo CSV. ⚠️")
        return False
    return True

def run():
    df_manager = DataframeManager()

    st.set_page_config(
        page_title="Campus PI App | Carregar Arquivos", 
        page_icon="📃", 
        layout="wide", 
        initial_sidebar_state="expanded", 
        menu_items={
            'Get Help': 'https://www.extremelycoolapp.com/help',
            'Report a bug': "https://www.extremelycoolapp.com/bug",
            'About': """
                Este projeto de pesquisa tem como foco principal a análise dos indicadores de desempenho dos Institutos Federais. Através da coleta e análise de dados, pretendemos identificar áreas específicas que apresentam indicadores desfavorávei e buscar ciclos críticos.
                ###### Professor Responsavel: [Fábio Longo de Moura](www.github.com/ldmfabio)
                ###### Aluno Responsavel: [Mateus Lopes Albano](www.github.com/mateus-lopes)
                ##
            """
        }
    )
    st.title("Carregar Arquivos")
    
    tab1, tab2, tab3 = st.tabs(["SISTEC ALUNOS", "SISTEC CICLOS", "TRANCADOS"])
    
    with tab1:
        files = st.file_uploader("Escolha os Arquivos CSV", accept_multiple_files=True, help="Arraste e solte os arquivos aqui ou clique para fazer upload.", key="file_uploader_students")
        col1, col2 = st.columns((2, 10))

        with col1:
            if st.button('Carregar arquivos', type="secondary", key="load_files_students"):
                if verify_files(files):
                    st.session_state.uploaded_files_students = files
                    st.session_state.data_frames_students = [pd.read_csv(i, encoding='latin-1', encoding_errors='replace', sep=';') for i in st.session_state.uploaded_files_students]

        with col2:
            if st.session_state.uploaded_files_students:
                if st.button('Limpar Escolha', type="secondary", key="clean_files_"):
                    st.session_state.uploaded_files_students = []
                    st.session_state.data_frames_students = []

        if st.session_state.uploaded_files_students:
            st.write("##### **Arquivos Carregados:**")
            st.write(f"( *{len(st.session_state.uploaded_files_students)} Arquivos Carregados* )")
            for obj in st.session_state.uploaded_files_students:
                st.write(f"- {obj.name}")

    with tab2:
        files = st.file_uploader("Escolha os Arquivos CSV", accept_multiple_files=True, help="Arraste e solte os arquivos aqui ou clique para fazer upload.", key="file_uploader_cycles")
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        with col1:
            if st.button('Carregar arquivos', type="secondary", key="load_files_cycles"):
                if verify_files(files):
                    st.session_state.uploaded_files_cycles = files
                    st.session_state.data_frames_cycles = [pd.read_csv(i, encoding='latin-1', encoding_errors='replace', sep=';') for i in st.session_state.uploaded_files_cycles]

        with col2:
            if st.session_state.uploaded_files_cycles:
                if st.button('Limpar Escolha', type="secondary", key="clean_files_cycles"):
                    st.session_state.uploaded_files_cycles = []
                    st.session_state.data_frames_cycles = []

        if st.session_state.uploaded_files_cycles:
            st.write("##### **Arquivos Carregados:**")
            st.write(f"( *{len(st.session_state.uploaded_files_cycles)} Arquivos Carregados* )")
            for obj in st.session_state.uploaded_files_cycles:
                st.write(f"- {obj.name}")

    with tab3:
        st.info("⚙️ Esta funcionalidade ainda está em desenvolvimento. Em breve estará disponível!")
        
        files = st.file_uploader("Escolha os Arquivos CSV", accept_multiple_files=True, help="Arraste e solte os arquivos aqui ou clique para fazer upload.", key="file_uploader_tranc", disabled=True)
        col1, col2 = st.columns((2, 10))

        with col1:
            if st.button('Carregar arquivos', type="secondary", key="load_files_tranc", disabled=True):
                if verify_files(files):
                    st.session_state.uploaded_files_tranc = files
                    st.session_state.data_frames_tranc = [pd.read_csv(i, encoding='latin-1', encoding_errors='replace', sep=';') for i in st.session_state.uploaded_files_tranc]

        with col2:
            if st.session_state.uploaded_files_tranc:
                if st.button('Limpar Escolha', type="secondary", key="clean_files_tranc", disabled=True):
                    st.session_state.uploaded_files_tranc = []
                    st.session_state.data_frames_tranc = []

        if st.session_state.uploaded_files_tranc:
            st.write("##### **Arquivos Carregados:**")
            st.write(f"( *{len(st.session_state.uploaded_files_tranc)} Arquivos Carregados* )")
            for obj in st.session_state.uploaded_files_tranc:
                st.write(f"- {obj.name}")

if __name__ == "__main__":
    run()