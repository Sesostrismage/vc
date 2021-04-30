import datetime
import json
import os

from dateutil.parser import parse

from vc.definitions import ROOT_DIR

class CityDataLabeler():
    def __init__(
        self,
        city_name: str
    ) -> None:
        self.city_name = city_name
        self.folder_path = os.path.join(ROOT_DIR, 'datasets', 'temp_brazil_cities')
        self.file_path = os.path.join(self.folder_path, 'labels.json')

        # Load the full tag dict.
        f = open(self.file_path)
        self.full_tag_dict = json.load(f)
        f.close()

        if self.city_name not in self.full_tag_dict:
            self.dt_list = []
        else:
            self.dt_list = [parse(dt).date() for dt in self.full_tag_dict[self.city_name]]

    def get_datetimes(
        self,
        date_start: datetime.date=None,
        date_end: datetime.date=None
    ) -> list:
        if date_start is None or date_end is None:
            dt_in_period_list = self.dt_list
        else:
            dt_in_period_list = [dt for dt in self.dt_list if date_start <= dt <= date_end]

        return dt_in_period_list

    def insert_datetimes(self, insert_dt_list: list) -> None:
        # Case when no tags currently exist.
        if len(self.dt_list) == 0:
            self.dt_list = sorted(insert_dt_list)
        else:
            self.dt_list = sorted(list(set(self.dt_list + insert_dt_list)))

        self.save()

    def remove_datetimes(self, remove_dt_list: list) -> None:
        self.dt_list = sorted(list(
            set(self.dt_list) - set(remove_dt_list)
        ))
        self.save()

    def save(self) -> None:
        dt_str_list = [str(dt) for dt in self.dt_list]
        self.full_tag_dict[self.city_name] = dt_str_list

        with open(self.file_path, 'w') as f:
            json.dump(self.full_tag_dict, f, indent=4, sort_keys=True)