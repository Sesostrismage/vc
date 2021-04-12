import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import streamlit as st

# Folder path to data files.
folder_path = r"C:/Data/temperature_time-series_for_brazilian_cities/"
# Get file names automatically from the folder.
file_name_list = os.listdir(folder_path)

#Selectbox to choose the file.
file_name = st.sidebar.selectbox(
    'Choose file name',
    options=file_name_list
)
# Translate into city name.
city_name = file_name[8:-4].replace('_', ' ').title()

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

# Get all available years from the file and make it into a list.
year_list = list(df_crop.index)
# Selectbox to choose the year.
year = st.sidebar.selectbox(
    'Choose year to view',
    options=year_list
)

# Calculate the mean per month across all years for comparison.
mean = df_crop.mean()

# Now you have to create a figure first.
fig = plt.figure()
# Plot data from selected year.
plt.plot(df_crop.columns, df_crop.loc[year], label=str(year))
# Plot all-time mean for comparison.
plt.plot(df_crop.columns, mean, label='Mean of all years')
plt.xlabel('Months')
plt.ylabel('Temperature [deg C]')
plt.title('Temperature for ' + city_name + ' in ' + str(year))
plt.legend()
# Show the figure in the Streamlit app.
st.pyplot(fig)