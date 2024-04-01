import streamlit as st
from manager.dataframe_manager import DataframeManager
from manager.chart_manager import ChartManager

def main():
    df_manager = DataframeManager()
    chart_manager = ChartManager()
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

    if not st.session_state.data_frames_students or len(st.session_state.data_frames_students) == 0:
        st.error("Por favor, faça o upload dos arquivos de estudantes.")
    elif not st.session_state.data_frames_cycles or len(st.session_state.data_frames_cycles) == 0:
        st.error("Por favor, faça o upload do arquivo de dados dos ciclos.")
    else:
        st.session_state.data_frame_cycles = df_manager.concact_data_sets(st.session_state.data_frames_cycles, cycles=True)
        st.session_state.data_frame_students = df_manager.concact_data_sets(st.session_state.data_frames_students, students=True)
        st.session_state.master_data_frame = df_manager.get_master_dataframe(st.session_state.data_frame_cycles, st.session_state.data_frame_students)
        df_manager.create_indicators(st.session_state.master_data_frame)
        st.divider()
        df_manager.create_subindicators(st.session_state.master_data_frame)

        tab1, tab2, tab3 = st.tabs([
            "SITUAÇÃO DA MATRÍCULA POR CURSO", 
            "TODOS OS DADOS COLETADOS", 
            "CICLOS CRÍTICOS"
        ])

        with tab1:
            st.write("#### Tabela de Status da Matrícula por Ciclo")
            st.write(df_manager.get_table_status(st.session_state.master_data_frame))
            st.write("#### Gráfico de Status da Matrícula por Ciclo")
            chart_manager.generate_chart(st.session_state.master_data_frame)  
        with tab2:
            df_manager.create_report_table(st.session_state.master_data_frame)
        with tab3:
            st.write(df_manager.create_critical_table(st.session_state.master_data_frame))

if __name__ == "__main__":
    main()