import pandas as pd
import plotly.graph_objects as go
import vc.visuals.plotly_tools.hovertext as pt_hover
from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData


def braz_cities_temp(
    fig: go.Figure, city_data: CitiesTempData, month: int, cmap=None
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
    plot_df, _ = city_data.get_data(selection_only=True, month=month)

    for city_name in plot_df.columns:
        text_list = pt_hover.braz_cities_temp(plot_df, city_name, month)

        if cmap is None:
            fig.add_trace(
                go.Scattergl(
                    x=plot_df.index,
                    y=plot_df[city_name],
                    hoverinfo="text",
                    hovertext=text_list,
                    name=city_name,
                )
            )
        else:
            fig.add_trace(
                go.Scattergl(
                    x=plot_df.index,
                    y=plot_df[city_name],
                    hoverinfo="text",
                    hovertext=text_list,
                    line={"color": cmap[city_name]},
                    name=city_name,
                )
            )

    return fig


def braz_cities_temp_old_style(fig: go.Figure, plot_df: pd.DataFrame) -> go.Figure:
    # Plot all selected cities.
    for city_name in plot_df.columns:
        fig.add_trace(
            go.Scattergl(
                x=plot_df.index,
                y=plot_df[city_name],
                name=city_name,
            )
        )
    return fig


def mean_series(fig: go.Figure, mean_series: pd.Series) -> go.Figure:
    fig.add_trace(go.Scatter(x=mean_series.index, y=mean_series, name="All-city mean"))
    return fig
