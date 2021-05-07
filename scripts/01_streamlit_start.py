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
# Title becomes the file name for easy reference to the presentation.
st.title(os.path.basename(__file__))
# Folder path with root of vc directory automatically detected.
folder_path = os.path.join(ROOT_DIR, 'datasets', 'temp_brazil_cities', 'raw_data')
# List of file names with data.
file_name_list = [
    'station_belem.csv',
    'station_curitiba.csv',
    'station_fortaleza.csv',
    'station_goiania.csv',
    'station_macapa.csv',
    'station_manaus.csv',
    'station_recife.csv',
    'station_rio.csv',
    'station_salvador.csv',
    'station_sao_luiz.csv',
    'station_sao_paulo.csv',
    'station_vitoria.csv'
]
# Empty dict to receive data.
file_dict = {}

# Loop through all file names and load the data.
for file_name in file_name_list:
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
    # Insert the dataframe into the dict.
    file_dict[file_name] = df_crop


####################################################################
# User input and calculations.
####################################################################

# Multi-select files to load, with all files chosen by default.
selected_files_list = st.sidebar.multiselect(
    'Select file names to view',
    options=file_name_list,
    default=file_name_list
)

# If no files are chosen, show a warning and stop the program.
if len(selected_files_list) == 0:
    st.error('No files are selected.')
    st.stop()

# Find earliest and latest years that have data.
# Start with a year that is in all cities' data.
min_year = 2010
max_year = 2010
# Loop through all cities and find the earliest and latest year with data.
for city in selected_files_list:
    if city in file_dict:
        min_year = min(min_year, file_dict[city].index[0])
        max_year = max(max_year, file_dict[city].index[-1])

# Make a list of all available years.
year_list = range(min_year, max_year+1)

# Selectbox to choose the year, default is the latest year.
year = st.sidebar.selectbox(
    'Choose year to view',
    options=year_list,
    index=len(year_list)-1
)

# Choose whether or not to show the mean value in the plot.
show_mean_bool = st.sidebar.checkbox(
    'Show mean value?'
)
# If yes, build the mean dataframe.
if show_mean_bool:
    mean_df = pd.DataFrame()

    for file_name in file_dict:
        if year in file_dict[file_name].index:
            #Build mean df.
            mean_df = pd.concat([mean_df, pd.DataFrame({file_name: file_dict[file_name].loc[year]})], axis=1)
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
    title='Temperature for brazilian cities in ' + str(year),
    hovermode='x',
    height=600,
    width=1100,
    plot_bgcolor='#ffffff'
)
# Dict to set better axis properties.
axis_dict = {
    # Move ticks outside the plot.
    'ticks': 'outside',
    # Show plot borders with these four settings.
    'showline': True,
    'linewidth': 2,
    'linecolor': 'black',
    'mirror': True,
    # Remove gridlines in the plot.
    'showgrid': False
}
# Apply to both axes.
fig.update_xaxes(axis_dict)
fig.update_yaxes(axis_dict)

# Plot each chosen city if it has data.
for file_name in (fname for fname in file_dict if fname in selected_files_list):
    if year in file_dict[file_name].index:
        # Name the trace after the file.
        fig.add_trace(go.Scattergl(
            x=file_dict[file_name].columns, y=file_dict[file_name].loc[year], name=file_name
        ))

# Plot mean line if chosen.
if show_mean_bool:
    fig.add_trace(go.Scattergl(
        x=mean_series.index, y=mean_series, name='All-city mean'
    ))

# Show the figure in the Streamlit app.
st.plotly_chart(fig)