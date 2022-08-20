import datetime
import json

from dateutil.parser import parse
from vc.definitions import ROOT_DIR


class CityDataLabeler:
    def __init__(self, city_name: str) -> None:
        """
        Object handle labeling of Brazilian cities temperature data.

        Args:
            city_name (str): Name of the city to handle labels for.
        """
        self.city_name = city_name
        # Generate paths to cities data.
        self.folder_path = ROOT_DIR / "datasets" / "temp_brazil_cities"
        # Generate path to labels file.
        self.file_path = self.folder_path / "labels.json"

        # Load the full label set.
        with open(self.file_path) as f:
            self.full_tag_dict = json.load(f)

        # Get any existing labels for the city.
        if self.city_name not in self.full_tag_dict:
            self.dt_list = []
        else:
            self.dt_list = [
                parse(dt).date() for dt in self.full_tag_dict[self.city_name]
            ]

    def get_datetimes(
        self, date_start: datetime.date = None, date_end: datetime.date = None
    ) -> list:
        """
        Get all labeled dates, optionally within user-set bounds.

        Args:
            date_start (datetime.date, optional): Start date. Defaults to None.
            date_end (datetime.date, optional): End date. Defaults to None.

        Returns:
            list: All labeled dates within the bounds, if any.
        """
        if date_start is None or date_end is None:
            dt_in_period_list = self.dt_list
        else:
            dt_in_period_list = [
                dt for dt in self.dt_list if date_start <= dt <= date_end
            ]

        return dt_in_period_list

    def insert_datetimes(self, insert_dt_list: list) -> None:
        """
        Insert defined dates into the label set.

        Args:
            insert_dt_list (list): Dates to insert.
        """
        # Case when no labels currently exist.
        if len(self.dt_list) == 0:
            # The date list becomes the label list for that city.
            self.dt_list = sorted(insert_dt_list)
        # Case with existing labels.
        else:
            # The insert list becomes merged with the existing list.
            self.dt_list = sorted(list(set(self.dt_list + insert_dt_list)))

        # Save to file.
        self.save()

    def remove_datetimes(self, remove_dt_list: list) -> None:
        """
        Remove defined dates from the label set.

        Args:
            remove_dt_list (list): Dates to remove from the label set.
        """
        # Makes the exising labels and the labels to remove into sets,
        # Subtract one from the other and turn the result back into a list.
        self.dt_list = sorted(list(set(self.dt_list) - set(remove_dt_list)))
        self.save()

    def save(self) -> None:
        """
        Insert the current label list into the full label set
        and save to file.
        """
        # Convert the dates to strings, else they can't be saved to JSON.
        dt_str_list = [str(dt) for dt in self.dt_list]
        # Insert the city's labels into the dict.
        self.full_tag_dict[self.city_name] = dt_str_list
        # Save to file.
        with open(self.file_path, "w") as f:
            json.dump(self.full_tag_dict, f, indent=4, sort_keys=True)
