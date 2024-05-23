import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
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
                Este projeto de pesquisa tem como foco principal a análise dos indicadores de desempenho dos Institutos Federais. Através da coleta e análise de dados, pretendemos identificar áreas específicas que apresentam indicadores desfavoráveis, tais como taxa de evasão, desempenho acadêmico, satisfação dos alunos, entre outros.
                  
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
            st.caption("### Tabela de Status da Matrícula por Ciclo")
            table_status_formatted = df_manager.get_table_status(df_master)
            data_10 = {
                'ABANDONO': [2, 5, 3, 4, 6, 1, 0, 7, 8, 2],
                'CONCLUÍDA': [31, 28, 25, 30, 27, 22, 35, 32, 20, 33],
                'DESLIGADO': [13, 10, 12, 9, 8, 15, 17, 14, 19, 11],
                'EM_CURSO': [1, 3, 2, 4, 5, 3, 2, 6, 4, 5],
                'TRANSF_EXT': [1, 0, 2, 1, 3, 0, 1, 2, 1, 0],
                'TOTAL DE ALUNOS': [48, 46, 44, 48, 49, 41, 55, 61, 52, 51]
            }
            index_10 = [
                'MEDICINA VETERINÁRIA - PRESENCIAL - MAR. 2016 / MAR. 2021',
                'TÉCNICO EM AGROPECUÁRIA - EDUCAÇÃO PRESENCIAL - INTEGRADO - FEV. 2020 / DEZ. 2022',
                'ENGENHARIA CIVIL - PRESENCIAL - JAN. 2017 / DEZ. 2021',
                'CIÊNCIA DA COMPUTAÇÃO - EAD - JAN. 2018 / DEZ. 2022',
                'ADMINISTRAÇÃO - PRESENCIAL - MAR. 2019 / MAR. 2023',
                'PSICOLOGIA - PRESENCIAL - JAN. 2015 / DEZ. 2019',
                'BIOLOGIA - EAD - JUL. 2017 / JUL. 2021',
                'DIREITO - PRESENCIAL - JAN. 2016 / DEZ. 2020',
                'ENFERMAGEM - PRESENCIAL - JAN. 2018 / DEZ. 2022',
                'EDUCAÇÃO FÍSICA - EAD - MAR. 2020 / MAR. 2024'
            ]
            data_20 = {
                'ABANDONO': [2, 5, 3, 4, 6, 1, 0, 7, 8, 2, 5, 4, 3, 6, 2, 1, 7, 3, 5, 6],
                'CONCLUÍDA': [31, 28, 25, 30, 27, 22, 35, 32, 20, 33, 29, 26, 28, 24, 30, 31, 27, 25, 33, 32],
                'DESLIGADO': [13, 10, 12, 9, 8, 15, 17, 14, 19, 11, 12, 13, 10, 14, 15, 16, 11, 13, 17, 14],
                'EM_CURSO': [1, 3, 2, 4, 5, 3, 2, 6, 4, 5, 2, 3, 5, 4, 1, 6, 2, 4, 3, 5],
                'TRANSF_EXT': [1, 0, 2, 1, 3, 0, 1, 2, 1, 0, 1, 2, 0, 1, 3, 1, 2, 0, 1, 3],
                'TOTAL DE ALUNOS': [48, 46, 44, 48, 49, 41, 55, 61, 52, 51, 47, 45, 43, 48, 50, 40, 54, 60, 53, 50]
            }
            index_20 = [
                'MEDICINA VETERINÁRIA - PRESENCIAL - MAR. 2016 / MAR. 2021',
                'TÉCNICO EM AGROPECUÁRIA - EDUCAÇÃO PRESENCIAL - INTEGRADO - FEV. 2020 / DEZ. 2022',
                'ENGENHARIA CIVIL - PRESENCIAL - JAN. 2017 / DEZ. 2021',
                'CIÊNCIA DA COMPUTAÇÃO - EAD - JAN. 2018 / DEZ. 2022',
                'ADMINISTRAÇÃO - PRESENCIAL - MAR. 2019 / MAR. 2023',
                'PSICOLOGIA - PRESENCIAL - JAN. 2015 / DEZ. 2019',
                'BIOLOGIA - EAD - JUL. 2017 / JUL. 2021',
                'DIREITO - PRESENCIAL - JAN. 2016 / DEZ. 2020',
                'ENFERMAGEM - PRESENCIAL - JAN. 2018 / DEZ. 2022',
                'EDUCAÇÃO FÍSICA - EAD - MAR. 2020 / MAR. 2024',
                'FÍSICA - PRESENCIAL - MAR. 2018 / MAR. 2022',
                'QUÍMICA - PRESENCIAL - MAR. 2017 / MAR. 2021',
                'MATEMÁTICA - EAD - MAR. 2019 / MAR. 2023',
                'HISTÓRIA - PRESENCIAL - MAR. 2016 / MAR. 2020',
                'GEOGRAFIA - PRESENCIAL - MAR. 2015 / MAR. 2019',
                'FILOSOFIA - EAD - JUL. 2017 / JUL. 2021',
                'SOCIOLOGIA - PRESENCIAL - JAN. 2016 / DEZ. 2020',
                'LETRAS - PRESENCIAL - JAN. 2018 / DEZ. 2022',
                'PEDAGOGIA - EAD - MAR. 2020 / MAR. 2024',
                'ARTES - PRESENCIAL - JAN. 2017 / DEZ. 2021'
            ]
            data_30 = {
                'ABANDONO': [2, 5, 3, 4, 6, 1, 0, 7, 8, 2, 5, 4, 3, 6, 2, 1, 7, 3, 5, 6, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                'CONCLUÍDA': [31, 28, 25, 30, 27, 22, 35, 32, 20, 33, 29, 26, 28, 24, 30, 31, 27, 25, 33, 32, 23, 21, 22, 24, 26, 28, 25, 27, 29, 31],
                'DESLIGADO': [13, 10, 12, 9, 8, 15, 17, 14, 19, 11, 12, 13, 10, 14, 15, 16, 11, 13, 17, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
                'EM_CURSO': [1, 3, 2, 4, 5, 3, 2, 6, 4, 5, 2, 3, 5, 4, 1, 6, 2, 4, 3, 5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                'TRANSF_EXT': [1, 0, 2, 1, 3, 0, 1, 2, 1, 0, 1, 2, 0, 1, 3, 1, 2, 0, 1, 3, 2, 1, 3, 0, 1, 2, 1, 0, 3, 2],
                'TOTAL DE ALUNOS': [48, 46, 44, 48, 49, 41, 55, 61, 52, 51, 47, 45, 43, 48, 50, 40, 54, 60, 53, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
            }
            index_30 = [
                'MEDICINA VETERINÁRIA - PRESENCIAL - MAR. 2016 / MAR. 2021',
                'TÉCNICO EM AGROPECUÁRIA - EDUCAÇÃO PRESENCIAL - INTEGRADO - FEV. 2020 / DEZ. 2022',
                'ENGENHARIA CIVIL - PRESENCIAL - JAN. 2017 / DEZ. 2021',
                'CIÊNCIA DA COMPUTAÇÃO - EAD - JAN. 2018 / DEZ. 2022',
                'ADMINISTRAÇÃO - PRESENCIAL - MAR. 2019 / MAR. 2023',
                'PSICOLOGIA - PRESENCIAL - JAN. 2015 / DEZ. 2019',
                'BIOLOGIA - EAD - JUL. 2017 / JUL. 2021',
                'DIREITO - PRESENCIAL - JAN. 2016 / DEZ. 2020',
                'ENFERMAGEM - PRESENCIAL - JAN. 2018 / DEZ. 2022',
                'EDUCAÇÃO FÍSICA - EAD - MAR. 2020 / MAR. 2024',
                'FÍSICA - PRESENCIAL - MAR. 2018 / MAR. 2022',
                'QUÍMICA - PRESENCIAL - MAR. 2017 / MAR. 2021',
                'MATEMÁTICA - EAD - MAR. 2019 / MAR. 2023',
                'HISTÓRIA - PRESENCIAL - MAR. 2016 / MAR. 2020',
                'GEOGRAFIA - PRESENCIAL - MAR. 2015 / MAR. 2019',
                'FILOSOFIA - EAD - JUL. 2017 / JUL. 2021',
                'SOCIOLOGIA - PRESENCIAL - JAN. 2016 / DEZ. 2020',
                'LETRAS - PRESENCIAL - JAN. 2018 / DEZ. 2022',
                'PEDAGOGIA - EAD - MAR. 2020 / MAR. 2024',
                'ARTES - PRESENCIAL - JAN. 2017 / DEZ. 2021',
                'MÚSICA - PRESENCIAL - JAN. 2016 / DEZ. 2020',
                'TEATRO - PRESENCIAL - JAN. 2018 / DEZ. 2022',
                'CINEMA - PRESENCIAL - MAR. 2019 / MAR. 2023',
                'DANÇA - EAD - JUL. 2017 / JUL. 2021',
                'MODA - PRESENCIAL - MAR. 2018 / MAR. 2022',
                'DESIGN - PRESENCIAL - MAR. 2019 / MAR. 2023',
                'ARQUITETURA - PRESENCIAL - JAN. 2017 / DEZ. 2021',
                'ENGENHARIA AMBIENTAL - EAD - JUL. 2018 / JUL. 2022',
                'ENGENHARIA DE PRODUÇÃO - PRESENCIAL - JAN. 2016 / DEZ. 2020',
                'CIÊNCIAS CONTÁBEIS - PRESENCIAL - JAN. 2017 / DEZ. 2021'
            ]

            table_status_formatted_30 = pd.DataFrame(data_30, index=index_30)
            table_status_formatted_10 = pd.DataFrame(data_10, index=index_10)
            table_status_formatted_20 = pd.DataFrame(data_20, index=index_20)
            
            # table_status_formatted = table_status_formatted_10

            st.table(table_status_formatted)
            options = {
                "title": {"text": ""},
                "tooltip": {"trigger": "axis"},
                "legend": {"data": [], "left": "1%"},
                "grid": {"left": "1%", "right": "1%", "top": "32%", "containLabel": True},
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
                "center": ["50%", "18%"],
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

            if len(table_status_formatted.index.tolist()) > 10:
                height = 50 * len(table_status_formatted.index.tolist())
            else:
                height = 500

            options["series"].append(series_pie)
            st_echarts(options=options, height=f"{height}px")
        with tab2:
            df_manager.create_report_table(df_master)
        with tab3:
            st.info("🔎 Os ciclo críticos são identificados quando possuem menos de 3 alunos ativos.")
            critical_table = df_manager.create_critical_table(df_master)
            if not critical_table.empty:
                st.write(critical_table)
            else:
                st.success("Nenhum ciclo crítico encontrado.")

if __name__ == "__main__":
    run()