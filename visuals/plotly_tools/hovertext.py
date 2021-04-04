import pandas as pd

def braz_cities_temp(series: pd.Series, city_name: str, timespan) -> list:
    text_list = [
        f"{city_name} {idx.title()} {timespan}<br>" +
        f"{item} Deg C"
        for idx, item in series.iteritems()
    ]

    return text_list