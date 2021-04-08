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

ref_option = st.sidebar.selectbox(
    'Choose reference display',
    options=['Mean line', 'Min-mean-max lines', 'Min-mean-max shapes']
)

if ref_option in ['Mean line', 'Min-mean-max lines']:
    background_bool = st.sidebar.checkbox(
        'Background styling?',
        value=False
    )
else:
    background_bool = False

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

# Now you have to create a figure first.
fig = go.Figure()

if ref_option == 'Min-mean-max shapes':
    x = list(df.columns) + list(df.columns[::-1])
    y_min = list(df.min()) + list(df.mean()[::-1])
    y_max = list(df.max()) + list(df.mean()[::-1])

    t = go.Scatter(
        x=x,
        y=y_min,
        fill='toself',
        mode='none',
        showlegend=False,
        hoverinfo='none'
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_min,
            fill='toself',
            mode='none',
            marker={'color': 'blue'},
            showlegend=False,
            hoverinfo='none'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_max,
            fill='toself',
            mode='none',
            marker={'color': 'red'},
            showlegend=False,
            hoverinfo='none'
        )
    )

# Plot data from selected year with hovertext.
fig.add_trace(pt_trace.braz_cities_temp_v2(
    df.loc[year],
    city_name,
    year,
    'temperature',
    'value'
))

if ref_option in ['Mean line', 'Min-mean-max lines']:
    # Calculate the mean per month across all years for comparison.
    mean = df.mean()
    # Plot all-time mean for comparison.
    fig.add_trace(pt_trace.braz_cities_temp_v2(
        mean,
        city_name,
        'Mean of all years',
        'temperature',
        'reference',
        background=background_bool
    ))

    if ref_option == 'Min-mean-max lines':
        # Calculate the mean per month across all years for comparison.
        min = df.min()
        # Plot all-time min for comparison.
        fig.add_trace(pt_trace.braz_cities_temp_v2(
            min,
            city_name,
            'Min of all years',
            'temperature',
            'min',
            background=background_bool
        ))

        # Calculate the mean per month across all years for comparison.
        max = df.max()
        # Plot all-time max for comparison.
        fig.add_trace(pt_trace.braz_cities_temp_v2(
            max,
            city_name,
            'Min of all years',
            'temperature',
            'max',
            background=background_bool
        ))

# Make it pretty and informative.
fig = pt_layout.braz_cities_temp(fig, city_name, year)
# Show the figure in the Streamlit app.
st.plotly_chart(fig)