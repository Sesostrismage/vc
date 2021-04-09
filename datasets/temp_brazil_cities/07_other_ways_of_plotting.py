import datetime
import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from vc.data_io import files
import vc.visuals.streamlit_tools as stt
import vc.visuals.plotly_tools.layout as pt_layout
import vc.visuals.plotly_tools.trace as pt_trace

stt.settings()

# Folder path to data files.
folder_path = r"C:/Data/temperature_time-series_for_brazilian_cities/"


# Get file name list from the folder.
file_name_list = os.listdir(folder_path)

df = pd.DataFrame()

for file_name in file_name_list:
    # Load data into Pandas DataFrame with first row as column names and first column as index names.
    city_df = files.braz_cities_temp(os.path.join(folder_path, file_name))
    city_df.columns = [idx+1 for idx, _ in enumerate(city_df.columns)]

    city_series = pd.Series(name=file_name)

    for idx, row in city_df.iterrows():
        for month in city_df.columns:
            city_series = city_series.append(
                pd.Series(
                    [row[month]],
                    index=[datetime.date(idx, month, 1)])
            )

    df = pd.concat([df, pd.DataFrame({file_name: city_series})], axis=1)

df.sort_index(inplace=True)
st.dataframe(df)