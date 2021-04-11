import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

import vc.visuals.streamlit_tools as stt

stt.settings()
data_folder = r"C:/Data/one_year_industrial_component_degradation"
df = pd.read_pickle(os.path.join(data_folder, 'agg_data.pkl'))
st.dataframe(df.head())

t_start = st.sidebar.number_input(
    'Choose start time',
    min_value=df.index[0],
    max_value=df.index[-1]
)

timespan = st.sidebar.number_input(
    'Choose number of seconds to show',
    min_value=1.,
    max_value=df.index[-1] - t_start,
    value=100.
)

plot_df = df[(df.index >= t_start) & (df.index <= t_start + timespan)]

fig = make_subplots(
    rows=len(plot_df.columns),
    cols=2,
    column_widths=[0.8, 0.2]
)

for idx, col in enumerate(plot_df.columns):
    fig.add_trace(
        go.Scattergl(
            x=plot_df.index,
            y=plot_df[col],
            name=col
        ),
        row=idx+1,
        col=1
    )

    fig.add_trace(go.Histogram(y=plot_df[col]), row=idx+1, col=2)

fig.update_layout(height=2500, width=1100, hovermode='x', showlegend=False)

st.plotly_chart(fig)