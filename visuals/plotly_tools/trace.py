import pandas as pd
import plotly.graph_objects as go

from vc.visuals.colors import get_color
import vc.visuals.plotly_tools.hovertext as pt_hover

def braz_cities_temp(
    fig: go.Figure,
    plot_df: pd.DataFrame,
    city_name: str,
    month: int,
    cmap
):
    text_list = pt_hover.braz_cities_temp(plot_df, city_name, month)

    fig.add_trace(go.Scattergl(
        x=plot_df.index,
        y=plot_df[city_name],
        hoverinfo='text',
        hovertext=text_list,
        line={'color': cmap[city_name]},
        name=city_name
    ))

    return fig


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
