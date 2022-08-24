from pathlib import Path

import streamlit as st
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

# Choose whether or not to show the mean value line.
show_mean_bool = st.sidebar.checkbox("Show mean value?")

# # If yes, build the mean series.
if show_mean_bool:
    # Create statistical series.
    mean_series = plot_df.mean(axis=1)


####################################################################
# Plotting.
####################################################################

# Create figure.
fig = pt_figure.braz_cities_temp_per_year(month=month)
# Get a consistent colormap.
cmap = map_color_sequence(city_data.get_cities(selection_only=False))
# Plot all selected cities with consistent colors.
fig = pt_trace.braz_cities_temp(fig, city_data, month, cmap=cmap)
# Plot statistical series if chosen.
if show_mean_bool:
    pt_trace.mean_series(fig, mean_series)
# Show the figure in the Streamlit app.
st.plotly_chart(fig)
