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
# Get all data for the correlation calculation.
df, stat_dict = city_data.get_data()
# Calculate the correlation matrix.
corr_df = df.corr()


####################################################################
# User input and calculations.
####################################################################

# Choose whether or not to use a built-in colorscale.
builtin_colorscale_bool = st.sidebar.checkbox(
    'Built-in colorscale?',
    value=True
)
# If yes, dropdown with all Plotly colorscales.
if builtin_colorscale_bool:
    colorscale = stt.cmap_plotly()
# Else home-made colorscale with neutral middle colour.
else:
    colorscale = [[0, 'rgb(255, 255, 0)'], [0.5, 'rgb(128, 128, 128)'], [1, 'rgb(0, 255, 255)']]

# Choose whether to fix the color range from -1 to 1.
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

# Plot the correlation matrix.
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