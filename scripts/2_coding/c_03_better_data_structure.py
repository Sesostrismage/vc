import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from vc.data_treat.maps import Month
from vc.definitions import ROOT_DIR


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
# Empty dataframe to receive data.
df = pd.DataFrame()

# Loop through all file names and load the data.
for file_name in file_name_list:
    # Generate city name from file name.
    city_name = file_name.name[8:-4].replace("_", " ").title()

    # Load data into Pandas DataFrame with first row as column names and first column as index names.
    city_df = pd.read_csv(folder_path / file_name, header=0, index_col=0)
    # Remove pre-generated average columns.
    city_df = city_df.drop(["D-J-F", "M-A-M", "J-J-A", "S-O-N", "metANN"], axis=1)
    # Set erroneous values to NaN so they don't disturb the results.
    city_df[city_df > 100] = np.nan

    city_df.columns = [idx + 1 for idx, _ in enumerate(city_df.columns)]
    stacked_df = city_df.stack()
    stacked_df.index = [datetime.date(i[0], i[1], 1) for i in stacked_df.index]
    df = pd.concat([df, pd.DataFrame({city_name: stacked_df})], axis=1)

df.sort_index(inplace=True)


####################################################################
# Old data structure for comparison.
####################################################################

# Empty dict to receive data.
city_dict = {}

# Loop through all file names and load the data.
for file_name in file_name_list:
    # Generate city name from file name.
    city_name = file_name.name[8:-4].replace("_", " ").title()

    # Load data into Pandas DataFrame with first row as column names and first column as index names.
    temp_df = pd.read_csv(folder_path / file_name, header=0, index_col=0)
    # Remove pre-generated average columns.
    df_crop = temp_df.drop(["D-J-F", "M-A-M", "J-J-A", "S-O-N", "metANN"], axis=1)
    # Set erroneous values to NaN so they don't disturb the results.
    df_crop[df_crop > 100] = np.nan
    # Insert dataframe into file dict.
    city_dict[city_name] = df_crop


####################################################################
# User input and calculations.
####################################################################

# Multi-select which cities to plot.
city_idx = st.sidebar.multiselect(
    "Select cities to view", options=list(df.columns), default=list(df.columns)
)
# Check if any cities have been selected and warn the user if not.
if len(city_idx) == 0:
    st.error("No cities are selected.")
    st.stop()

# Keep only selected cities.
city_slice_df = df[city_idx]
# Create an index of all places where the data is null for all selected cities.
na_idx = city_slice_df.isnull().all(axis=1)

# Choose whether or not to only show a single month per year.
month_bool = st.sidebar.checkbox("Filter by month?", value=False)
# If filtering by month:
if month_bool:
    # Choose which month.
    month = st.sidebar.select_slider(
        "Choose month", options=range(1, 13), format_func=lambda x: Month(x).name
    )
    # Get a list of all usable years in the data.
    year_list = sorted(set([dt.year for dt in df.loc[~na_idx].index]))
    # Choose start and end year.
    year_start = st.sidebar.slider(
        "Start year", min_value=year_list[0], max_value=year_list[-1]
    )

    year_end = st.sidebar.slider(
        "End year", min_value=year_start, max_value=year_list[-1], value=year_list[-1]
    )
    # Create an index of all dates fulfilling the requirements.
    dt_idx = [
        True if ((year_start <= dt.year <= year_end) and (dt.month == month)) else False
        for dt in df.index
    ]
    # Create the plot DataFrame.
    plot_df = df.loc[dt_idx & ~na_idx, city_idx]

# If no month is chosen:
else:
    # Choose normal start and end date.
    date_start = st.sidebar.select_slider(
        "Start date", options=list(city_slice_df.index)
    )

    date_end = st.sidebar.select_slider(
        "End date",
        options=list(city_slice_df.loc[date_start:].index),
        value=list(city_slice_df.index)[-1],
    )
    # Create date index and slice the data.
    dt_idx = (date_start <= df.index) & (df.index <= date_end)
    plot_df = df.loc[dt_idx & ~na_idx, city_idx]

# Choose whether or not to show the mean value line.
show_mean_bool = st.sidebar.checkbox("Show mean value?")

# If yes, build the mean series.
if show_mean_bool:
    # Create statistical series.
    mean_series = df.loc[dt_idx].mean(axis=1)


####################################################################
# Show old and new data structures.
####################################################################

st.write("Old data structure (one city)")
st.dataframe(city_dict["Belem"].style.highlight_null(null_color="grey"))

st.write("New data structure (all cities)")
st.dataframe(df.style.highlight_null(null_color="grey"))

####################################################################
# Plotting.
####################################################################

# Create figure.
fig = go.Figure()
# If month is chosen, add it to the plot title.
if month_bool:
    title = f"Temperature for brazilian cities in {Month(month).name}"
else:
    title = f"Temperature for brazilian cities"

# Layout.
fig.update_xaxes(title="Datetime")
fig.update_yaxes(title="Temperature [deg C]")
fig.update_layout(
    title=title, hovermode="x", height=800, width=1400, plot_bgcolor="#ffffff"
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


# Plot all selected cities.
for city_name in plot_df.columns:
    fig.add_trace(
        go.Scattergl(
            x=plot_df.index,
            y=plot_df[city_name],
            name=city_name,
        )
    )

# Plot statistical series if chosen.
if show_mean_bool:
    fig.add_trace(go.Scatter(x=mean_series.index, y=mean_series, name="All-city mean"))

# Show the figure in the Streamlit app.
st.plotly_chart(fig)
