import datetime
import os
import pandas as pd

folder = r"C:/Data/one_year_industrial_component_degradation"
raw_data_folder = os.path.join(folder, 'raw_data')

raw_file_list = os.listdir(raw_data_folder)

start_dt = datetime.datetime(2020, 1, 1)

for fn in os.listdir(raw_data_folder):
    print(fn)
    month = int(fn[0:2])
    day = int(fn[3:5])
    hour = int(fn[6:8])
    minute = int(fn[8:10])
    second = int(fn[10:12])
    delta = datetime.timedelta(days=30*month + day, hours=hour, minutes=minute, seconds=second)
    print(delta)
    mode = int(fn[-5])

    if fn == raw_file_list[0]:
        df = pd.read_csv(
            os.path.join(raw_data_folder, fn),
            header=0
        )
        df['mode'] = mode
        df.index = start_dt + delta + pd.to_timedelta(df['timestamp'], unit='s')
    else:
        file_df = pd.read_csv(
            os.path.join(raw_data_folder, fn),
            header=0
        )
        file_df.index = start_dt + delta + pd.to_timedelta(file_df['timestamp'], unit='s')
        file_df['mode'] = mode

        df = pd.concat([df, file_df])

print(df.tail())

df.to_pickle(os.path.join(folder, 'agg_data.pkl'))
df.to_csv(os.path.join(folder, 'agg_data.txt'))