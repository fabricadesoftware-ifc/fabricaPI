import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

class DataframeManager:
    def __init__(self):
        self.dataframes = {}

    def init_session_state(self):
        if "data_frames_students" not in st.session_state:
            st.session_state.data_frames_students = []
        if "data_frames_cycles" not in st.session_state:
            st.session_state.data_frames_cycles = []
        if not st.session_state.get('uploaded_files_students'):
            st.session_state.uploaded_files_students = []
        if not st.session_state.get('uploaded_files_cycles'):
            st.session_state.uploaded_files_cycles = []

    def add_dataframe(self, dataframe, name):
        self.dataframes[name] = dataframe

    def get_dataframe(self, name):
        return self.dataframes[name]

    def remove_dataframe(self, name):
        del self.dataframes[name]

    def get_dataframe_names(self):
        return list(self.dataframes.keys())
    
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