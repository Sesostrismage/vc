import pandas as pd
import plotly.graph_objects as go

from vc.visuals.colors import get_color
import vc.visuals.plotly_tools.hovertext as pt_hover

def braz_cities_temp_v1(series: pd.Series, city_name: list, trace_name: str) -> go.Scatter:
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


def braz_cities_temp_v2(
    series: pd.Series,
    city_name: list,
    trace_name: str,
    cat1: str,
    cat2: str,
    background: bool=False,
    ref_df: pd.DataFrame=None
) -> go.Scatter:
    text_list = pt_hover.braz_cities_temp(
        series,
        city_name,
        trace_name,
        ref_df=ref_df
    )


    color = get_color(cat1, cat2)

    if background:
        opacity = 0.25
    else:
        opacity = 1

    trace = go.Scatter(
        x=series.index,
        y=series,
        hoverinfo='text',
        hovertext=text_list,
        name=str(trace_name),
        mode='lines+markers',
        line={'color': color},
        marker={'color': color},
        opacity=opacity
    )

    return trace


def minmax_shapes(
    fig: go.Figure,
    df: pd.DataFrame,
    axis: int=0
):

    if axis == 0:
        x = list(df.columns) + list(df.columns[::-1])
    else:
        x = list(df.index) + list(df.index[::-1])

    y_min = list(df.min(axis=axis)) + list(df.mean(axis=axis)[::-1])
    y_max = list(df.max(axis=axis)) + list(df.mean(axis=axis)[::-1])

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_min,
            fill='toself',
            mode='none',
            marker={'color': get_color('temperature', 'min')},
            showlegend=False,
            hoverinfo='none'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_max,
            fill='toself',
            mode='none',
            marker={'color': get_color('temperature', 'max')},
            showlegend=False,
            hoverinfo='none'
        )
    )

    return fig