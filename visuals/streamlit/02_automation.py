import plotly.graph_objects as go
import pandas as pd
import streamlit as st

from vc.analytics.braz_cities_temp import year_span
from vc.data_io import files
import vc.visuals.streamlit_tools as stt

stt.settings()

# Load all data files into a dict with city names as keys.
data_dict = files.braz_cities_temp(folder_path)
# Multi-select cities.
selected_cities_list = stt.multiselect_cities(data_dict)
# Whether or not to show the mean graph.
show_mean_bool = st.sidebar.checkbox('Show mean value?')
# Get the span of years in the selected data.
min_year, max_year = year_span(data_dict, selected_cities_list)

# Selectbox to choose the year.
year = st.sidebar.selectbox(
    'Choose year to view',
    options=range(min_year, max_year+1),
    index=len(range(min_year, max_year+1))-2
)

# Create figure.
fig = go.Figure()

# Create DataFrame to receive data for mean graph.
mean_df = pd.DataFrame()

for city in selected_cities_list:
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