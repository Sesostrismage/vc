import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk
import streamlit as st

from vc.data_io import files
from vc.ref_data.braz_cities_locations import loc
import vc.visuals.streamlit_tools as stt
import vc.visuals.plotly_tools.hovertext as pt_hover
import vc.visuals.plotly_tools.layout as pt_layout
import vc.visuals.plotly_tools.trace as pt_trace

stt.settings()

# IMPROVE Add title.
# TODO Dostrings.
# Folder path to data files.
folder_path = r"C:/Data/temperature_time-series_for_brazilian_cities/"

df = files.braz_cities_temp_all(folder_path)

plot_mode = st.sidebar.selectbox(
    'Choose display mode',
    options=['Line plot', 'Map plot']
)

month_bool = st.sidebar.checkbox(
    'Filter by month?',
    value=False
)
if month_bool:
    month = st.sidebar.slider(
        'Choose month',
        min_value=1,
        max_value=12,
        step=1
    )
    options = [dt for dt in df.index if dt.month == month]

else:
    options = list(df.index)


if plot_mode == 'Line plot':
    city = st.sidebar.selectbox(
        'Choose city',
        options=df.columns
    )

    date_start = st.sidebar.select_slider(
        'Start date',
        options=options
    )

    date_end = st.sidebar.select_slider(
        'End date',
        options=options,
        value=options[-1]
    )

    if date_start >= date_end:
        st.error('Date start is greater than date end!')
        st.stop()

    range_df = df.loc[date_start:date_end]
    range_df = range_df[range_df.index.isin(options)]

    city_series = range_df[city]

    fig = go.Figure()
    fig = pt_trace.minmax_shapes(fig, range_df, axis=1)

    text_list = pt_hover.braz_cities_temp(city_series, city, '', ref_df=range_df, axis=1)

    # Plot data from selected date range with hovertext.
    fig.add_trace(
        go.Scattergl(
            x=city_series.index,
            y=city_series,
            hoverinfo='text',
            hovertext=text_list,
            line={'color': 'black'},
            showlegend=False
        )
    )
    fig = pt_layout.braz_cities_temp_all(fig, city_series)
    fig.update_yaxes(range=[df.min().min(), df.max().max()])
    st.plotly_chart(fig)

elif plot_mode == 'Map plot':
    date_show = st.sidebar.select_slider(
        'Show date',
        options=options,
        value=options[-1]
    )

    temp_series = df.loc[date_show]
    temp_series.dropna(how='any', inplace=True)

    plot_df = pd.DataFrame(
        {
            'city': temp_series.index,
            'temperature': temp_series
        }
    )

    for city in plot_df.index:
        plot_df.loc[city, 'all_time_low'] = df[city].min()
        plot_df.loc[city, 'all_time_high'] = df[city].max()

    temp_min = df.min().min()
    temp_max = df.max().max()
    temp_series_norm = (temp_series - temp_min)/(temp_max - temp_min)

    cmap_name = st.sidebar.selectbox(
        'Choose colormap',
        options=plt.colormaps(),
        index=plt.colormaps().index('jet')
    )
    cmap = cm.get_cmap(cmap_name)

    for city, temp in temp_series_norm.iteritems():
        k = matplotlib.colors.colorConverter.to_rgb(cmap(temp))
        plot_df.loc[city, 'r'] = int(k[0] * 255)
        plot_df.loc[city, 'g'] = int(k[1] * 255)
        plot_df.loc[city, 'b'] = int(k[2] * 255)

    plot_df['lat'] = 0
    plot_df['lon'] = 0

    for city in loc:
        if city in plot_df.index:
            plot_df.loc[city, 'lat'] = loc[city]['lat']
            plot_df.loc[city, 'lon'] = loc[city]['lon']

    st.pydeck_chart(
        pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=-17,
                longitude=-65,
                zoom=4,
                pitch=50
            ),
            tooltip={'text': '{city}: {temperature}\n{city} All-time low: {all_time_low}\n{city} All-time high: {all_time_high}'},
            layers = [
                pdk.Layer(
                    "ScatterplotLayer",
                    plot_df,
                    pickable=True,
                    get_position=['lon', 'lat'],
                    get_fill_color=['r', 'g', 'b'],
                    get_line_color=[0, 0, 0],
                    get_radius=100000
                )
            ]
        )
    )