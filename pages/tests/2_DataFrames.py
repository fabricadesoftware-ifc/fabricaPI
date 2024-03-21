import streamlit as st
from utils import read_files

def run():
    st.set_page_config(
        page_title="Campus PI App | DataFrames", 
        page_icon="🔢", 
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
    st.write("## 🔢 DataFrames")

    if not st.session_state.get('uploaded_files'):
        st.session_state.uploaded_files = []
    
    if not st.session_state.get('data_frames'):
        st.session_state.data_frames = read_files(st.session_state.uploaded_files)
    
    if len(st.session_state.uploaded_files) == 0:
        st.write("( *Nenhum dado encontrado nos arquivos.* )")
        st.page_link("pages/0_Carregar_Arquivos.py", label="Carregar Arquivos", icon="📃")
    else:
        st.write(f"( *Foram gerados {len(st.session_state.uploaded_files)} dataFrames.* )")
   
    for index, obj in enumerate(st.session_state.data_frames):
        st.write(f"#### {st.session_state.uploaded_files[index].name.split('.')[0]}")
        st.write(obj)
    
if __name__ == "__main__":
    run()