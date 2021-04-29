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
st.set_page_config(layout='wide')
# Title becomes the file name for easy reference to the presentation.
st.title(os.path.basename(__file__))
# Object with city temp data.
city_data = CitiesTempData()

city_data = CitiesTempData()
df, stat_dict = city_data.get_data()


####################################################################
# User input and calculations.
####################################################################

colorscale = stt.cmap_plotly()


####################################################################
# Plotting.
####################################################################

fig = pt_figure.heatmap_fig()
fig.add_trace(
    go.Heatmap(
        x=df.columns,
        y=df.index,
        z=df,
        colorscale=colorscale
    )
)
st.plotly_chart(fig)