import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

class DataframeManager:
    def __init__(self):
        self.init_session_state()

    def init_session_state(self):
        if "error_file_message" not in st.session_state:
            st.session_state.error_file_message = ''
        if "data_frames_students" not in st.session_state:
            st.session_state.data_frames_students = []
        if "data_frames_cycles" not in st.session_state:
            st.session_state.data_frames_cycles = []
        if not st.session_state.get('uploaded_files_students'):
            st.session_state.uploaded_files_students = []
        if not st.session_state.get('uploaded_files_cycles'):
            st.session_state.uploaded_files_cycles = []
        if not st.session_state.get('error_file'):
            st.session_state.error_file = False
        if not st.session_state.get('error_file_message'):
            st.session_state.error_file_message = ""

    def get_dataframe_names(self, name):
        if name in st.session_state:
            return st.session_state[name].keys()
    
    def concact_data_sets(self, data_frames):
        return pd.concat(data_frames, ignore_index=True)

    def create_indicators(self, df):
        pass

    def create_report_table(self, df):
        pass

    def create_master_table(self, df):
        pass

    def create_critical_table(self, df):
        pass

    def verify_files(self, files, one_file=False):
        st.session_state.error_file_message = ''
        if not files:
            st.session_state.error_file_message = "Por favor, selecione algum arquivo."
            return False
        
        for i, x in enumerate(files):
            if not files[i].name.split('.')[-1] == 'csv':
                st.session_state.error_file_message = "Os arquivos selecionados não correspondem a um arquivo CSV. Por favor, selecione um arquivo CSV válido."
                return False
        
        if not len(files) == 1 and one_file:
            st.session_state.error_file_message = "Por favor, selecione apenas um arquivo."
            return False
        return True