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

    with st.sidebar:
        pass
    
    st.markdown(
        """
        ## 📉 Projeto Campus PI  
        \\
        Projeto de pesquisa institucional do campus IFC Araquari com foco na visualização, análise e transparência de dados. Para utilziar basta fazer upload do arquivo .csv e começar a explorar os dados. Você pode filtrar, ordenar, visualizar e exportar os dados, além de gerar gráficos e relatórios.
        ##
        """
    )
        
    st.write(
        """
        **Um projeto desenvolvido por:**
        \
        """
    )
    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.image('./assets/img/logo-ifc.png', width=300)

    with col2:
        st.image('./assets/img/logo-fabrica.png')
    st.write("*Versão 1.0.1 (beta)*")


if __name__ == "__main__":
    run()