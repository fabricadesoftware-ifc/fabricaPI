import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import matplotlib.pyplot as plt

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(
        page_title="Campus PI App | Gráficos", 
        page_icon="📊", 
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
    st.write("## 📊 Gráficos")

    if "data_frames" not in st.session_state:
        st.session_state.data_frames = []

    def get_UN_data():
        if st.session_state.data_frames:
            df = pd.concat(st.session_state.data_frames, ignore_index=True)
            return df.set_index("NO_STATUS_MATRICULA")
        else:
            return pd.DataFrame()

    df = get_UN_data()
    df_alunos_abandono = df[df.index == 'ABANDONO'].shape[0]
    df_alunos_transf_ext = df[df.index == 'TRANSF_EXT'].shape[0]
    df_alunos_concluida = df[df.index == 'CONCLUÍDA'].shape[0]
    df_alunos_desligado = df[df.index == 'DESLIGADO'].shape[0]
    df_alunos_em_curso = df[df.index == 'EM_CURSO'].shape[0]

    df_NO_STATUS_MATRICULA = pd.DataFrame({
        'NO_STATUS_MATRICULA': ['ABANDONO', 'TRANSF_EXT', 'CONCLUÍDA', 'DESLIGADO', 'EM_CURSO'],
        'Total': [df_alunos_abandono, df_alunos_transf_ext, df_alunos_concluida, df_alunos_desligado, df_alunos_em_curso]
    })

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(df_NO_STATUS_MATRICULA["NO_STATUS_MATRICULA"], df_NO_STATUS_MATRICULA['Total'])
    ax.set_title('')
    ax.set_xlabel('Quantidade de alunos')
    ax.set_ylabel('')

    for i,v in enumerate(df_NO_STATUS_MATRICULA['Total']):
        ax.text(v + 1, i, str(v), color="black", fontsize=8, ha="left", va="center")


    ax.yaxis.set_tick_params(labelsize=10)
    ax.xaxis.set_tick_params(labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if st.session_state.data_frames != []:
        st.write("#### Quantidade de alunos por status de matricula")
        st.pyplot(fig)
    else:
        st.write("( *Nenhum dado encontrado nos arquivos.* )")
        st.page_link("pages/0_Carregar_Arquivos.py", label="Carregar Arquivos", icon="📃")

if __name__ == "__main__":
    run()