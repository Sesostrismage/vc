import datetime
import plotly.graph_objects as go
import numpy as np
import os
import pandas as pd
import streamlit as st

from vc.definitions import ROOT_DIR
from vc.visuals.colors import get_color, map_color_sequence


####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
st.set_page_config(layout='wide')
# Folder path with root of vc dirextory automatically detected.
folder_path = os.path.join(ROOT_DIR, 'datasets', 'temp_brazil_cities', 'raw_data')
# File name list from reading the folder contents.
file_name_list = os.listdir(folder_path)
# Empty dataframe to receive data.
df = pd.DataFrame()

# Loop through all file names and load the data.
for file_name in file_name_list:
    # Generate city name from file name.
    city_name = file_name[8:-4].replace('_', ' ').title()

    # Load data into Pandas DataFrame with first row as column names and first column as index names.
    city_df = pd.read_csv(
        os.path.join(folder_path, file_name),
        header=0,
        index_col=0
    )
    # Remove pre-generated average columns.
    city_df = city_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
    # Set erroneous values to NaN so they don't disturb the results.
    city_df[city_df > 100] = np.nan

    city_df.columns = [idx+1 for idx, _ in enumerate(city_df.columns)]
    stacked_df = city_df.stack()
    stacked_df.index = [datetime.date(i[0], i[1], 1) for i in stacked_df.index]
    df = pd.concat([df, pd.DataFrame({city_name: stacked_df})], axis=1)

df.sort_index(inplace=True)

# Get fixed colormap.
cmap = map_color_sequence(df.columns)


####################################################################
# User input and calculations.
####################################################################

# Multi-select which cities to plot.
city_idx = st.sidebar.multiselect(
    'Select cities to view',
    options=list(df.columns),
    default=[df.columns[0]]
)
# Check if any cities have been selected and warn the user if not.
if len(city_idx) == 0:
    st.error('No cities are selected.')
    st.stop()

city_slice_df = df[city_idx]
na_idx = city_slice_df.isnull().all(axis=1)

# Choose whether or not to only show a single month per year.
month_bool = st.sidebar.checkbox(
    'Filter by month?',
    value=False
)
if month_bool:
    month = st.sidebar.slider(
        'Choose month',
        min_value=1,
        max_value=12,
        step=1
    )

    year_list = sorted(set([dt.year for dt in df.loc[~na_idx].index]))

    year_start = st.sidebar.slider(
        'Start year',
        min_value=year_list[0],
        max_value=year_list[-1]
    )

    year_end = st.sidebar.slider(
        'End year',
        min_value=year_start,
        max_value=year_list[-1],
        value=year_list[-1]
    )

    dt_idx = [True if ((year_start <= dt.year <= year_end) and (dt.month == month)) else False for dt in df.index]
    dt_city_slice_df = df.loc[dt_idx & ~na_idx, city_idx]
    st.dataframe(dt_city_slice_df)

else:
    date_start = st.sidebar.select_slider(
        'Start date',
        options=list(city_slice_df.index)
    )

    date_end = st.sidebar.select_slider(
        'End date',
        options=list(city_slice_df.loc[date_start:].index),
        value=list(city_slice_df.index)[-1]
    )

    dt_idx = (date_start <= df.index) & (df.index <= date_end)
    dt_city_slice_df = df.loc[dt_idx & ~na_idx, city_idx]

min_series = df.loc[dt_idx].min(axis=1)
max_series = df.loc[dt_idx].max(axis=1)
mean_series = df.loc[dt_idx].mean(axis=1)


####################################################################
# Plotting.
####################################################################

# Create figure.
fig = go.Figure()

# Handle missing data.
# Find indices where the series doesn't have null values.
valid_idx = min_series.notnull()
# Use those indices to put together x and y value lists.
x_part = list(min_series[valid_idx].index)
x = x_part + list(reversed(x_part))

y_mean_part = [val for idx, val in enumerate(mean_series) if valid_idx[idx]]

y_part = [val for idx, val in enumerate(min_series) if valid_idx[idx]]
y_min = y_part + list(reversed(y_mean_part))
y_part = [val for idx, val in enumerate(max_series) if valid_idx[idx]]
y_max = y_part + list(reversed(y_mean_part))

# Plot the min and max areas as filled polygons.
fig.add_trace(
    go.Scatter(
        x=x,
        y=y_min,
        fill='toself',
        mode='none',
        marker={'color': get_color('temperature', 'min')},
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
        marker={'color': get_color('temperature', 'max')},
        showlegend=False,
        hoverinfo='none'
    )
)

# Plot all selected cities.
for city_name in dt_city_slice_df.columns:
        text_list = ['So empty...' for idx, row in dt_city_slice_df.iterrows()]

        fig.add_trace(go.Scattergl(
            x=dt_city_slice_df.index,
            y=dt_city_slice_df[city_name],
            hoverinfo='text',
            hovertext=text_list,
            line={'color': cmap[city_name]},
            name=city_name
        ))

# Set up the layout.
fig.update_xaxes(title='Datetime')
fig.update_yaxes(title='Temperature [deg C]')
fig.update_layout(
    title=f"Temperature for brazilian cities",
    hovermode='x',
    height=600,
    width=1100
)
# Show the figure in the Streamlit app.
st.plotly_chart(fig)