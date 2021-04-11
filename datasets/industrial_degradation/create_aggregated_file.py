import os
import pandas as pd

folder = r"C:/Data/one_year_industrial_component_degradation"
raw_data_folder = os.path.join(folder, 'raw_data')

raw_file_list = os.listdir(raw_data_folder)


for file_name in os.listdir(raw_data_folder):
    print(file_name)
    mode = int(file_name[-5])

    if file_name == raw_file_list[0]:
        df = pd.read_csv(
            os.path.join(raw_data_folder, file_name),
            index_col=0,
            header=0
        )
        df['mode'] = mode
    else:
        file_df = pd.read_csv(
            os.path.join(raw_data_folder, file_name),
            index_col=0,
            header=0
        )
        file_df.index = file_df.index + df.index[-1]
        file_df['mode'] = mode

        df = pd.concat([df, file_df])

print(df.tail())

df.to_pickle(os.path.join(folder, 'agg_data.pkl'))
df.to_csv(os.path.join(folder, 'agg_data.txt'))