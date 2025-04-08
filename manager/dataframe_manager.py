import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import re
from streamlit.logger import get_logger
from manager.config import TABLE_STATUS_COLUMNS, TABLE_TRANC 

LOGGER = get_logger(__name__)

class DataframeManager:
    def __init__(self):
        self.init_session_state()

    def init_session_state(self):
        if "data_frames_students" not in st.session_state:
            st.session_state.data_frames_students = []
        if "data_frames_cycles" not in st.session_state:
            st.session_state.data_frames_cycles = []
        if "data_frames_tranc" not in st.session_state:
            st.session_state.data_frames_tranc = []
        if not st.session_state.get('uploaded_files_students'):
            st.session_state.uploaded_files_students = []
        if not st.session_state.get('uploaded_files_tranc'):
            st.session_state.uploaded_files_tranc = []
        if not st.session_state.get('uploaded_files_cycles'):
            st.session_state.uploaded_files_cycles = []
        
    def get_dataframe_names(self, name):
        if name in st.session_state:
            return st.session_state[name].keys()

    def extract_year(self, ciclo_str):
        match = re.search(r'\b\d{4}\b', ciclo_str)
        return match.group(0) if match else None
    
    def extract_curse(self, i):
        return i.split(' - ')[0] if ' - ' in i else i

    def get_locked_students(self):
        csv = pd.concat(st.session_state.data_frames_tranc, ignore_index=True)
        new_column_names = TABLE_TRANC

        for i, col in enumerate(csv.columns):
            csv.rename(columns={col: new_column_names[i]}, inplace=True)

        csv['CICLO_EXTRAIDO'] = csv['MATRICULA_TRANC'].astype(str).str[:4]
        df_grouped = csv.groupby(['CICLO_EXTRAIDO', 'CURSO_TRANC'])['NOME_TRANC'].count()
        
        return df_grouped
    
    def get_table_status(self, df):
        table_status = df.groupby(['CICLO DE MATRÍCULA', 'NO_STATUS_MATRICULA']).size().unstack(fill_value=0)
        table_status['TOTAL DE ALUNOS'] = table_status.sum(axis=1)

        if "CONCLUï¿½DA" in table_status.columns:
            table_status.rename(columns={"CONCLUï¿½DA": "CONCLUÍDA"}, inplace=True)

        status_columns = TABLE_STATUS_COLUMNS
        missing_columns = set(status_columns) - set(table_status.columns)
        for column in missing_columns:
            table_status[column] = 0

        table_status['CURSO'] = table_status.index.to_series().apply(self.extract_curse)
        table_status['ANO'] = table_status.index.to_series().apply(self.extract_year)

        df_presentation = table_status[status_columns]

        if len(st.session_state.uploaded_files_tranc) > 0:
            ciclo_counts = self.get_locked_students()
            for index, value in ciclo_counts.items():
                year, curse = index
                mask = (table_status['ANO'] == year) & (table_status['CURSO'] == curse)
                table_status.loc[mask, 'TRANCADO'] = value

            df_presentation['TRANCADO'] = table_status['TRANCADO']
            df_presentation['FREQUENTANDO'] = abs(table_status['EM_CURSO'] - table_status['TRANCADO'])

        df_presentation = df_presentation.reset_index()
        df_presentation.rename(columns={'CICLO DE MATRÍCULA': 'NOME DO CICLO'}, inplace=True)
        table_status_formatted = df_presentation.set_index('NOME DO CICLO')
        
        return table_status_formatted

    def create_indicators(self, df):
        indicators = [
            {
                "title": "Total de Alunos",
                "value": df.shape[0]
            },
            {
                "title": "Total de Ciclos Críticos",
                "value": self.get_table_status(df).query('EM_CURSO < 2').shape[0]
            },
            {
                "title": "Total de Ciclos",
                "value": df["CICLO DE MATRÍCULA"].nunique()
            },
            {
                "title": "Total de Cursos",
                "value": df["NOME DO CURSO"].nunique()
            },
            {
                "title": "Total de Municípios",
                "value": df["MUNICIPIO"].nunique()
            }
        ]
        col1, col2, col3, col4, col5 = st.columns(5)

        for item, column in zip(indicators, [col1, col2, col3, col4, col5]):
            with column:
                st.write(f"## {item['value']}")
                st.caption(f"{item['title']}")
        return indicators
    
    def create_subindicators(self, df):
        subindicators = [
            {
                "title": "Total em curso",
                "value": df.query('NO_STATUS_MATRICULA == "EM_CURSO"').shape[0]
            },
            {
                "title": "Total de concluentes",
                "value": df.query('NO_STATUS_MATRICULA == "CONCLUÍDA"').shape[0]
            },
            {
                "title": "Total de transferidos",
                "value": df.query('NO_STATUS_MATRICULA == "TRANSF_EXT"').shape[0]
            },
            {
                "title": "Total de desistentes",
                "value": df.query('NO_STATUS_MATRICULA == "ABANDONO"').shape[0]
            },
            {
                "title": "Total de desligados",
                "value": df.query('NO_STATUS_MATRICULA == "DESLIGADO"').shape[0]
            }
        ]

        col1, col2, col3, col4, col5 = st.columns(5)

        for item, column in zip(subindicators, [col1, col2, col3, col4, col5]):
            value = item["value"]
            title = item["title"]
            with column:
                st.write(f"## {value}")
                st.caption(title)
        
        return subindicators

    def create_selection_options(self, df, column_name):
        options = df[column_name].unique()
        options = ['TODOS'] + options.tolist()
        return options

    def apply_filter(self, df, column_name, selected_option):
        if selected_option == 'TODOS':
            return df
        else:
            return df[df[column_name] == selected_option]
        
    def apply_filters(self, df, filters):
        df = self.apply_filter(df, "CICLO DE MATRÍCULA", filters['cycle'])
        df = self.apply_filter(df, "NOME DO CURSO", filters['curse'])
        df = self.apply_filter(df, "NO_STATUS_MATRICULA", filters['status'])
        df = self.apply_filter(df, "MUNICIPIO", filters['municipality'])

        return df

    def create_report_table(self, df):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            cycle_options = self.create_selection_options(df, "CICLO DE MATRÍCULA")
            cycle = st.selectbox('Ciclo de Matrícula', cycle_options)

        with col2:
            curse_options = self.create_selection_options(df, "NOME DO CURSO")
            curse = st.selectbox('Curso', curse_options)

        with col3:
            status_options = self.create_selection_options(df, "NO_STATUS_MATRICULA")
            status = st.selectbox('Status da Matrícula', status_options)
        
        with col4:
            municipality_options = self.create_selection_options(df, "MUNICIPIO")
            municipality = st.selectbox('Município', municipality_options)

        # Aplicar filtros
        df_with_filters = df.copy()
        df_with_filters = self.apply_filters(df_with_filters, {
            'cycle': cycle,
            'curse': curse,
            'status': status,
            'municipality': municipality
        })

        st.write(df_with_filters)

        return df_with_filters
        
    def create_critical_table(self, df):
        for i in df["CICLO DE MATRÍCULA"].unique():
            if self.get_table_status(df).query(f'`NOME DO CICLO` == "{i}" and EM_CURSO < 3').shape[0] > 0:
                st.write(f"#### Ciclo: {i.lower()}")
                isShow = st.toggle('Mostrar somente os alunos em curso', True)
                if isShow:
                    return df.query(f'`CICLO DE MATRÍCULA` == "{i}" and NO_STATUS_MATRICULA == "EM_CURSO"')
                else:
                    return df.query(f'`CICLO DE MATRÍCULA` == "{i}"')

    def get_master_dataframe(self):
        df_cycles =  self.concact_data_sets(st.session_state.data_frames_cycles, students=False)
        df_students =  self.concact_data_sets(st.session_state.data_frames_students, students=True)
        return pd.merge(df_cycles, df_students, left_on='CÓDIGO CICLO DE MATRÍCULA', right_on='CO_CICLO_MATRICULA', how='inner')

    def concact_data_sets(self, data_frames, students=False):
        if students:
            for i in range(len(data_frames)):
                if 'CO_CICLO_MATRICULA' in data_frames[i].columns:
                    data_frames[i]['CO_CICLO_MATRICULA'] = data_frames[i]['CO_CICLO_MATRICULA'].astype(str)
        else:
            for i in range(len(data_frames)):
                if 'CÓDIGO CICLO DE MATRÍCULA' in data_frames[i].columns:
                    data_frames[i]['CÓDIGO CICLO DE MATRÍCULA'] = data_frames[i]['CÓDIGO CICLO DE MATRÍCULA'].astype(str)
        return pd.concat(data_frames, ignore_index=True)
    
    def clean_df(self, df):
        if df.shape[0] > 1:
            for column in df.columns:
                if len(df[column].unique()) == 1 or df[column].isnull().sum() > len(df) * 0.5:
                    df = df.drop(column, axis=1)
        return df
    
    def calculate_layout_params(self, table_status):
        num_rows = len(table_status.index)

        if num_rows <= 10:
            height = 900
            bars_mt = "32%"
            pie_mt = "18%"
        elif num_rows <= 20:
            height = 100 * num_rows
            bars_mt = "15%"
            pie_mt = "8%"
        elif num_rows <= 30:
            height = 100 * num_rows
            bars_mt = "12%"
            pie_mt = "6%"
        else:
            height = 100 * num_rows
            bars_mt = "6.5%"
            pie_mt = "3.5%"
        
        return height, bars_mt, pie_mt
        
