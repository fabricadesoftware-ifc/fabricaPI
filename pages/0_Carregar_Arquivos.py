import streamlit as st
import pandas as pd

def run():
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
    with st.sidebar:
        pass

    st.write("## 📃 Carregar Arquivos")

    if "data_frames" not in st.session_state:
        st.session_state.data_frames = []
        
    if not st.session_state.get('uploaded_files'):
        st.session_state.uploaded_files = []
    
    error_file = False
    
    files = st.file_uploader("Escolha os Arquivos CSV", accept_multiple_files=True, help="Arraste e solte os arquivos aqui ou clique para fazer upload.")

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        if st.button('Carregar arquivos', type="secondary"):
            if files:
                st.session_state.uploaded_files = files
            else:
                error_file = True

    with col2:
        if st.session_state.uploaded_files:
            if st.button('Limpar Escolha', type="secondary"):
                st.session_state.uploaded_files = []

    if error_file:
        st.write("( *Nenhum arquivo foi enviado* )")

    if st.session_state.uploaded_files:
        st.write("##### **Arquivos Carregados:**")
        st.write(f"( *{len(st.session_state.uploaded_files)} Arquivos Carregados* )")
        for obj in st.session_state.uploaded_files:
            st.write(f"- {obj.name}")

        if not st.session_state.data_frames:
            st.session_state.data_frames = [pd.read_csv(i, encoding='latin-1', sep=';') for i in st.session_state.uploaded_files]

if __name__ == "__main__":
    run()