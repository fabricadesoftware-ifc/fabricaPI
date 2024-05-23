import streamlit as st
import pandas as pd
from utils import create_df_students, create_graph, create_df_status, create_df_merged, init_session_state

def main():
    init_session_state()
    temporary_df = pd.read_csv('./assets/csv/example_ciclos.csv', encoding='latin-1', sep=';')

    st.set_page_config(page_title="Resultado", page_icon="✅")
    st.markdown("## Relatório de Resultados")
    if not st.session_state.data_frames_students or not st.session_state.data_frames_cycles:
        st.error("🚩 Por favor, faça o upload de um arquivo.")
    else:
        df = create_df_students()
        
        # Dados Tratados
        st.divider()
        st.write(" #### Dataset com os dados tratados e limpos")
        st.write(df)

        # Gráfico de Status da Matricula
        st.divider()
        st.write(" #### Quantidade de alunos por status da matricula (Todos os ciclos)")

        # df_merged_one = create_df_merged(temporary_df)
        # [df_all, x, y] = create_df_status(0, df_merged_one)
        # create_graph(df_all, y, x)

        # Filtro por status
        st.divider()
        st.write(" #### Filtrar por status da matricula (Todos os ciclos)")
        status = st.multiselect(
            "Selecione as opções desejadas", ["ABANDONO", "TRANSF_EXT", "CONCLUÍDA", "DESLIGADO", "EM_CURSO"], ["EM_CURSO"]
        )
        df_status = df.set_index("NO_STATUS_MATRICULA").loc[status]
        st.write(df_status.sort_index())
        
        # Filtro por ciclo da matricula
        df_merged = create_df_merged(temporary_df)
        st.divider()
        st.write(" #### Filtrar por ciclo matricula (Gráfico interativo)")
        ciclo = st.multiselect(
            "Selecione as opções desejadas", df_merged['CICLO DE MATRÍCULA'].unique(), df_merged['CICLO DE MATRÍCULA'].unique()[1]
        )
        df_ciclo = df_merged.set_index("CICLO DE MATRÍCULA").loc[ciclo]
        st.write(df_ciclo.sort_index())

        # Gráfico de Status da Matricula
        # [df_filter, x, y] = create_df_status(ciclo, df_merged)
        # create_graph(df_filter, y, x)

if __name__ == "__main__":
    main()
