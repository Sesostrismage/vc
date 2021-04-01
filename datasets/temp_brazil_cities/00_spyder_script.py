import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Folder path to data files.
folder_path = r"C:/Data/temperature_time-series_for_brazilian_cities/"
# File names of each data file. Uncomment to choose a specific file.
# file_name = 'station_belem.csv'
# file_name = 'station_curitiba.csv'
# file_name = 'station_fortaleza.csv'
# file_name = 'station_goiania.csv'
# file_name = 'station_macapa.csv'
# file_name = 'station_manaus.csv'
# file_name = 'station_recife.csv'
file_name = 'station_rio.csv'
# file_name = 'station_salvador.csv'
# file_name = 'station_sao_luiz.csv'
# file_name = 'station_sao_paulo.csv'
# file_name = 'station_vitoria.csv'

# Load data into Pandas DataFrame with first row as column names and first column as index names.
df = pd.read_csv(
    folder_path + file_name,
    header=0,
    index_col=0
)

# Remove pre-generated average columns.
df_crop = df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
# Set erroneous values to NaN so they don't disturb the results.
df_crop[df_crop > 100] = np.nan

# Set the year you want to look at.
year = 1977
# Calculate the mean per month across all years for comparison.
mean = df_crop.mean()

# Plot data from selected year.
plt.plot(df_crop.columns, df_crop.loc[year], label=str(year))
# Plot all-time mean for comparison.
plt.plot(df_crop.columns, mean, label='Mean of all years')
plt.xlabel('Months')
plt.ylabel('Temperature [deg C]')
plt.title('Temperature for ' + file_name + ' in ' + str(year))
plt.legend()
plt.show()