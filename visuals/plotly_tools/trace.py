import pandas as pd
import plotly.graph_objects as go
import vc.visuals.plotly_tools.hovertext as pt_hover
from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData


def braz_cities_temp(
    fig: go.Figure, plot_df: pd.DataFrame, month: int, cmap=None
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


def stat_lines(fig: go.Figure, stat_dict: dict, selection: list) -> go.Figure:
    for stat in selection:
        fig.add_trace(
            go.Scatter(x=stat_dict[stat].index, y=stat_dict[stat], name=f"All-city {stat}")
        )

    return fig
