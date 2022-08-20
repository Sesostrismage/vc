import pandas as pd
from vc.data_treat.maps import Month


def braz_cities_temp(plot_df: pd.DataFrame, city_name: str, month: int) -> list:
    """
    Hovertext for standard time plot.

    Args:
        plot_df (pd.DataFrame): DataFrame with temperature data.
        city_name (str): Name of the city to plot.
        month (int): Month to plot, if any.

    Returns:
        text_list (list): Hovertext elements.
    """
    if month is not None:
        text_list = [
            f"{city_name} - {Month(month).name} {idx.year}<br>"
            + f"{row[city_name]} deg C"
            for idx, row in plot_df.iterrows()
        ]
    else:
        text_list = [
            f"{city_name} - {idx}<br>" + f"{row[city_name]} deg C"
            for idx, row in plot_df.iterrows()
        ]

    return text_list
