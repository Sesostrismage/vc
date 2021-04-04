import pandas as pd
import plotly.graph_objects as go

import vc.visuals.plotly_tools.hovertext as pt_hover

def braz_cities_temp(series: pd.Series, city_name: list, trace_name: str) -> go.Scatter:
    text_list = pt_hover.braz_cities_temp(series, city_name, trace_name)

    trace = go.Scatter(
        x=series.index,
        y=series,
        hoverinfo='text',
        hovertext=text_list,
        name=str(trace_name),
        mode='lines+markers'
    )

    return trace