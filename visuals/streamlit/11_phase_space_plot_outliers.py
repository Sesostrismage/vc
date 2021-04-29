import os
import plotly.graph_objects as go
import streamlit as st

from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData
import vc.visuals.plotly_tools.figure as pt_figure
import vc.visuals.streamlit_tools as stt


####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
st.set_page_config(layout='wide')
# Title becomes the file name for easy reference to the presentation.
st.title(os.path.basename(__file__))
# Object with city temp data.
city_data = CitiesTempData()

df, stat_dict = city_data.get_data()


####################################################################
# User input and calculations.
####################################################################

city_x = st.sidebar.selectbox(
        'Select cities to view',
        options=city_data.get_cities(selection_only=False),
        key='x'
    )
city_y = st.sidebar.selectbox(
        'Select cities to view',
        options=city_data.get_cities(selection_only=False),
        key='y',
        index=1
    )

df, stat_dict = city_data.get_data()

series_x = df[city_x]
series_y = df[city_y]

outlier_tolerance = st.sidebar.slider(
    'Outlier tolerance',
    min_value=0.,
    max_value=1.,
    step=0.01,
    value=1.
)

outlier_idx = (
    (series_y - series_x).abs()/series_x > outlier_tolerance
)

inlier_x = series_x.loc[~outlier_idx]
inlier_y = series_y.loc[~outlier_idx]
outlier_x = series_x.loc[outlier_idx]
outlier_y = series_y.loc[outlier_idx]

####################################################################
# Plotting.
####################################################################

fig = pt_figure.phase_space(outlier_x)
fig.add_trace(
    go.Scattergl(
        x=inlier_x,
        y=inlier_y,
        mode='markers',
        marker={'color': 'lime'},
        name='Inliers'
    )
)
fig.add_trace(
    go.Scattergl(
        x=outlier_x,
        y=outlier_y,
        mode='markers',
        marker={'color': 'red'},
        name='Outliers'
    )
)
fig.update_xaxes(range=[stat_dict['min_total'], stat_dict['max_total']])
fig.update_yaxes(range=[stat_dict['min_total'], stat_dict['max_total']])
fig.update_layout(showlegend=True)
st.plotly_chart(fig)