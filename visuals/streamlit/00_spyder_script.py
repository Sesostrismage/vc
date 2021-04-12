import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Folder path to data files.
folder_path = r"C:/Data/temperature_time-series_for_brazilian_cities/"

# Load data into Pandas DataFrame with first row as column names and first column as index names.
belem_df = pd.read_csv(folder_path + 'station_belem.csv', header=0, index_col=0)
# Remove pre-generated average columns.
belem_df = belem_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
# Set erroneous values to NaN so they don't disturb the results.
belem_df[belem_df > 100] = np.nan

curitiba_df = pd.read_csv(folder_path + 'station_curitiba.csv', header=0, index_col=0)
curitiba_df = curitiba_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
curitiba_df[curitiba_df > 100] = np.nan

fortaleza_df = pd.read_csv(folder_path + 'station_fortaleza.csv', header=0, index_col=0)
fortaleza_df = fortaleza_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
fortaleza_df[fortaleza_df > 100] = np.nan

goiania_df = pd.read_csv(folder_path + 'station_goiania.csv', header=0, index_col=0)
goiania_df = goiania_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
goiania_df[goiania_df > 100] = np.nan

macapa_df = pd.read_csv(folder_path + 'station_macapa.csv', header=0, index_col=0)
macapa_df = macapa_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
macapa_df[macapa_df > 100] = np.nan

manaus_df = pd.read_csv(folder_path + 'station_manaus.csv', header=0, index_col=0)
manaus_df = manaus_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
manaus_df[manaus_df > 100] = np.nan

recife_df = pd.read_csv(folder_path + 'station_recife.csv', header=0, index_col=0)
recife_df = recife_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
recife_df[recife_df > 100] = np.nan

rio_df = pd.read_csv(folder_path + 'station_rio.csv', header=0, index_col=0)
rio_df = rio_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
rio_df[rio_df > 100] = np.nan

salvador_df = pd.read_csv(folder_path + 'station_salvador.csv', header=0, index_col=0)
salvador_df = salvador_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
salvador_df[salvador_df > 100] = np.nan

sao_luiz_df = pd.read_csv(folder_path + 'station_sao_luiz.csv', header=0, index_col=0)
sao_luiz_df = sao_luiz_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
sao_luiz_df[sao_luiz_df > 100] = np.nan

sao_paulo_df = pd.read_csv(folder_path + 'station_sao_paulo.csv', header=0, index_col=0)
sao_paulo_df = sao_paulo_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
sao_paulo_df[sao_paulo_df > 100] = np.nan

vitoria_df = pd.read_csv(folder_path + 'station_vitoria.csv', header=0, index_col=0)
vitoria_df = vitoria_df.drop(['D-J-F', 'M-A-M', 'J-J-A', 'S-O-N', 'metANN'], axis=1)
vitoria_df[vitoria_df > 100] = np.nan

# Set the year you want to look at.
year = 1977
# Calculate the mean per month across all years for comparison.
mean = belem_df.mean()

# Create figure.
plt.figure()
# Plot cities data from selected year.
if year in belem_df.index:
    plt.plot(belem_df.columns, belem_df.loc[year], label='Belem')
if year in curitiba_df.index:
    plt.plot(curitiba_df.columns, curitiba_df.loc[year], label='Curitiba')
if year in fortaleza_df.index:
    plt.plot(fortaleza_df.columns, fortaleza_df.loc[year], label='Fortaleza')
if year in goiania_df.index:
    plt.plot(goiania_df.columns, goiania_df.loc[year], label='Goiania')
if year in macapa_df.index:
    plt.plot(macapa_df.columns, macapa_df.loc[year], label='Macaba')
# if year in manaus_df.index:
#     plt.plot(manaus_df.columns, manaus_df.loc[year], label='Manaus')
# if year in recife_df.index:
#     plt.plot(recife_df.columns, recife_df.loc[year], label='Recife')
# if year in rio_df.index:
#     plt.plot(rio_df.columns, rio_df.loc[year], label='Rio')
# if year in salvador_df.index:
#     plt.plot(salvador_df.columns, salvador_df.loc[year], label='Salvador')
if year in sao_luiz_df.index:
    plt.plot(sao_luiz_df.columns, sao_luiz_df.loc[year], label='Sao Luiz')
if year in sao_paulo_df.index:
    plt.plot(sao_paulo_df.columns, sao_paulo_df.loc[year], label='Sao Paulo')
if year in vitoria_df.index:
    plt.plot(vitoria_df.columns, vitoria_df.loc[year], label='Vitoria')
plt.xlabel('Months')
plt.ylabel('Temperature [deg C]')
plt.title('Temperature for brazilian cities in ' + str(year))
plt.legend()
plt.show()