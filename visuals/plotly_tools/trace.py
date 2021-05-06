import pandas as pd
import plotly.graph_objects as go

import vc.visuals.plotly_tools.hovertext as pt_hover

def braz_cities_temp(
    fig: go.Figure,
    plot_df: pd.DataFrame,
    city_name: str,
    month: int,
    cmap
) -> go.Figure:
    """
    Creates line traces for standard time plot.

    Args:
        fig (go.Figure): Existing Plotly figure.
        plot_df (pd.DataFrame): Temperature data.
        city_name (str): Name of the city to plot.
        month (int): Month to plot, if any.
        cmap ([type]): Colormap.

    Returns:
        fig (go.Figure): The input figure with a trace added.
    """
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
