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

city = st.sidebar.selectbox(
    'Choose city',
    options=df.columns
)

date_start = st.sidebar.select_slider(
    'Start date',
    options=list(df.index)
)

date_end = st.sidebar.select_slider(
    'End date',
    options=list(df.index)
)

if date_start >= date_end:
    st.error('Date start is greater than date end!')
    st.stop()

range_df = df.loc[date_start:date_end]

city_series = range_df[city]

fig = go.Figure()

# Plot data from selected year with hovertext.
fig.add_trace(
    go.Scattergl(
        x=city_series.index,
        y=city_series
    )
)
st.plotly_chart(fig)