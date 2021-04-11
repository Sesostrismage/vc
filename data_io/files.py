import datetime
import numpy as np
import os
import pandas as pd

from vc.data_io import files

def braz_cities_temp(file_path: str) -> pd.DataFrame:
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


def braz_cities_temp_all(folder_path: str) -> pd.DataFrame:
    # Get file name list from the folder.
    file_name_list = os.listdir(folder_path)

    df = pd.DataFrame()

    for file_name in file_name_list:
        # Load data into Pandas DataFrame with first row as column names and first column as index names.
        city_df = files.braz_cities_temp(os.path.join(folder_path, file_name))
        city_df.columns = [idx+1 for idx, _ in enumerate(city_df.columns)]
        stacked_df = city_df.stack()
        stacked_df.index = [datetime.date(i[0], i[1], 1) for i in stacked_df.index]
        df = pd.concat([df, pd.DataFrame({file_name: stacked_df})], axis=1)

    df.sort_index(inplace=True)
    df.columns = [file_name[8:-4].replace('_', ' ').title() for file_name in df.columns]

    return df