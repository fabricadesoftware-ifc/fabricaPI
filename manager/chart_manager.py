import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

class ChartManager:
    def __init__(self):
        pass
    
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