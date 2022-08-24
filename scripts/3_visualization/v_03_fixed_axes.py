from pathlib import Path

import pandas as pd
import streamlit as st
import vc.data_treat.cities_data_treat as cdt
import vc.visuals.plotly_tools.figure as pt_figure
import vc.visuals.plotly_tools.trace as pt_trace
import vc.visuals.streamlit_tools as stt
from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData
from vc.visuals.colors import map_color_sequence

####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
stt.settings()
# Title becomes the file name for easy reference to the presentation.
st.title(Path(__file__).name)
# Object with city temp data.
city_data = CitiesTempData()


####################################################################
# User input and calculations.
####################################################################

# Multi-select which cities to plot.
stt.multiselect_cities(city_data)

plot_df, stat_dict, month = stt.braz_cities_choose_data(city_data)

show_stat_shapes = st.sidebar.checkbox("Show stat shapes?")

# Choose if you want a fixed x-axis.
fixed_x_axis = st.sidebar.checkbox("Fixed x-axis?")

# Choose if you want a fixed y-axis.
fixed_y_axis = st.sidebar.checkbox("Fixed y-axis?")


####################################################################
# Plotting.
####################################################################

# Create figure.
fig = pt_figure.braz_cities_temp_per_year(month=month)

if show_stat_shapes:
    # Plot stat shapes.
    fig = pt_trace.stat_shapes(fig, stat_dict)

# Get a consistent colormap.
cmap = map_color_sequence(city_data.get_cities(selection_only=False))
# Plot all selected cities with consistent colors.
fig = pt_trace.braz_cities_temp(fig, plot_df, month, cmap=cmap)

if fixed_x_axis:
    x_min, x_max = cdt.get_x_axis_extremes(city_data)
    fig.update_xaxes(range=[x_min, x_max])

if fixed_y_axis:
    fig.update_yaxes(range=[stat_dict["min_total"], stat_dict["max_total"]])

st.plotly_chart(fig)
