import plotly.graph_objects as go
import numpy as np
import os
import pandas as pd
import streamlit as st

from vc.definitions import ROOT_DIR


####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
st.set_page_config(layout='wide')
# Folder path with root of vc dirextory automatically detected.
folder_path = os.path.join(ROOT_DIR, 'datasets', 'temp_brazil_cities', 'raw_data')
# File name list from reading the folder contents.
file_name_list = os.listdir(folder_path)
# Empty dict to receive data.
city_dict = {}

# Loop through all file names and load the data.
for file_name in file_name_list:
    # Generate city name from file name.
    city_name = file_name[8:-4].replace('_', ' ').title()

    # Load data into Pandas DataFrame with first row as column names and first column as index names.
    df = pd.read_csv(
        os.path.join(folder_path, file_name),
        header=0,
        index_col=0
    )
    # Remove pre-generated average columns.
    df_crop = df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
    # Set erroneous values to NaN so they don't disturb the results.
    df_crop[df_crop > 100] = np.nan
    # Insert dataframe into file dict.
    city_dict[city_name] = df_crop


####################################################################
# User input and calculations.
####################################################################

selected_cities_list = st.sidebar.multiselect(
    'Select cities to view',
    options=sorted(list(city_dict.keys())),
    default=sorted(list(city_dict.keys()))
)

if len(selected_cities_list) == 0:
    st.error('No cities are selected.')
    st.stop()

# Find earliest and latest years that have data.
min_year = 2010
max_year = 2010

for city in selected_cities_list:
    if city in city_dict:
        min_year = min(min_year, city_dict[city].index[0])
        max_year = max(max_year, city_dict[city].index[-1])

# Get all available years from the file and make it into a list.
year_list = range(min_year, max_year+1)
# Selectbox to choose the year.
year = st.sidebar.selectbox(
    'Choose year to view',
    options=year_list,
    index=len(year_list)-1
)

show_mean_bool = st.sidebar.checkbox(
    'Show mean value?'
)

if show_mean_bool:
    mean_df = pd.DataFrame()

    for file_name in city_dict:
        if year in city_dict[file_name].index:
            #Build mean df.
            mean_df = pd.concat([mean_df, pd.DataFrame({file_name: city_dict[file_name].loc[year]})], axis=1)

    mean_series = mean_df.mean(axis=1)


####################################################################
# PLotting.
####################################################################

fig = go.Figure()

for file_name in city_dict:
    if year in city_dict[file_name].index:
        # Plot data from selected year if present.
        fig.add_trace(go.Scattergl(
            x=city_dict[file_name].columns, y=city_dict[file_name].loc[year], name=file_name
        ))

if show_mean_bool:
    fig.add_trace(go.Scattergl(
        x=mean_series.index, y=mean_series, name='All-city mean'
    ))

fig.update_xaxes(title='Datetime')
fig.update_yaxes(title='Temperature [deg C]')
fig.update_layout(
    title='Temperature for brazilian cities in ' + str(year),
    hovermode='x',
    height=600,
    width=1100
)
# Show the figure in the Streamlit app.
st.plotly_chart(fig)