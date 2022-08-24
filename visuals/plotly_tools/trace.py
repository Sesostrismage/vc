import pandas as pd
import plotly.graph_objects as go
import vc.visuals.plotly_tools.hovertext as pt_hover
from vc.visuals.colors import get_color


def braz_cities_temp(
    fig: go.Figure, plot_df: pd.DataFrame, month: int, cmap=None
) -> go.Figure:
    """
    Creates line traces for standard time plot.

    Args:
        fig (go.Figure): Existing Plotly figure.
        plot_df (pd.DataFrame): Temperature data.
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


def stat_lines(
    fig: go.Figure, stat_dict: dict, selection: list, discreet_stats: bool = False
) -> go.Figure:
    # This sets the opacity of the reference lines.
    if discreet_stats:
        opacity = 0.25
    else:
        opacity = 1

    for stat in selection:
        fig.add_trace(
            go.Scatter(
                x=stat_dict[stat].index,
                y=stat_dict[stat],
                line={"color": get_color("temperature", stat)},
                opacity=opacity,
                name=f"All-city {stat}",
            )
        )

    return fig


def stat_shapes(fig, stat_dict: dict) -> go.Figure:
    # Handle missing data.
    # Find indices where the series doesn't have null values.
    valid_idx = stat_dict["mean"].notnull().index
    # Use those indices to put together x and y value lists.
    # Add all indices again in reverse order to create a bounded figure.
    x = list(valid_idx) + list(reversed(valid_idx))

    # Build the min shape from the mean and min series.
    y_min = list(stat_dict["mean"].loc[valid_idx]) + list(
        reversed(stat_dict["min"].loc[valid_idx])
    )

    # Build the max shape from the mean and max series.
    y_max = list(stat_dict["mean"].loc[valid_idx]) + list(
        reversed(stat_dict["max"].loc[valid_idx])
    )

    # Plot the min and max areas as filled polygons.
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_min,
            fill="toself",
            mode="none",
            marker={"color": get_color("temperature", "min")},
            showlegend=False,
            hoverinfo="none",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y_max,
            fill="toself",
            mode="none",
            marker={"color": get_color("temperature", "max")},
            showlegend=False,
            hoverinfo="none",
        )
    )

    return fig
