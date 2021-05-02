import os
import plotly.graph_objects as go
import streamlit as st

from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData
import vc.visuals.plotly_tools.figure as pt_figure


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
    'Select x-axis city',
    options=city_data.get_cities(selection_only=False),
    key='x'
)
city_y = st.sidebar.selectbox(
    'Select y-axis city',
    options=city_data.get_cities(selection_only=False),
    key='y',
    index=1
)

color_option = st.sidebar.selectbox(
    'Color option',
    options=['City', 'Outlier detection']
)

df, stat_dict = city_data.get_data()
series_x = df[city_x]
series_y = df[city_y]

if color_option == 'City':
    city_color = st.sidebar.selectbox(
        'Select color city',
        options=city_data.get_cities(selection_only=False),
        key='c',
        index=2
    )

    cropped_df = df[[city_x, city_y, city_color]].dropna(how='any')
    series_x = cropped_df[city_x]
    series_y = cropped_df[city_y]
    series_color = cropped_df[city_color]

elif color_option == 'Outlier detection':
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

if color_option == 'City':
    fig = pt_figure.phase_space(stat_dict)

    text_list = [
        f"{idx}<br>" +
        f"{city_x}: {series_x.loc[idx]} deg C<br>" +
        f"{city_y}: {series_y.loc[idx]} deg C<br>" +
        f"{city_color}: {series_color.loc[idx]} deg C<br>"
        for idx, _ in series_x.iteritems()
    ]

    fig.add_trace(
        go.Scattergl(
            x=series_x,
            y=series_y,
            hoverinfo='text',
            hovertext=text_list,
            mode='markers',
            marker={'color': series_color},
            name='Temperatures'
        )
    )
    fig.update_layout(showlegend=False)

elif color_option == 'Outlier detection':
    fig = pt_figure.phase_space(stat_dict, outlier_x)

    text_list = [
        f"{idx}<br>" +
        f"{city_x}: {inlier_x.loc[idx]} deg C<br>" +
        f"{city_y}: {inlier_y.loc[idx]} deg C<br>" +
        f"Inlier<br>" +
        f"Outlier degree: {round(((inlier_y - inlier_x).abs()/inlier_x).loc[idx], 2)}<br>"
        for idx, _ in inlier_x.iteritems()
    ]

    fig.add_trace(
        go.Scattergl(
            x=inlier_x,
            y=inlier_y,
            hoverinfo='text',
            hovertext=text_list,
            mode='markers',
            marker={'color': 'lime'},
            name='Inliers'
        )
    )

    text_list = [
        f"{idx}<br>" +
        f"{city_x}: {outlier_x.loc[idx]} deg C<br>" +
        f"{city_y}: {outlier_y.loc[idx]} deg C<br>" +
        f"Outlier<br>" +
        f"Outlier degree: {round(((outlier_y - outlier_x).abs()/outlier_x).loc[idx], 2)}<br>"
        for idx, _ in outlier_x.iteritems()
    ]

    fig.add_trace(
        go.Scattergl(
            x=outlier_x,
            y=outlier_y,
            hoverinfo='text',
            hovertext=text_list,
            mode='markers',
            marker={'color': 'red'},
            name='Outliers'
        )
    )

st.plotly_chart(fig)