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

df = files.braz_cities_temp_all(folder_path)

st.dataframe(df)