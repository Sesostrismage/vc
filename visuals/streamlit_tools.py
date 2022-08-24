import matplotlib.pyplot as plt
import pandas as pd
import plotly.colors
import streamlit as st
from matplotlib import cm
from vc.data_treat.maps import Month
from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData


# Standard settings to apply at the start of every Streamlit script.
def settings():
    st.set_page_config(layout="wide")


def multiselect_cities(city_data: CitiesTempData):
    # Multiselect any cities from the data.
    city_idx = st.sidebar.multiselect(
        "Select cities to view",
        options=city_data.get_cities(selection_only=False),
        default=[city_data.get_cities(selection_only=False)[0]],
    )
    # Check if no cities have been selected and warn the user if this is the case.
    if len(city_idx) == 0:
        st.error("No cities are selected.")
        st.stop()
    # Set the selection in the cities data object.
    city_data.set_city_selection(city_idx)


def multiselect_cities_old_style(df: pd.DataFrame) -> list:
    # Multi-select which cities to plot.
    city_idx = st.sidebar.multiselect(
        "Select cities to view", options=list(df.columns), default=list(df.columns)
    )
    # Check if any cities have been selected and warn the user if not.
    if len(city_idx) == 0:
        st.error("No cities are selected.")
        st.stop()

    return city_idx


def braz_cities_choose_data(city_data: CitiesTempData):
    """
    Choose the date part of the data.

    Args:
        city_data (CitiesTempData): Temperature data

    Returns:
        If month is chosen, returns DataFrame, stat data and month.
        Else return DataFrame and stat data.
    """
    # Choose whether or not to only show a single month per year.
    month_bool = st.sidebar.checkbox("Filter by month?", value=False)

    if month_bool:
        # If yes, choose which month.
        month = st.sidebar.select_slider(
            "Choose month", options=range(1, 13), format_func=lambda x: Month(x).name
        )
        # Choose start and end years via sliders.
        year_list = city_data.get_year_list()

        year_start = st.sidebar.slider(
            "Start year", min_value=year_list[0], max_value=year_list[-1]
        )

        year_end = st.sidebar.slider(
            "End year",
            min_value=year_start,
            max_value=year_list[-1],
            value=year_list[-1],
        )
        # Get the data.
        plot_df, stat_dict = city_data.get_data(
            year_start=year_start, year_end=year_end, month=month
        )

    else:
        # If no month is chosen, choose start and end date.
        dt_series = city_data.get_datetimes()

        date_start = st.sidebar.select_slider("Start date", options=list(dt_series))

        date_end = st.sidebar.select_slider(
            "End date",
            options=list(dt_series[dt_series >= date_start]),
            value=dt_series[-1],
        )

        month = None
        # Get the data.
        plot_df, stat_dict = city_data.get_data(
            date_start=date_start, date_end=date_end
        )

    return plot_df, stat_dict, month


def cmap_matplotlib():
    # Choose a Matplotlib colormap.
    cmap_name = st.sidebar.selectbox(
        "Choose colormap", options=plt.colormaps(), index=plt.colormaps().index("jet")
    )
    cmap = cm.get_cmap(cmap_name)

    return cmap


def cmap_plotly():
    # Choose a Plotly colorscale.

    # Get both sequential and diverging colorscale names.
    full_list = list(plotly.colors.sequential.__dict__.keys()) + list(
        plotly.colors.diverging.__dict__.keys()
    )
    # Remove items that aren't colorscale names.
    pruned_list = sorted(
        [
            item
            for item in full_list
            if ((not item.startswith("_")) and (not item.startswith("swatches")))
        ]
    )
    # Choose among the possible colorscales.
    colorscale = st.sidebar.selectbox(
        "Choose colormap", options=pruned_list, index=pruned_list.index("Jet")
    )

    return colorscale
