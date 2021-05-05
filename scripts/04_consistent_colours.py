import plotly.graph_objects as go
import numpy as np
import os
import pandas as pd
import plotly.express as px
import streamlit as st

from vc.definitions import ROOT_DIR


####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
st.set_page_config(layout='wide')
# Title becomes the file name for easy reference to the presentation.
st.title(os.path.basename(__file__))
# Folder path with root of vc directory automatically detected.
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

# Create a dictionary to hold consistent colours for each city.
cdict = {}
# Ensure that the cities are always sorted in the same order.
sorted_list = sorted(city_dict.keys())
# Assign colours to each city.
for idx, item in enumerate(sorted_list):
    cdict[item] = px.colors.qualitative.Alphabet[idx]


####################################################################
# User input and calculations.
####################################################################

# Multi-select files to load, with all files chosen by default from the dict.
selected_cities_list = st.sidebar.multiselect(
    'Select cities to view',
    options=sorted(list(city_dict.keys())),
    default=sorted(list(city_dict.keys()))
)

# If no files are chosen, show a warning and stop the program.
if len(selected_cities_list) == 0:
    st.error('No cities are selected.')
    st.stop()

# Find earliest and latest years that have data.
# Start with a year that is in all cities' data.
min_year = 2010
max_year = 2010
# Loop through all cities and find the earliest and latest year with data.
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
# Choose whether or not to having consistent colours assigned to the cities.
consistent_color_bool = st.sidebar.checkbox(
    'Consistent colormap?',
)
# Choose whether or not to show the mean value line.
show_mean_bool = st.sidebar.checkbox(
    'Show mean value?'
)
# If yes, build the mean dataframe.
if show_mean_bool:
    mean_df = pd.DataFrame()
    # Loop through all cities.
    for city_name in city_dict:
        if year in city_dict[city_name].index:
            #Build mean df.
            mean_df = pd.concat([mean_df, pd.DataFrame({city_name: city_dict[city_name].loc[year]})], axis=1)
    # Calculate the mean series.
    mean_series = mean_df.mean(axis=1)


####################################################################
# Plotting.
####################################################################

# Create a Plotly figure.
fig = go.Figure()
# Layout.
fig.update_xaxes(title='Datetime')
fig.update_yaxes(title='Temperature [deg C]')
fig.update_layout(
    title=f"Temperature for brazilian cities in {year}",
    hovermode='x',
    height=600,
    width=1100
)

# Plot each chosen city if it has data.
for city_name in (city for city in city_dict if city in selected_cities_list):
    if year in city_dict[city_name].index:
        if consistent_color_bool:
            # Plot data from selected year if present.
            # use the assigned colour for each city.
            fig.add_trace(go.Scattergl(
                x=city_dict[city_name].columns,
                y=city_dict[city_name].loc[year],
                line={'color': cdict[city_name]},
                name=city_name
            ))
        else:
            # Else plot without consistent colour assignment.
            fig.add_trace(go.Scattergl(
                x=city_dict[city_name].columns,
                y=city_dict[city_name].loc[year],
                name=city_name
            ))

# Plot mean line if chosen.
if show_mean_bool:
    fig.add_trace(go.Scattergl(
        x=mean_series.index, y=mean_series, name='All-city mean', line={'color': 'grey'}
    ))

# Show the figure in the Streamlit app.
st.plotly_chart(fig)