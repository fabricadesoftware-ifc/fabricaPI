from urllib.error import URLError
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st


def data_frame_demo():
    # @st.cache_data
    def get_UN_data():
        df = pd.concat(st.session_state.data_frames, ignore_index=True)
        df['CO_CICLO_MATRICULA'] = df['CO_CICLO_MATRICULA'].astype(str)
        return df

    def getGraph(df, title=''):
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
        ax.set_title(title)
        ax.set_xlabel('Quantidade de alunos')
        ax.set_ylabel('')

        for i,v in enumerate(df_NO_STATUS_MATRICULA['Total']):
            ax.text(v + 1, i, str(v), color="black", fontsize=8, ha="left", va="center")


        ax.yaxis.set_tick_params(labelsize=10)
        ax.xaxis.set_tick_params(labelsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        st.pyplot(fig)

    try:
        df = get_UN_data()
        st.write(df)

        # filtro por status
        st.write("### Filtrar por status da matricula")
        status = st.multiselect(
            "Selecione as opções desejadas", ["ABANDONO", "TRANSF_EXT", "CONCLUÍDA", "DESLIGADO", "EM_CURSO"], ["EM_CURSO"]
        )
        if not status:
            st.error("Please select at least one NO_STATUS_MATRICULA.")
        else:
            df.set_index("NO_STATUS_MATRICULA", inplace=True)
            df_status = df.loc[status]
            st.write(df_status.sort_index())
            getGraph(df)

        # filtro por ciclo
        st.write("### Filtrar por ciclo da matricula")
        ciclo = st.multiselect(
            "Selecione as opções desejadas", ["2022369", "2680569"], "2022369"
        )
        if not ciclo:
            st.error("Please select at least one NO_STATUS_MATRICULA.")
        else:
            df.set_index("CO_CICLO_MATRICULA", inplace=True)
            df_ciclo = df.loc[ciclo]
            st.write(df_ciclo.sort_index())
            getGraph(get_UN_data().set_index("NO_STATUS_MATRICULA"))

    except URLError as e:
        st.error(
            """
            **This demo requires internet access.**
            Connection error: %s
        """
            % e.reason
        )


st.set_page_config(page_title="DataFrame Demo", page_icon="✅")
st.markdown("## ✅ Dados Unificados")


if __name__ == "__main__":
    data_frame_demo()