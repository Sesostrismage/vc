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
# Get data from all cities.
df, stat_dict = city_data.get_data()

# Choose from all dates in the dataset.
options = list(df.index)
# Default is the latest date.
date_show = st.sidebar.select_slider(
    'Show date',
    options=options,
    value=options[-1]
)
# Get all data from the chosen date.
temp_series = df.loc[date_show]
# Drop any NaN entries.
temp_series.dropna(how='any', inplace=True)
# Create DataFrame where the date has the day part removed.
plot_df = pd.DataFrame(
    {
        'city': temp_series.index,
        'temperature': temp_series,
        'date': pd.Series(str(date_show)[:-3], index=temp_series.index)
    }
)
# Get all-time highs and lows per city.
for city in plot_df.index:
    plot_df.loc[city, 'all_time_low'] = df[city].min()
    plot_df.loc[city, 'all_time_high'] = df[city].max()

# Map the series between 0 and 1, bounded by all-time temperatures for consistency.
temp_min = stat_dict['min_total']
temp_max = stat_dict['max_total']
temp_series_norm = (temp_series - temp_min)/(temp_max - temp_min)
# Get a colormap.
cmap = cm.get_cmap('coolwarm')
# Create RGB values to add to the plot DataFrame, since it's needed for PyDeck colouring.
for city, temp in temp_series_norm.iteritems():
    k = matplotlib.colors.colorConverter.to_rgb(cmap(temp))
    plot_df.loc[city, 'r'] = int(k[0] * 255)
    plot_df.loc[city, 'g'] = int(k[1] * 255)
    plot_df.loc[city, 'b'] = int(k[2] * 255)

# Get latitude and longitude for each city with data.
plot_df['lat'] = 0
plot_df['lon'] = 0

for city in coords:
    if city in plot_df.index:
        plot_df.loc[city, 'lat'] = coords[city]['lat']
        plot_df.loc[city, 'lon'] = coords[city]['lon']

# Plot on a map.
st.pydeck_chart(
    pdk.Deck(
        # Map style.
        map_style='mapbox://styles/mapbox/light-v9',
        # Initial view, choosing coordinates and zoom.
        initial_view_state=pdk.ViewState(
            latitude=-17,
            longitude=-65,
            zoom=4,
            pitch=50
        ),
        # Defining the hovertext from the DataFrame columns.
        tooltip={'text': '{city} {date}: {temperature}\nAll-time low: {all_time_low}\nAll-time high: {all_time_high}'},
        # Plot the data at coordinates and coloured by temperature.
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