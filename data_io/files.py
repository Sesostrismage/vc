import datetime
import numpy as np
import os
import pandas as pd

from vc.definitions import ROOT_DIR

# This function loads files from the Brazilian cities temperature dataset.
def braz_cities_temp(mode: str='agg'):
    # Gets the folder path relative to the root dir of the module.
    folder_path = os.path.join(ROOT_DIR, 'datasets', 'temp_brazil_cities', 'raw_data')

    # Function to perform the actual loading of each city's data.
    def load_file(file_path: str) -> pd.DataFrame:
        # Load data into Pandas DataFrame with first row as column names and first column as index names.
        df = pd.read_csv(
            file_path,
            header=0,
            index_col=0
        )
        # Remove pre-generated average columns.
        df_crop = df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
        # Set erroneous values to NaN so they don't disturb the results.
        df_crop[df_crop > 100] = np.nan

        return df_crop

    # Function to extract the city name from the file name.
    def fname_to_city_name(file_name: str) -> str:
        city_name = file_name[8:-4].replace('_', ' ').title()
        return city_name

    # Get a lidt of all files in the folder.
    file_name_list = os.listdir(folder_path)

    # If mode == 'dict', load the data from each file as-is into a dict key.
    if mode == 'dict':
        file_dict = {}

        for file_name in file_name_list:
            city_name = fname_to_city_name(file_name)
            file_dict[city_name] = load_file(os.path.join(folder_path, file_name))

        return file_dict

    # Else load data from all cities into a single DataFrame with shares date index.
    elif mode == 'agg':
        # Empty DataFrame to receive data.
        df = pd.DataFrame()
        # Loop through all file names.
        for file_name in file_name_list:
            # Load data into Pandas DataFrame with first row as column names and first column as index names.
            city_df = load_file(os.path.join(folder_path, file_name))
            # Change columns from month names to month numbers.
            city_df.columns = [idx+1 for idx, _ in enumerate(city_df.columns)]
            # Stack the data columns.
            stacked_df = city_df.stack()
            # Convert the index to date based on year and month, assume day 1 of the month.
            stacked_df.index = [datetime.date(i[0], i[1], 1) for i in stacked_df.index]
            # Add the city's data to the DataFrame.
            df = pd.concat([df, pd.DataFrame({file_name: stacked_df})], axis=1)

        # Sort the date index.
        df.sort_index(inplace=True)
        # Change the columns from file name to city name.
        df.columns = [fname_to_city_name(file_name) for file_name in df.columns]

        return df

    # Raise an error is another mode has been entered.
    else:
        raise KeyError(f"Mode {mode} not allowed.")