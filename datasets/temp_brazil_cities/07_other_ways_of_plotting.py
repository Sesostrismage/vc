import datetime
import os
import pandas as pd
from plotly.figure_factory import create_scatterplotmatrix
import plotly.graph_objects as go
import streamlit as st

from vc.data_io import files
import vc.visuals.streamlit_tools as stt
import vc.visuals.plotly_tools.hovertext as pt_hover
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
    options=list(df.index),
    value=df.index[-1]
)

if date_start >= date_end:
    st.error('Date start is greater than date end!')
    st.stop()

plot_mode = st.sidebar.selectbox(
    'Choose display mode',
    options=['Line plot', 'Scatter matrix', 'Map plot']
)

range_df = df.loc[date_start:date_end]

city_series = range_df[city]



if plot_mode == 'Line plot':
    fig = go.Figure()
    fig = pt_trace.minmax_shapes(fig, range_df, axis=1)

    text_list = pt_hover.braz_cities_temp(city_series, city, '', ref_df=range_df, axis=1)

    # Plot data from selected date range with hovertext.
    fig.add_trace(
        go.Scattergl(
            x=city_series.index,
            y=city_series,
            hoverinfo='text',
            hovertext=text_list,
            line={'color': 'black'},
            showlegend=False
        )
    )
    fig = pt_layout.braz_cities_temp_all(fig, city_series)

elif plot_mode == 'Scatter matrix':
    fig = create_scatterplotmatrix(
        range_df[range_df.columns[:4]],
        height=pt_layout.height_standard,
        width=pt_layout.width_standard
    )
    fig.update_xaxes(matches='x')
    fig.update_yaxes(matches='y')

st.plotly_chart(fig)
