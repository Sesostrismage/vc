import pandas as pd

def mean_all_cities_per_year(
    data_dict: dict,
    selected_cities_list: list,
    year: int
) -> pd.DataFrame:
    # Create DataFrame to receive data for mean graph.
    mean_df = pd.DataFrame()

    for city in selected_cities_list:
        if year in data_dict[city].index:
            #Build mean df.
            mean_df = pd.concat([mean_df, pd.DataFrame({city: data_dict[city].loc[year]})], axis=1)

    mean_series = mean_df.mean(axis=1)

    return mean_series


def year_span(data_dict: dict, selected_cities_list: list):
    min_year = 2010
    max_year = 2010

    for city in selected_cities_list:
        if city in data_dict:
            min_year = min(min_year, data_dict[city].index[0])
            max_year = max(max_year, data_dict[city].index[-1])

    return min_year, max_year
