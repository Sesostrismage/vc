import datetime
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

import vc.visuals.plotly_tools.layout as pt_layout
import vc.visuals.streamlit_tools as stt

stt.settings()
data_folder = r"C:/Data/spotify"
df = pd.read_csv(
    os.path.join(data_folder, 'data.csv'),
    index_col=0,
    header=0,
    low_memory=False
)

df.drop('release_date', axis=1, inplace=True)
st.dataframe(df.head())
st.write(df.dtypes)

st.info(f"Total data size: {len(df)} rows.")

options = list(df.select_dtypes(exclude=['object']).columns)

x = st.sidebar.selectbox(
    'Choose X variable',
    options=options,
    index=0
)

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
        x=df[x],
        y=df[y],
        mode='markers',
        marker={'color': df[color]}
    )
)

fig.update_layout(
        height=pt_layout.height_standard,
        width=pt_layout.width_standard
    )

st.plotly_chart(fig)