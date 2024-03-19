import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np

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

    with st.sidebar:
        pass
    
    st.markdown(
        """
        ## 📉 Projeto Campus PI  
        #####
        ##### Descrição do Projeto:
        Este projeto de pesquisa tem como foco principal a análise dos indicadores de desempenho dos Institutos Federais. Através da coleta e análise de dados, pretendemos identificar áreas específicas que apresentam indicadores desfavoráveis.
        ##### Benefícios Esperados:
        - Melhoria da tomada de decisão através de dados concretos e visualizações claras.
        - Desenvolvimento de estratégias eficazes para melhorar os indicadores negativos.
        - Contribuição para a melhoria contínua da qualidade do ensino nos Institutos Federais.
        """
    )
        
    st.write(
        """
        ##### 
        \
        """
    )
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.image('./assets/img/logo-ifc.png', width=300)

    with col2:
        st.image('./assets/img/logo-fabrica.png')
    st.write("*Versão 1.0.2 (beta)*")


if __name__ == "__main__":
    run()