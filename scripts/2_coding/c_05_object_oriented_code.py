from pathlib import Path

import streamlit as st
import vc.visuals.plotly_tools.figure as pt_figure
import vc.visuals.plotly_tools.trace as pt_trace
import vc.visuals.streamlit_tools as stt
from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData

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


####################################################################
# Plotting.
####################################################################

# Create figure.
fig = pt_figure.braz_cities_temp_per_year(month=month)
# Plot all selected cities.
fig = pt_trace.braz_cities_temp(fig, plot_df, month)
# Plot statistical series if chosen.
if show_mean_bool:
    pt_trace.stat_lines(fig, stat_dict, ["mean"])
# Show the figure in the Streamlit app.
st.plotly_chart(fig)
