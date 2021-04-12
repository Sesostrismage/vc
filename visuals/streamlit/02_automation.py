import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from vc.analytics.braz_cities_temp import year_span
from vc.data_io import files
import vc.visuals.streamlit_tools as stt

stt.settings()

# Folder path to data files.
folder_path = r"C:/Data/temperature_time-series_for_brazilian_cities/"
# Load all data files into a dict with city names as keys.
data_dict = files.braz_cities_temp(folder_path)

selected_cities_list = st.sidebar.multiselect(
    'Select cities to view',
    options=list(data_dict.keys()),
    default=list(data_dict.keys())
)

if len(selected_cities_list) == 0:
    st.error('No cities are selected.')
    st.stop()

show_mean_bool = st.sidebar.checkbox(
    'Show mean value?'
)

min_year, max_year = year_span(data_dict, selected_cities_list)

# Selectbox to choose the year.
year = st.sidebar.selectbox(
    'Choose year to view',
    options=range(min_year, max_year+1),
    index=len(range(min_year, max_year+1))-1
)

fig = go.Figure()

mean_df = pd.DataFrame()

for city in data_dict:
    if year in data_dict[city].index:
        # Plot data from selected year if present.
        fig.add_trace(go.Scattergl(
            x=data_dict[city].columns, y=data_dict[city].loc[year], name=city
        ))

        #Build mean df.
        mean_df = pd.concat([mean_df, pd.DataFrame({city: data_dict[city].loc[year]})], axis=1)

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