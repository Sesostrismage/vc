import datetime
import pandas as pd

from vc.data_io import files

# Object to hold Brazilian cities temperature data.
class CitiesTempData:
    # Automatically loads all data and sets selection to all cities.
    def __init__(self) -> None:
        self._df = files.braz_cities_temp()
        self.city_selection = list(self._df.columns)

    # Get a list of either all cities in the data
    # or all currently selected cities.
    def get_cities(self, selection_only: bool=True) -> list:
        if selection_only:
            return self.city_selection
        else:
            return list(self._df.columns)

    # Set the city selection, with input checking.
    def set_city_selection(self, city_selection: list):
        for city in city_selection:
            if not city in self._df.columns:
                raise KeyError(f"{city} is not in the data.")

        # Done like this to avoid errors if the same city is listed
        # multiple times in the selection.
        self.city_selection = sorted(list(set(city_selection)))

    # Get datetimes in the data.
    def get_datetimes(
        self,
        selection_only: bool=True,
        as_bool: bool=False
    ) -> pd.Series:
        # If this, only datetimes with valid data from
        # the selected cities.
        if selection_only:
            cities = self.get_cities()
            dt_bool = self._df[cities].notnull().any(axis=1)
        # Else get all all datetimes.
        else:
            dt_bool = self._df.notnull().any(axis=1)

        # Whether or not to return a boolean mask or
        # The actual dates.
        if as_bool:
            return dt_bool
        else:
            return self._df.loc[dt_bool].index

    # Get a list of years in the data, either for all the data
    # Or only for the cities selected.
    def get_year_list(self, selection_only: bool=True) -> list:
        dt_idx = self.get_datetimes(selection_only=selection_only)
        year_list = sorted(set([dt.year for dt in dt_idx]))

        return year_list

    # Get the actual data.
    def get_data(
        self,
        selection_only: bool=True,
        year_start: int=None,
        year_end: int=None,
        month: int=None,
        date_start: datetime.date=None,
        date_end: datetime.date=None
    ) -> pd.DataFrame:
        """
        This function gets the temperature data within chosen constraints.

        Args:
            selection_only (bool, optional): If only data from chosen cities should be returned. Defaults to True.
            year_start (int, optional): Start year. Defaults to None.
            year_end (int, optional): End year. Defaults to None.
            month (int, optional): Get from only this month every year. Defaults to None.
            date_start (datetime.date, optional): Start date. Defaults to None.
            date_end (datetime.date, optional): End date. Defaults to None.

        Returns:
            pd.DataFrame: [description]
        """
        # Get all data with at least one non-null entry per date.
        out_df = self._df.loc[self._df.notnull().any(axis=1)].copy()

        # A series of slices of the data depending on the input choices.
        if year_start is not None:
            out_df = out_df.loc[[True if year_start <= dt.year else False for dt in out_df.index]]

        if year_end is not None:
            out_df = out_df.loc[[True if dt.year <= year_end else False for dt in out_df.index]]

        if month is not None:
            out_df = out_df.loc[[True if dt.month == month else False for dt in out_df.index]]

        if date_start is not None:
            out_df = out_df.loc[[True if dt >= date_start else False for dt in out_df.index]]

        if date_end is not None:
            out_df = out_df.loc[[True if dt <= date_end else False for dt in out_df.index]]

        # Create some handy statistics for plotting and titles.
        stat_dict = {
            'min': out_df.min(axis=1),
            'min_total': self._df.min().min(),
            'mean': out_df.mean(axis=1),
            'max': out_df.max(axis=1),
            'max_total': self._df.max().max()
        }

        # Whether or not to only include data from chosen cities.
        if selection_only:
            out_df = out_df[self.city_selection]

        return out_df, stat_dict