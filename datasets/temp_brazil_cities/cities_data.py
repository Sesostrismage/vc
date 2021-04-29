import datetime
import pandas as pd

from vc.data_io import files

class CitiesTempData:
    def __init__(self) -> None:
        self._df = files.braz_cities_temp()
        self.city_selection = list(self._df.columns)

    def get_cities(self, selection_only: bool=True) -> list:
        if selection_only:
            return self.city_selection
        else:
            return list(self._df.columns)

    def set_city_selection(self, city_selection: list):
        for city in city_selection:
            if not city in self._df.columns:
                raise KeyError(f"{city} is not in the data.")

        self.city_selection = city_selection

    def get_datetimes(
        self,
        selection_only: bool=True,
        as_bool: bool=False
    ) -> pd.Series:
        if selection_only:
            cities = self.get_cities()
            dt_bool = self._df[cities].notnull().any(axis=1)
        else:
            dt_bool = self._df.notnull().any(axis=1)

        if as_bool:
            return dt_bool
        else:
            return self._df.loc[dt_bool].index

    def get_year_list(self, selection_only: bool=True) -> list:
        dt_idx = self.get_datetimes(selection_only=selection_only)
        year_list = sorted(set([dt.year for dt in dt_idx]))

        return year_list

    def get_data(
        self,
        selection_only: bool=True,
        year_start: int=None,
        year_end: int=None,
        month: int=None,
        date_start: datetime.date=None,
        date_end: datetime.date=None
    ) -> pd.DataFrame:
        out_df = self._df.loc[self._df.notnull().any(axis=1)]

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

        stat_dict = {
            'min': out_df.min(axis=1),
            'min_total': self._df.min().min(),
            'mean': out_df.mean(axis=1),
            'max': out_df.max(axis=1),
            'max_total': self._df.max().max()
        }

        if selection_only:
            out_df = out_df[self.city_selection]

        return out_df.copy(), stat_dict