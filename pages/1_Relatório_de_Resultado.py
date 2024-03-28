import streamlit as st
from manager.dataframe_manager import DataframeManager

def main():
    df_manager = DataframeManager()
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
        st.error("Por favor, faça o upload dos arquivos corretamente.")
    elif not st.session_state.data_frames_cycles:
        st.error("Por favor, faça o upload do arquivo de dados dos ciclos.")
    else:
        df_cycles = df_manager.concact_data_sets(st.session_state.data_frames_cycles, cycles=True)
        df_students = df_manager.concact_data_sets(st.session_state.data_frames_students, students=True)
        st.session_state.master_data_frame = df_manager.get_master_dataframe(df_cycles, df_students)
        df_manager.create_indicators(st.session_state.master_data_frame)
        st.divider()
        df_manager.create_subindicators(st.session_state.master_data_frame)
        df_manager.create_tabs(st.session_state.master_data_frame)

if __name__ == "__main__":
    main()