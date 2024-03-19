from urllib.error import URLError
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

def init_session_state():
    if "data_frames" not in st.session_state:
        st.session_state.data_frames = None
    if "data" not in st.session_state:
        st.session_state.data = None
    if "df" not in st.session_state:
        st.session_state.df = None

def create_df_master():
    df = pd.concat(st.session_state.data_frames, ignore_index=True)
    df['CO_CICLO_MATRICULA'] = df['CO_CICLO_MATRICULA'].astype(str)
    return df

def create_df_status(ciclo, df_master):
    new_df = []

    if ciclo:
        filter = f'CO_CICLO_MATRICULA == {ciclo}'
    else:
        filter = 'CO_CICLO_MATRICULA != "PINTO"'

    labels_status = df_master.query(f'{filter}')["NO_STATUS_MATRICULA"].unique()
    
    for i in labels_status:
            count = df_master.query(f'{filter} & NO_STATUS_MATRICULA == "{i}"')["NO_STATUS_MATRICULA"].count()
            new_df.append({'Status da Matricula': i, 'Total': count})

    # retorna o dataframe e as labels de x e y
    return [pd.DataFrame(new_df), 'Total', 'Status da Matricula']


def create_graph(df, y, x):
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
