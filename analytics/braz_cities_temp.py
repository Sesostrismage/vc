def year_span(data_dict: dict, selected_cities_list: list):
    min_year = 2010
    max_year = 2010

    for city in selected_cities_list:
        if city in data_dict:
            min_year = min(min_year, data_dict[city].index[0])
            max_year = max(max_year, data_dict[city].index[-1])

    return min_year, max_year
