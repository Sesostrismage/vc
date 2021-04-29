import pandas as pd

from vc.data_treat import maps

def braz_cities_temp(
    plot_df: pd.DataFrame,
    city_name: str,
    month: int
):
    if month is not None:
        text_list = [
            f"{city_name} - {maps.month_dict[month]} {idx.year}<br>" +
            f"{row[city_name]} deg C"
            for idx, row in plot_df.iterrows()
        ]
    else:
        text_list = [
            f"{city_name} - {idx}<br>" +
            f"{row[city_name]} deg C"
            for idx, row in plot_df.iterrows()
        ]

    return text_list


def braz_cities_temp_old(
    series: pd.Series,
    city_name: str,
    timespan,
    ref_df: pd.DataFrame=None,
    axis=0
) -> list:

    if ref_df is None:
        text_list = [
            f"{city_name} {str(idx).title()} {timespan}<br>" +
            f"{round(item, 1)} Deg C"
            for idx, item in series.iteritems()
        ]

    else:
        min_series = ref_df.min(axis=axis)
        mean_series = ref_df.mean(axis=axis)
        max_series = ref_df.max(axis=axis)

        idxmin_series = ref_df.idxmin(axis=axis)
        idxmax_series = ref_df.idxmax(axis=axis)

        text_list = [
            f"{city_name} {str(idx).title()} {timespan}<br>" +
            f"{round(item, 1)} Deg C<br>" +
            f"{round(min_series.loc[idx], 1)} deg C minimum ({idxmin_series.loc[idx]})<br>" +
            f"{round(mean_series.loc[idx], 1)} deg C mean<br>" +
            f"{round(max_series.loc[idx], 1)} deg C maximum ({idxmax_series.loc[idx]})<br>"
            for idx, item in series.iteritems()
        ]

    return text_list
