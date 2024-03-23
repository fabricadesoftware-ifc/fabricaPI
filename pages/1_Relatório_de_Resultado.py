import streamlit as st
from utils import *

def main():
    init_session_state()
    st.set_page_config(
        page_title="Campus PI App | Resultado", 
        page_icon="✅", 
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

    st.markdown("## ✅ Relatório de Resultados")

    if not st.session_state.data_frames_students:
        st.error("Por favor, faça o upload do arquivo de dados dos alunos.")
    elif not st.session_state.data_frames_cycles:
        st.error("Por favor, faça o upload do arquivo de dados dos ciclos.")
    else:
        df_cycles = create_df_cycles()
        df_students = create_df_students()
        st.session_state.master_data_frame = create_df_merged(df_cycles, df_students)
        
        st.write("#")
        get_indicators(st.session_state.master_data_frame)
        st.divider()
        get_subindicators(st.session_state.master_data_frame)
        st.write("#")
        get_tables(st.session_state.master_data_frame)
if __name__ == "__main__":
    main()