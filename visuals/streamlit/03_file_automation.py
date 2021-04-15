import plotly.graph_objects as go
import numpy as np
import os
import pandas as pd
import streamlit as st

from vc.definitions import ROOT_DIR
import vc.visuals.streamlit_tools as stt

stt.settings()
# Folder path with root of vc dirextory automatically detected.
folder_path = os.path.join(ROOT_DIR, 'datasets', 'temp_brazil_cities', 'raw_data')

# File names of each data file as a list.
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

file_dict = {}
min_year = 2010
max_year = 2010

selected_cities_list = st.sidebar.multiselect(
    'Select file names to view',
    options=file_name_list,
    default=file_name_list
)

if len(selected_cities_list) == 0:
    st.error('No cities are selected.')
    st.stop()

show_mean_bool = st.sidebar.checkbox(
    'Show mean value?'
)

for file_name in selected_cities_list:
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

    min_year = min(min_year, df_crop.index[0])
    max_year = max(max_year, df_crop.index[-1])

    file_dict[file_name] = df_crop

# Get all available years from the file and make it into a list.
year_list = range(min_year, max_year+1)
# Selectbox to choose the year.
year = st.sidebar.selectbox(
    'Choose year to view',
    options=year_list,
    index=len(year_list)-1
)

fig = go.Figure()

mean_df = pd.DataFrame()

for file_name in file_dict:
    if year in file_dict[file_name].index:
        # Plot data from selected year if present.
        fig.add_trace(go.Scattergl(
            x=file_dict[file_name].columns, y=file_dict[file_name].loc[year], name=file_name
        ))

        #Build mean df.
        mean_df = pd.concat([mean_df, pd.DataFrame({file_name: file_dict[file_name].loc[year]})], axis=1)

if show_mean_bool:
    mean_series = mean_df.mean(axis=1)
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