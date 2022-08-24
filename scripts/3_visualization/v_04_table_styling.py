from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from vc.definitions import ROOT_DIR
from vc.visuals.colors import get_color, map_color_sequence

####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
st.set_page_config(layout="wide")
# Title becomes the file name for easy reference to the presentation.
st.title(Path(__file__).name)
# Folder path with root of vc dirextory automatically detected.
folder_path = ROOT_DIR / "datasets" / "temp_brazil_cities" / "raw_data"
# File name list from reading the folder contents.
file_name_list = list(folder_path.iterdir())
# Empty dict to receive data.
city_dict = {}

# Loop through all file names and load the data.
for file_name in file_name_list:
    # Generate city name from file name.
    city_name = file_name.name[8:-4].replace("_", " ").title()

    # Load data into Pandas DataFrame with first row as column names and first column as index names.
    df = pd.read_csv(folder_path / file_name, header=0, index_col=0)
    # Remove pre-generated average columns.
    df_crop = df.drop(["D-J-F", "M-A-M", "J-J-A", "S-O-N", "metANN"], axis=1)
    # Set erroneous values to NaN so they don't disturb the results.
    df_crop[df_crop > 100] = np.nan
    # Insert dataframe into file dict.
    city_dict[city_name] = df_crop

# Get fixed colormap.
cmap = map_color_sequence(city_dict.keys())


####################################################################
# User input and calculations.
####################################################################

# Multi-select which cities to plot.
selected_cities_list = st.sidebar.multiselect(
    "Select cities to view",
    options=sorted(list(city_dict.keys())),
    default=sorted(list(city_dict.keys())),
)
# Check if any cities have been selected and warn the user if not.
if len(selected_cities_list) == 0:
    st.error("No cities are selected.")
    st.stop()

# Find earliest and latest years that have data.
min_year = 2010
max_year = 2010

for city in selected_cities_list:
    if city in city_dict:
        min_year = min(min_year, city_dict[city].index[0])
        max_year = max(max_year, city_dict[city].index[-1])

# Get all available years from the file and make it into a list.
year_list = range(min_year, max_year + 1)
# Selectbox to choose the year.
year = st.sidebar.selectbox(
    "Choose year to view", options=year_list, index=len(year_list) - 1
)

# Choose hovermode.
hovermode = st.sidebar.selectbox("Choose hovermode", options=["x", "closest"])

# Calculate statistical values.
stat_df = pd.DataFrame()

for city_name in city_dict:
    if year in city_dict[city_name].index:
        # Build stat df.
        stat_df = pd.concat(
            [stat_df, pd.DataFrame({city_name: city_dict[city_name].loc[year]})], axis=1
        )

mean_series = stat_df.mean(axis=1)
min_series = stat_df.min(axis=1)
max_series = stat_df.max(axis=1)


####################################################################
# Plotting.
####################################################################

# Create figure.
fig = go.Figure()
# Set up the layout.
fig.update_xaxes(title="Datetime")
fig.update_yaxes(title="Temperature [deg C]")
fig.update_layout(
    title=f"Temperature for brazilian cities in {year}",
    hovermode=hovermode,
    height=800,
    width=1400,
    plot_bgcolor="#ffffff",
)
# Dict to set better axis properties.
axis_dict = {
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
# Apply to both axes.
fig.update_xaxes(axis_dict)
fig.update_yaxes(axis_dict)

# Handle missing data.
# Find indices where the series doesn't have null values.
valid_idx = min_series.notnull()
# Use those indices to put together x and y value lists.
x_part = [col for idx, col in enumerate(df_crop.columns) if valid_idx[idx]]
x = x_part + list(reversed(x_part))

y_mean_part = [val for idx, val in enumerate(mean_series) if valid_idx[idx]]
y_part = [val for idx, val in enumerate(min_series) if valid_idx[idx]]
y_min = y_part + list(reversed(y_mean_part))
y_part = [val for idx, val in enumerate(max_series) if valid_idx[idx]]
y_max = y_part + list(reversed(y_mean_part))

# Plot the min and max areas as filled polygons.
fig.add_trace(
    go.Scatter(
        x=x,
        y=y_min,
        fill="toself",
        mode="none",
        marker={"color": get_color("temperature", "min")},
        showlegend=False,
        hoverinfo="none",
    )
)
fig.add_trace(
    go.Scatter(
        x=x,
        y=y_max,
        fill="toself",
        mode="none",
        marker={"color": get_color("temperature", "max")},
        showlegend=False,
        hoverinfo="none",
    )
)

# Print all selected cities.
for city_name in (city for city in city_dict if city in selected_cities_list):
    # Plot data from selected year if present.
    if year in city_dict[city_name].index:
        # Create hovertext.
        text_list = [
            f"{city_name}, {idx.title()} {year}<br>" + f"{item} deg C"
            for idx, item in city_dict[city_name].loc[year].iteritems()
        ]

        fig.add_trace(
            go.Scattergl(
                x=city_dict[city_name].columns,
                y=city_dict[city_name].loc[year],
                hoverinfo="text",
                hovertext=text_list,
                line={"color": cmap[city_name]},
                name=city_name,
            )
        )

# Show the figure in the Streamlit app.
st.plotly_chart(fig)
