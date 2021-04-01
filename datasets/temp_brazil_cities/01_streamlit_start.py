import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Folder path to data files.
folder_path = r"C:/Data/temperature_time-series_for_brazilian_cities/"
# File names of each data file as a list
file_name_list = [
    'station_belem.csv',
    'station_curitiba.csv',
    'station_fortaleza.csv',
    'station_goiania.csv',
    'station_macapa.csv',
    'station_manaus.csv',
    'station_recife.csv',
    'station_rio.csv',
    'station_salvador.csv',
    'station_sao_luiz.csv',
    'station_sao_paulo.csv',
    'station_vitoria.csv'
]

file_name = st.sidebar.selectbox(
    'Choose file name',
    options=file_name_list
)

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
year_list = list(df_crop.index)
year = st.sidebar.selectbox(
    'Choose year to view',
    options=year_list
)

# Calculate the mean per month across all years for comparison.
mean = df_crop.mean()


fig = plt.figure()
# Plot data from selected year.
plt.plot(df_crop.columns, df_crop.loc[year], label=str(year))

# Plot all-time mean for comparison.
plt.plot(df_crop.columns, mean, label='Mean of all years')
plt.xlabel('Months')
plt.ylabel('Temperature [deg C]')
plt.title('Temperature for ' + file_name + ' in ' + str(year))
plt.legend()
st.pyplot(fig)