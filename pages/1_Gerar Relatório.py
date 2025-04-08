import streamlit as st
from manager.dataframe_manager import DataframeManager
from streamlit_echarts import st_echarts
from matplotlib import pyplot as plt
import pandas as pd

def create_graph(self, df, y, x):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(df[y], df[x])
    ax.set_title('')
    ax.set_xlabel('Quantidade de alunos')
    ax.set_ylabel('')

    for i,v in enumerate(df[x]):
        ax.text(v + 1, i, str(v), color="black", fontsize=8, ha="left", va="center")

    ax.yaxis.set_tick_params(labelsize=12)
    ax.xaxis.set_tick_params(labelsize=12)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    st.pyplot(fig)

def get_filtered_df(self, df, ciclo, curse):
    if ciclo in df['CICLO DE MATRÍCULA'].unique() and curse in df[df['CICLO DE MATRÍCULA'] == ciclo]['NOME DO CURSO'].unique():
        df_filtered = df[(df['CICLO DE MATRÍCULA'] == ciclo) & (df['NOME DO CURSO'] == curse)]
        status_counts = df_filtered['NO_STATUS_MATRICULA'].value_counts().reset_index()
        status_counts.columns = ['Status da Matrícula', 'Total']
        return status_counts
    else:
        return pd.DataFrame({'Status da Matrícula': [], 'Total': []})

def generate_chart(self, df):
    col1, col2 = st.columns(2)

    with col1:
        cycle = st.selectbox('Ciclo de Matrícula', df['CICLO DE MATRÍCULA'].unique())
    with col2:
        curse_options = df[df['CICLO DE MATRÍCULA'] == cycle]['NOME DO CURSO'].unique()
        curse = st.selectbox('Nome do Curso', curse_options)

    df_filtro_NO_STATUS_MATRICULA = self.get_filtered_df(df, cycle, curse)
    st.bar_chart(data=df_filtro_NO_STATUS_MATRICULA, y='Total', x='Status da Matrícula')

def run():
    df_manager = DataframeManager()

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
            # if len(st.session_state.uploaded_files_tranc) == 0:
            #     st.warning("👀 Não foram selecionados arquivos para alunos trancados")
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