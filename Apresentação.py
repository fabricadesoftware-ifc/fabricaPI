import streamlit as st

def run():
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
    
    st.title("📉 Projeto Campus PI  ")
    st.markdown(
        """
        #### Descrição do Projeto:
        Este projeto de pesquisa tem como foco principal a análise dos indicadores de desempenho dos Institutos Federais. Através da coleta e análise de dados, pretendemos identificar áreas específicas que apresentam indicadores desfavoráveis.
        #### Benefícios Esperados:
        - Melhoria da tomada de decisão através de dados concretos e visualizações claras.
        - Desenvolvimento de estratégias eficazes para melhorar os indicadores negativos.
        - Contribuição para a melhoria contínua da qualidade do ensino nos Institutos Federais.
        #####
        """
    )

    col1, col2, col3 = st.columns(3, gap="large")
    col1.image('./assets/img/logo-ifc.png', width=300)
    col2.image('./assets/img/logo-fabrica.png')

    st.write("""
        ###### Professor: [Fábio Longo de Moura](www.github.com/ldmfabio) &nbsp;&nbsp;&nbsp;&nbsp; Aluno: [Mateus Lopes Albano](www.github.com/mateus-lopes)
        *Versão 1.1.0*
    """)

if __name__ == "__main__":
    run()