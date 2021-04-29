import os
import pandas as pd

import streamlit as st

from vc.data_treat.maps import month_dict
from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData

def settings():
    st.set_page_config(layout='wide')

def multiselect_cities(city_data: CitiesTempData):
    city_idx = st.sidebar.multiselect(
        'Select cities to view',
        options=city_data.get_cities(selection_only=False),
        default=[city_data.get_cities(selection_only=False)[0]]
    )
    # Check if any cities have been selected and warn the user if not.
    if len(city_idx) == 0:
        st.error('No cities are selected.')
        st.stop()

    city_data.set_city_selection(city_idx)

def braz_cities_choose_data(city_data: CitiesTempData):
        # Choose whether or not to only show a single month per year.
    month_bool = st.sidebar.checkbox(
        'Filter by month?',
        value=False
    )
    if month_bool:
        month = st.sidebar.select_slider(
            'Choose month',
            options=range(1, 13),
            format_func=month_dict.get
        )

        year_list = city_data.get_year_list()

        year_start = st.sidebar.slider(
            'Start year',
            min_value=year_list[0],
            max_value=year_list[-1]
        )

        year_end = st.sidebar.slider(
            'End year',
            min_value=year_start,
            max_value=year_list[-1],
            value=year_list[-1]
        )

        plot_df, stat_dict = city_data.get_data(year_start=year_start, year_end=year_end, month=month)

    else:
        dt_series = city_data.get_datetimes()

        date_start = st.sidebar.select_slider(
            'Start date',
            options=list(dt_series)
        )

        date_end = st.sidebar.select_slider(
            'End date',
            options=list(dt_series[dt_series >= date_start]),
            value=dt_series[-1]
        )

        month = None

        plot_df, stat_dict = city_data.get_data(date_start=date_start, date_end=date_end)

    return plot_df, stat_dict, month