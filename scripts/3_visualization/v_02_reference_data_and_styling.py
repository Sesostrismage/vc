from pathlib import Path

import pandas as pd
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

# Choose how to display reference data.
ref_option = st.sidebar.selectbox(
    "Choose reference display",
    options=[
        "None",
        "Mean line",
        "Min-mean-max lines",
        "Min-mean-max shapes",
        "Seasons",
    ],
)

# If reference lines are shown, you can choose to have them less obtrusive.
if ref_option in ["Mean line", "Min-mean-max lines"]:
    discreet_stats = st.sidebar.checkbox("Background styling?", value=False)
else:
    discreet_stats = False


####################################################################
# Plotting.
####################################################################

# Create figure.
fig = pt_figure.braz_cities_temp_per_year(month=month)

# Case when mean line is chosen.
if ref_option == "Mean line":
    fig = pt_trace.stat_lines(fig, stat_dict, ["mean"], discreet_stats=discreet_stats)

# Case when all stat lines are chosen.
elif ref_option == "Min-mean-max lines":
    fig = pt_trace.stat_lines(
        fig, stat_dict, ["mean", "min", "max"], discreet_stats=discreet_stats
    )

# Case when all reference shapes are chosen.
elif ref_option == "Min-mean-max shapes":
    fig = pt_trace.stat_shapes(fig, stat_dict)

# Case when seasons are chosen.
elif ref_option == "Seasons":
    fig = pt_trace.season_shapes(fig, plot_df, month=month)

# Get a consistent colormap.
cmap = map_color_sequence(city_data.get_cities(selection_only=False))
# Plot all selected cities with consistent colors.
fig = pt_trace.braz_cities_temp(fig, plot_df, month, cmap=cmap)

st.plotly_chart(fig)
