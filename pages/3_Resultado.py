import streamlit as st
from utils import create_df_master, create_graph, create_df_status, init_session_state

def main():
    init_session_state()

    st.set_page_config(page_title="Resultado", page_icon="✅")
    st.markdown("## Relatório de Resultados")
    if not st.session_state.data_frames:
        st.error("Por favor, faça o upload de um arquivo.")
    else:
        df = create_df_master()
        
        # Dados Tratados
        st.divider()
        st.write(" #### Dataset com os dados tratados e limpos")
        st.write(df)

        # Gráfico de Status da Matricula
        st.divider()
        st.write(" #### Quantidade de alunos por status da matricula (Todos os ciclos)")
        [df_all, x, y] = create_df_status(0, df)
        create_graph(df_all, y, x)

        # Filtro por status
        st.divider()
        st.write(" #### Filtrar por status da matricula (Todos os ciclos)")
        status = st.multiselect(
            "Selecione as opções desejadas", ["ABANDONO", "TRANSF_EXT", "CONCLUÍDA", "DESLIGADO", "EM_CURSO"], ["EM_CURSO"]
        )
        df_status = df.set_index("NO_STATUS_MATRICULA").loc[status]
        st.write(df_status.sort_index())

        # Filtro por ciclo da matricula
        st.divider()
        st.write(" #### Filtrar por ciclo matricula (Gráfico interativo)")
        ciclo = st.multiselect(
            "Selecione as opções desejadas", ["2022369", "2680569"], "2022369"
        )
        df_ciclo = df.set_index("CO_CICLO_MATRICULA").loc[ciclo]
        st.write(df_ciclo.sort_index())

        # Gráfico de Status da Matricula
        [df_filter, x, y] = create_df_status(ciclo, df)
        create_graph(df_filter, y, x)

if __name__ == "__main__":
    main()
