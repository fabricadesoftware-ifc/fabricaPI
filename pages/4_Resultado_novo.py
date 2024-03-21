import streamlit as st
import pandas as pd
from utils import get_tables, get_indicators, get_table_status, create_df_master, create_graph, create_df_status, create_df_merged, init_session_state, clean_df

def main():
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

    init_session_state()
    temporary_df = pd.read_csv('./assets/csv/example_ciclos.csv', encoding='latin-1', sep=';')

    st.markdown("## Relatório de Resultados")
    if not st.session_state.data_frames:
        st.error("Por favor, faça o upload de um arquivo.")
    else:
        st.session_state.master_data_frame = create_df_merged(temporary_df)
        # get_indicators(st.session_state.master_data_frame)

        get_tables(st.session_state.master_data_frame)


if __name__ == "__main__":
    main()
