import os

import streamlit as st

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