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

df, stat_dict = city_data.get_data()

corr_df = df.corr()

####################################################################
# User input and calculations.
####################################################################

builtin_colorscale_bool = st.sidebar.checkbox(
    'Built-in colorscale?',
    value=True
)

if builtin_colorscale_bool:
    colorscale = stt.cmap_plotly()
else:
    colorscale = [[0, 'rgb(255, 255, 0)'], [0.5, 'rgb(128, 128, 128)'], [1, 'rgb(0, 255, 255)']]

fixed_color_range_bool = st.sidebar.checkbox(
    'Fixed color range?'
)

if fixed_color_range_bool:
    zmin = -1
    zmax = 1
else:
    zmin = corr_df.min().min()
    zmax = corr_df.max().max()


####################################################################
# Plotting.
####################################################################

fig = pt_figure.corr_map()
fig.add_trace(
    go.Heatmap(
        x=df.columns,
        y=df.columns,
        z=corr_df,
        colorscale=colorscale,
        zmin=zmin,
        zmax=zmax
    )
)
st.plotly_chart(fig)