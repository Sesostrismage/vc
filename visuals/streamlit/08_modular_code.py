import datetime
import plotly.graph_objects as go
import numpy as np
import os
import pandas as pd
import streamlit as st

from vc.data_io import files
from vc.data_treat.maps import month_dict
from vc.visuals.colors import get_color, map_color_sequence
import vc.visuals.streamlit_tools as stt


####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
st.set_page_config(layout='wide')
st.title(os.path.basename(__file__))

# DataFrame with city data.
df = files.braz_cities_temp()
# Get fixed colormap.
cmap = map_color_sequence(df.columns)


####################################################################
# User input and calculations.
####################################################################

# Get index of cities to plot.
city_idx = stt.multiselect_cities(df)

city_df = df[city_idx]
notnull_idx = city_df.notnull().all(axis=1)

# Choose whether or not to only show a single month per year.
month_bool = st.sidebar.checkbox(
    'Filter by month?',
    value=False
)
if month_bool:
    month = st.sidebar.select_slider(
        'Choose month',
        options=range(1, 13),
        format_func=month_dict.get
    )

    year_list = sorted(set([dt.year for dt in df.loc[notnull_idx].index]))

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
    plot_df = df.loc[dt_idx & notnull_idx, city_idx]

else:
    date_start = st.sidebar.select_slider(
        'Start date',
        options=list(city_df.index)
    )

    date_end = st.sidebar.select_slider(
        'End date',
        options=list(city_df.loc[date_start:].index),
        value=list(city_df.index)[-1]
    )

    dt_idx = (date_start <= df.index) & (df.index <= date_end)
    plot_df = df.loc[dt_idx & notnull_idx, city_idx]

min_series = df.loc[dt_idx].min(axis=1)
max_series = df.loc[dt_idx].max(axis=1)
mean_series = df.loc[dt_idx].mean(axis=1)

# Choose whether or not to have a fixed y-axis.
fixed_yaxis_bool = st.sidebar.checkbox(
    'Fixed y-axis?',
    value=False
)


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
for city_name in plot_df.columns:
    if month_bool:
        text_list = [
            f"{city_name} - {month_dict[month]} {idx.year}<br>" +
            f"{row[city_name]} deg C"
            for idx, row in plot_df.iterrows()
        ]
    else:
        text_list = [
            f"{city_name} - {idx}<br>" +
            f"{row[city_name]} deg C"
            for idx, row in plot_df.iterrows()
        ]

    fig.add_trace(go.Scattergl(
        x=plot_df.index,
        y=plot_df[city_name],
        hoverinfo='text',
        hovertext=text_list,
        line={'color': cmap[city_name]},
        name=city_name
    ))

if month_bool:
    title = f"Temperature for brazilian cities in {month_dict[month]}"
else:
    title = f"Temperature for brazilian cities"

# Set up the layout.
fig.update_xaxes(title='Datetime')
fig.update_yaxes(title='Temperature [deg C]')

if fixed_yaxis_bool:
    fig.update_yaxes(range=[df.min().min(), df.max().max()])

fig.update_layout(
    title=title,
    hovermode='x',
    height=600,
    width=1100
)
# Show the figure in the Streamlit app.
st.plotly_chart(fig)