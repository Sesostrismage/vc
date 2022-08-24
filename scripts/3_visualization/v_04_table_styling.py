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

plot_df, _ = city_data.get_data(year_start=1975, year_end=1975)
precision_df = plot_df.style.format(precision=2)

styling = st.sidebar.radio("Choose styling", options=["None", "NaNs", "Color gradient"])

if styling == "None":
    final_df = precision_df
elif styling == "NaNs":
    final_df = precision_df.highlight_null(null_color="grey")
elif styling == "Color gradient":
    final_df = precision_df.background_gradient(cmap="coolwarm")

st.dataframe(final_df)
