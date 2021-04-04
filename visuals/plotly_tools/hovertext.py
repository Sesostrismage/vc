import pandas as pd

def braz_cities_temp(series: pd.Series, city_name: str, timespan) -> list:
    text_list = [
        f"{city_name} {idx.title()} {timespan}<br>" +
        f"{round(item, 1)} Deg C"
        for idx, item in series.iteritems()
    ]

    return text_list