from pathlib import Path

import streamlit as st
import vc.data_treat.cities_data_treat as cdt
import vc.visuals.plotly_tools.figure as pt_figure
import vc.visuals.plotly_tools.trace as pt_trace
import vc.visuals.streamlit_tools as stt
from vc.data_io import files
from vc.data_treat.maps import Month

####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
stt.settings()
# Title becomes the file name for easy reference to the presentation.
st.title(Path(__file__).name)
# Load data.
df = files.braz_cities_temp()


####################################################################
# User input and calculations.
####################################################################

# Multi-select which cities to plot.
city_idx = stt.multiselect_cities_old_style(df)
# Keep only selected cities.
city_slice_df = df[city_idx]

# Choose whether or not to only show a single month per year.
month_bool = st.sidebar.checkbox("Filter by month?", value=False)

# If filtering by month:
if month_bool:
    # Choose which month.
    month = st.sidebar.select_slider(
        "Choose month", options=range(1, 13), format_func=lambda x: Month(x).name
    )
    plot_df = cdt.filter_cities_data_by_month(city_slice_df, city_idx, month)

# If no month is chosen:
else:
    month = None

    # Choose normal start and end date.
    date_start = st.sidebar.select_slider(
        "Start date", options=list(city_slice_df.index)
    )
    date_end = st.sidebar.select_slider(
        "End date",
        options=list(city_slice_df.loc[date_start:].index),
        value=list(city_slice_df.index)[-1],
    )
    # Create an index of all places where the data is null for all selected cities.
    na_idx = city_slice_df.isnull().all(axis=1)
    # Create date index and slice the data.
    dt_idx = (date_start <= df.index) & (df.index <= date_end)
    plot_df = df.loc[dt_idx & ~na_idx, city_idx]

# Choose whether or not to show the mean value line.
show_mean_bool = st.sidebar.checkbox("Show mean value?")

# If yes, build the mean series.
if show_mean_bool:
    # Create statistical series.
    mean_series = plot_df.mean(axis=1)


####################################################################
# Plotting.
####################################################################

# Create figure.
fig = pt_figure.braz_cities_temp_per_year(month=month)
# Plot all selected cities.
fig = pt_trace.braz_cities_temp_old_style(fig, plot_df)
# Plot statistical series if chosen.
if show_mean_bool:
    pt_trace.mean_line_old_style(fig, mean_series)
# Show the figure in the Streamlit app.
st.plotly_chart(fig)
