import streamlit as st

from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

def reset_sidebar_options():
    st.session_state.is_running = False

def run():
    st.set_page_config(
        page_title="Campus PI App",
        page_icon="📈",
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

    if "is_running" not in st.session_state:
        st.session_state.is_running = False

    def runPage():
        st.markdown(
            """
            ## 📈 Projeto Campus PI  
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

    def runGraph():
        st.write('RODANDO GRAFICO...')
        st.write(st.session_state.selected_filter)
        st.write(st.session_state.uploaded_files)

    with st.sidebar:
        st.write("# Opções:")
        filter_options_status = (
            "Todas",
            "Em curso",
            "Concluinte",
            "Abandono", 
            "Desistente",
            "Transferido",
        )
        
        st.session_state.selected_filter = st.selectbox(
            label="Situação da Matrícula:",
            options=filter_options_status,
        )
       
        filter_options_year = (
            "Todos",
            "2018",
            "2019",
            "2020",
            "2021",
            "2022",
            "2023",
            "2024",
        )
        
        st.session_state.selected_filter = st.selectbox(
            label="Ciclos:",
            options=filter_options_year,
        )
        
        filter_options_curse = (
            "Todos",
            "Técnico em Informática",
            "Técnico em Eletromecânica",
            "Técnico em Mecânica",
        )
        
        st.session_state.selected_filter = st.selectbox(
            label="Cursos:",
            options=filter_options_curse,
        )

        st.session_state.uploaded_files = st.file_uploader("Escolha os Arquivos CSV", accept_multiple_files=True, help="Arraste e solte os arquivos aqui ou clique para fazer upload.")
        
        col1, col2 = st.columns(2)

        with col1:
            if st.button('Gerar Pesquisa', type="primary"):
                st.session_state.is_running = True

        with col2:
             if st.button('Voltar ao Inicio', type="secondary"):
                st.session_state.is_running = False

        st.write("*Versão 1.0.1*")

    if st.session_state.is_running:
        runGraph()
    else:
        runPage()

if __name__ == "__main__":
    run()