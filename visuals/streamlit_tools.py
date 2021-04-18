import os
import pandas as pd

import streamlit as st

def settings():
    st.set_page_config(layout='wide')

def file_name_from_folder(folder_path: str):
    # Get file names automatically from the folder.
    file_name_list = os.listdir(folder_path)

    #Selectbox to choose the file.
    file_name = st.sidebar.selectbox(
        'Choose file name',
        options=file_name_list
    )
    # Translate into city name.
    city_name = file_name[8:-4].replace('_', ' ').title()

    return file_name, city_name, file_name_list

def multiselect_cities(df: pd.DataFrame) -> list:
    city_idx = st.sidebar.multiselect(
        'Select cities to view',
        options=list(df.columns),
        default=[df.columns[0]]
    )
    # Check if any cities have been selected and warn the user if not.
    if len(city_idx) == 0:
        st.error('No cities are selected.')
        st.stop()

    return city_idx

def select_year(min_year: int, max_year: int) -> st.sidebar.selectbox:
    year = st.sidebar.selectbox(
        'Choose year to view',
        options=range(min_year, max_year+1),
        index=len(range(min_year, max_year+1))-2
    )

    return year