import streamlit as st
from manager.dataframe_manager import DataframeManager
from manager.chart_manager import ChartManager
from streamlit_echarts import st_echarts

def run():
    df_manager = DataframeManager()
    chart_manager = ChartManager()
    st.set_page_config(
        page_title="Campus PI App | Apresentação", 
        page_icon="📉", 
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
    
    st.title("Relatório de Resultados")
   
    if "data_frames_cycles" not in st.session_state or len(st.session_state.data_frames_cycles) == 0 or "data_frames_students" not in st.session_state or len(st.session_state.data_frames_students) == 0:
        st.error("🚩 Por favor, faça o upload dos arquivos de estudantes e ciclos.")
        st.info('🔎 Se você já carrgou algum arquivo verifique se possui a formatação correta.')
    else:
        df_master = df_manager.get_master_dataframe()
        df_manager.create_indicators(df_master)
        st.divider()
        df_manager.create_subindicators(df_master)
        st.write("##")
        tab1, tab2, tab3 = st.tabs([
            "SITUAÇÃO DA MATRÍCULA POR CURSO", 
            "TODOS OS DADOS COLETADOS", 
            "CICLOS CRÍTICOS"
        ])

        with tab1:
            if len(st.session_state.uploaded_files_tranc) == 0:
                st.warning("👀 Não foram selecionados arquivos para alunos trancados")
            st.caption("### Tabela de Status da Matrícula por Ciclo")
            table_status_formatted = df_manager.get_table_status(df_master)
            height, bars_mt, pie_mt = df_manager.calculate_layout_params(table_status_formatted)
            options = {
                "title": {"text": ""},
                "tooltip": {"trigger": "axis"},
                "legend": {"data": [], "left": "1%"},
                "grid": {"left": "1%", "right": "1%", "top": bars_mt, "containLabel": True},
                "toolbox": {"feature": {"saveAsImage": {}}},
                "xAxis": {
                    "type": "value",
                },
                "yAxis": {
                    "type": "category",
                    "axisLabel": {"margin": 20 }, 
                    "axisTick": {"show": True},
                    "data": [i.split('-')[0] + i.split('-')[-1] for i in table_status_formatted.index.tolist()]
                },
                "series": []
            }

            for column in table_status_formatted.columns:
                series_line = {
                    "name": column,
                    "type": "bar",
                    "stack": column,
                    "smooth": True,
                    "data": table_status_formatted[column].tolist(),
                }
                options["legend"]["data"].append(column)
                options["series"].append(series_line)

            series_pie = {
                "name": "Soma Total (R$)",
                "type": "pie",
                "radius": ['12%', '20%'],
                "center": ["50%", pie_mt],
                "data": [
                    {"value": int(table_status_formatted[column].sum()), "name": column} for column in table_status_formatted.columns
                ],
                "emphasis": {
                    "label": {
                        "show": True,
                        "fontSize": 18,
                        "fontWeight": 'bold'
                    }
                },
                "label": {
                    "show": False,
                    "position": 'center',
                    "formatter": "{c}"
                }
            }
            options["series"].append(series_pie)

            st.table(table_status_formatted)
            st_echarts(options=options, height=f"{height}px")

        with tab2:
            st.info("🔎 Estamos apenas exibindo os dados no momento. Estamos trabalhando para oferecer visualizações mais detalhadas e informativas em breve.")
            df_manager.create_report_table(df_master)

        with tab3:
            st.info("🔎 Os ciclo críticos são identificados quando possuem menos de 3 alunos ativos.")
            critical_table = df_manager.create_critical_table(df_master)
            if critical_table is not None and not critical_table.empty:
                st.write(critical_table)
            else:
                st.success("✅ Nenhum ciclo crítico encontrado.")

if __name__ == "__main__":
    run()