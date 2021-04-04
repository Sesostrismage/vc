import numpy as np
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
# Get file name, city name and file name list.
file_name, city_name, file_name_list = stt.file_name_from_folder(folder_path)

# Load data into Pandas DataFrame with first row as column names and first column as index names.
df = files.braz_cities_temp(os.path.join(folder_path, file_name))

# Get all available years from the file and make it into a list.
year_list = list(df.index)
# Selectbox to choose the year.
year = st.sidebar.selectbox(
    'Choose year to view',
    options=year_list
)

# Calculate the mean per month across all years for comparison.
mean = df.mean()

# Now you have to create a figure first.
fig = go.Figure()
# Plot data from selected year with hovertext.
fig.add_trace(pt_trace.braz_cities_temp(df.loc[year], city_name, year))
# Plot all-time mean for comparison.
fig.add_trace(pt_trace.braz_cities_temp(mean, city_name, 'Mean of all years'))
# Make it pretty and informative.
fig = pt_layout.braz_cities_temp(fig, city_name, year)
# Show the figure in the Streamlit app.
st.plotly_chart(fig)