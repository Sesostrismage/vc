import datetime
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

import vc.visuals.plotly_tools.layout as pt_layout
import vc.visuals.streamlit_tools as stt

stt.settings()
data_folder = r"C:/Data/mining"
df = pd.read_csv(
    os.path.join(data_folder, 'MiningProcess_Flotation_Plant_Database.csv'),
    parse_dates=['date'],
    decimal=',',
    index_col=0,
    header=0
)
df.index = pd.to_datetime(df.index)
st.dataframe(df.head())

st.info(f"Total data size: {len(df)} rows.")

date_start = st.sidebar.date_input(
    'Data start date',
    min_value=df.index[0].date(),
    max_value=df.index[-1].date(),
    value=df.index[0].date()
)

date_end = st.sidebar.date_input(
    'Data start date',
    min_value=df.index[0].date(),
    max_value=df.index[-1].date(),
    value=df.index[-1].date()
)

plot_df = df[(df.index >= datetime.datetime.combine(date_start, datetime.datetime.min.time())) & (df.index <= datetime.datetime.combine(date_end, datetime.datetime.min.time()))]

options = list(df.columns)

x = st.sidebar.selectbox(
    'Choose X variable',
    options=['Datetime'] + options,
    index=0
)
if x == 'Datetime':
    x = plot_df.index
else:
    x = plot_df[x]

y = st.sidebar.selectbox(
    'Choose y variable',
    options=options,
    index=1
)

color = st.sidebar.selectbox(
    'Choose color variable',
    options=options,
    index=2
)

fig = go.Figure()

fig.add_trace(
    go.Scattergl(
        x=x,
        y=plot_df[y],
        mode='markers',
        marker={'color': plot_df[color]}
    )
)

fig.update_layout(
        height=pt_layout.height_standard,
        width=pt_layout.width_standard
    )

st.plotly_chart(fig)