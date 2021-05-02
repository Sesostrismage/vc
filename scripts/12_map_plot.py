import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import os
import pandas as pd
import pydeck as pdk
import streamlit as st

from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData
from vc.datasets.temp_brazil_cities.coordinates import coords
import vc.visuals.streamlit_tools as stt

# Standard Streamlit settings.
stt.settings()
# Title becomes the file name for easy reference to the presentation.
st.title(os.path.basename(__file__))
# Object with city temp data.
city_data = CitiesTempData()

df, stat_dict = city_data.get_data()

options = list(df.index)

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
        'temperature': temp_series,
        'date': pd.Series(str(date_show)[:-3], index=temp_series.index)
    }
)

for city in plot_df.index:
    plot_df.loc[city, 'all_time_low'] = df[city].min()
    plot_df.loc[city, 'all_time_high'] = df[city].max()

temp_min = stat_dict['min_total']
temp_max = stat_dict['max_total']
temp_series_norm = (temp_series - temp_min)/(temp_max - temp_min)

cmap = cm.get_cmap('coolwarm')

for city, temp in temp_series_norm.iteritems():
    k = matplotlib.colors.colorConverter.to_rgb(cmap(temp))
    plot_df.loc[city, 'r'] = int(k[0] * 255)
    plot_df.loc[city, 'g'] = int(k[1] * 255)
    plot_df.loc[city, 'b'] = int(k[2] * 255)

plot_df['lat'] = 0
plot_df['lon'] = 0

for city in coords:
    if city in plot_df.index:
        plot_df.loc[city, 'lat'] = coords[city]['lat']
        plot_df.loc[city, 'lon'] = coords[city]['lon']

st.pydeck_chart(
    pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=-17,
            longitude=-65,
            zoom=4,
            pitch=50
        ),
        tooltip={'text': '{city} {date}: {temperature}\nAll-time low: {all_time_low}\nAll-time high: {all_time_high}'},
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