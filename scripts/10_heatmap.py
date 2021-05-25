import os
import plotly.graph_objects as go
import streamlit as st

from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData
import vc.visuals.plotly_tools.figure as pt_figure
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
# Get all data for the heatmap plot.
df, stat_dict = city_data.get_data()


####################################################################
# Plotting.
####################################################################

# Plot the data in a heatmap.
fig = pt_figure.heatmap()
fig.add_trace(
    go.Heatmap(
        x=df.columns,
        y=df.index,
        z=df,
        colorscale='Jet'
    )
)
st.plotly_chart(fig)