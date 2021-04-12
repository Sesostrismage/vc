import os

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

def multiselect_cities(data_dict: dict) -> list:
    selected_cities_list = st.sidebar.multiselect(
        'Select cities to view',
        options=list(data_dict.keys()),
        default=list(data_dict.keys())
    )

    if len(selected_cities_list) == 0:
        st.error('No cities are selected.')
        st.stop()

    return selected_cities_list