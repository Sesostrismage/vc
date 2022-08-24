import pandas as pd
import streamlit as st
from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData


def filter_cities_data_by_month(
    city_slice_df: pd.DataFrame, city_idx: list, month: int
) -> pd.DataFrame:
    # Create an index of all places where the data is null for all selected cities.
    na_idx = city_slice_df.isnull().all(axis=1)

    # Get a list of all usable years in the data.
    year_list = sorted(set([dt.year for dt in city_slice_df.loc[~na_idx].index]))
    # Choose start and end year.
    year_start = st.sidebar.slider(
        "Start year", min_value=year_list[0], max_value=year_list[-1]
    )

    year_end = st.sidebar.slider(
        "End year", min_value=year_start, max_value=year_list[-1], value=year_list[-1]
    )
    # Create an index of all dates fulfilling the requirements.
    dt_idx = [
        True if ((year_start <= dt.year <= year_end) and (dt.month == month)) else False
        for dt in city_slice_df.index
    ]
    # Create the plot DataFrame.
    plot_df = city_slice_df.loc[dt_idx & ~na_idx, city_idx]

    return plot_df


def get_x_axis_extremes(city_data: CitiesTempData) -> dict:
    # Get the smallest and largest datetimes, regardless of city selection.
    datetimes = city_data.get_datetimes(selection_only=False)
    x_min = datetimes.min()
    x_max = datetimes.max()
    return x_min, x_max
