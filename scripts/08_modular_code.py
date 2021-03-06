import os
import streamlit as st

from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData
from vc.visuals.plotly_tools import (
    figure as pt_figure,
    shapes as pt_shapes,
    trace as pt_trace,
)
from vc.visuals.colors import map_color_sequence
import vc.visuals.streamlit_tools as stt


####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
stt.settings()
# Title becomes the file name for easy reference to the presentation.
st.title(os.path.basename(__file__))
# Object with city temp data.
city_data = CitiesTempData()
# Get fixed colormap for the cities.
cmap = map_color_sequence(city_data.get_cities())


####################################################################
# User input and calculations.
####################################################################

# Get index of cities to plot.
stt.multiselect_cities(city_data)
# Choose data ranges and get data.
plot_df, stat_dict, month = stt.braz_cities_choose_data(city_data)
# Choose whether or not to have a fixed y-axis.
fixed_yaxis_bool = st.sidebar.checkbox("Fixed y-axis?", value=False)
# The the type of reference shapes to use.
ref_type = st.sidebar.selectbox(
    "Reference data type", options=["Min-max", "Summer-winter"]
)


####################################################################
# Plotting.
####################################################################

# Create figure.
fig = pt_figure.braz_cities_temp_per_year(month=month)

if ref_type == "Min-max":
    # Add shapes for min and max temperatures.
    fig = pt_shapes.minmax_temp(fig, stat_dict)
elif ref_type == "Summer-winter":
    # Add shapes or single background colours for season(s).
    fig = pt_shapes.summer_winter(fig, plot_df, stat_dict, month=month)

# Plot all selected cities.
for city_name in plot_df.columns:
    fig = pt_trace.braz_cities_temp(fig, plot_df, city_name, month, cmap)

# Apply fixed y-axis if requested.
if fixed_yaxis_bool:
    fig.update_yaxes(range=[stat_dict["min_total"], stat_dict["max_total"]])

# Show the figure in the Streamlit app.
st.plotly_chart(fig)
