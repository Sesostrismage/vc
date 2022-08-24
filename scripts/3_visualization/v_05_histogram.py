from pathlib import Path

import plotly.graph_objects as go
import streamlit as st
import vc.visuals.streamlit_tools as stt
from plotly.subplots import make_subplots
from vc.data_treat.maps import Month
from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData
from vc.visuals.colors import map_color_sequence
from vc.visuals.plotly_tools import figure as pt_figure
from vc.visuals.plotly_tools import hovertext as pt_hover

####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
stt.settings()
# Title becomes the file name for easy reference to the presentation.
st.title(Path(__file__).name)
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
fixed_yaxis_bool = st.sidebar.checkbox("Fixed y-axis?", value=True)


####################################################################
# Plotting.
####################################################################

# Create figure.
fig = make_subplots(
    rows=1, cols=2, shared_yaxes=True, column_widths=[0.8, 0.2], horizontal_spacing=0.01
)
# The layout has to be constructed manually, since setting this with subplots
# Needs explicit subplot references, so the existing modular code can't be used.
if month is not None:
    title = f"Temperature for brazilian cities in {Month(month).name}"
else:
    title = f"Temperature for brazilian cities"

fig.update_layout(
    height=pt_figure.height_standard,
    width=pt_figure.width_standard,
    title=title,
    plot_bgcolor="#ffffff",
)
fig.update_xaxes(title={"text": "Months"}, row=1, col=1)
fig.update_xaxes(title={"text": "Counts"}, row=1, col=2)
fig.update_yaxes(title={"text": "Temperature [deg C]"}, row=1, col=1)

axis_dict_col1 = {
    # Move ticks outside the plot.
    "ticks": "outside",
    # Show plot borders with these four settings.
    "showline": True,
    "linewidth": 2,
    "linecolor": "black",
    "mirror": True,
    # Remove gridlines in the plot.
    "showgrid": False,
}
# Apply to both axes in col 1.
fig.update_xaxes(axis_dict_col1, row=1, col=1)
fig.update_xaxes(axis_dict_col1, row=1, col=2)
axis_dict_col2 = {
    # Remove ticks.
    "ticks": "",
    # Show plot borders with these four settings.
    "showline": True,
    "linewidth": 2,
    "linecolor": "black",
    "mirror": True,
    # Remove gridlines in the plot.
    "showgrid": False,
}
fig.update_yaxes(axis_dict_col2, row=1, col=1)
fig.update_yaxes(axis_dict_col2, row=1, col=2)
fig.update_layout(barmode="stack")


# Plot all selected cities.
for city_name in plot_df.columns:
    text_list = pt_hover.braz_cities_temp(plot_df, city_name, month)

    fig.add_trace(
        go.Scattergl(
            x=plot_df.index,
            y=plot_df[city_name],
            hoverinfo="text",
            hovertext=text_list,
            line={"color": cmap[city_name]},
            name=city_name,
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Histogram(
            y=plot_df[city_name],
            marker_color=cmap[city_name],
            name=city_name,
            showlegend=False,
        ),
        row=1,
        col=2,
    )

# Apply fixed y-axis if requested.
if fixed_yaxis_bool:
    fig.update_yaxes(range=[stat_dict["min_total"], stat_dict["max_total"]])

# Show the figure in the Streamlit app.
st.plotly_chart(fig)
