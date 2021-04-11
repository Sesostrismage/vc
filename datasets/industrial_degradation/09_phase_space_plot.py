import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

import vc.visuals.streamlit_tools as stt

stt.settings()
data_folder = r"C:/Data/one_year_industrial_component_degradation"
df = pd.read_pickle(os.path.join(data_folder, 'agg_data.pkl'))
df.columns = ['timestamp', 'pCut motor torque', 'pCut lag error', 'pCut actual position', 'pCut actual speed', 'pFilm actual position', 'pFilm actual speed', 'pFilm lag error', 'pSpintor VAX speed', 'Mode']
st.dataframe(df.head())

st.info(f"Total data size: {len(df)} rows.")

t_start = st.sidebar.number_input(
    'Choose start datetime',
    min_value=df.index[0],
    max_value=df.index[-1]
)

timespan = st.sidebar.number_input(
    'Choose number of seconds to show',
    min_value=1.,
    max_value=df.index[-1] - t_start,
    value=100.
)

x = st.sidebar.selectbox(
    'Choose x variable',
    options=df.columns,
    index=1
)

y = st.sidebar.selectbox(
    'Choose y variable',
    options=df.columns,
    index=2
)

color = st.sidebar.selectbox(
    'Choose color variable',
    options=df.columns,
    index=len(df.columns)-1
)

plot_df = df[(df.index >= t_start) & (df.index <= t_start + timespan)]

fig = go.Figure()



fig.update_layout(height=800, width=1100, hovermode='closest', showlegend=False)

fig.add_trace(
    go.Scattergl(
        x=plot_df[x],
        y=plot_df[y],
        mode='markers',
        marker={'color': plot_df[color]}
    )
)

st.plotly_chart(fig)