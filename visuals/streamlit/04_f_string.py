import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Folder path to data files.
folder_path = r"C:/Data/temperature_time-series_for_brazilian_cities/"
# Get file names automatically from the folder.
file_name_list = os.listdir(folder_path)

#Selectbox to choose the file.
file_name = st.sidebar.selectbox(
    'Choose file name',
    options=file_name_list
)
# Translate into city name.
city_name = file_name[8:-4].replace('_', ' ').title()

# Load data into Pandas DataFrame with first row as column names and first column as index names.
df = pd.read_csv(
    folder_path + file_name,
    header=0,
    index_col=0
)

# Remove pre-generated average columns.
df_crop = df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
# Set erroneous values to NaN so they don't disturb the results.
df_crop[df_crop > 100] = np.nan

# Get all available years from the file and make it into a list.
year_list = list(df_crop.index)
# Selectbox to choose the year.
year = st.sidebar.selectbox(
    'Choose year to view',
    options=year_list
)

# Calculate the mean per month across all years for comparison.
mean = df_crop.mean()

# Now you have to create a figure first.
fig = go.Figure()
# Create hovertext for selected year.
text_list = [
    f"{city_name} {idx.title()} {year}<br>" +
    f"{item} Deg C"
    for idx, item in df_crop.loc[year].iteritems()
]
# Plot data from selected year with hovertext.
fig.add_trace(
    go.Scatter(
        x=df_crop.columns,
        y=df_crop.loc[year],
        hoverinfo='text',
        hovertext=text_list,
        name=str(year),
        mode='lines+markers'
    )
)

# Create hovertext for all-years mean.
text_list = [
    f"{city_name} {idx.title()} all-years mean<br>" +
    f"{item} Deg C"
    for idx, item in df_crop.loc[year].iteritems()
]
# Plot all-time mean for comparison.
fig.add_trace(
    go.Scatter(
        x=df_crop.columns,
        y=mean,
        hoverinfo='text',
        hovertext=text_list,
        name='Mean of all years',
        mode='lines+markers'
    )
)

# Make it pretty and informative.
fig.update_xaxes(title={'text': 'Months'})
fig.update_yaxes(title={'text': 'Temperature [deg C]'})
fig.update_layout(
    title=f"Temperature for {city_name} in {year}",
    hovermode='x',
    height=600,
    width=1100
)
# Show the figure in the Streamlit app.
st.plotly_chart(fig)