import numpy as np
import pandas as pd

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