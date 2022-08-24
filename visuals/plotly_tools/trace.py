import datetime
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


def season_shapes(
    fig: go.Figure, plot_df: pd.DataFrame, month: int = None
) -> go.Figure:
    # Dict of which months belong to summer and winter.
    season_dict = {"summer": [1, 2, 3, 12], "winter": [6, 7, 8, 9]}

    if month is None:
        # Empty DataFrame to take info on season shapes.
        season_df = pd.DataFrame(columns=["start", "end", "season"])

        # Prepare for loop.
        start_date = plot_df.index[0]
        prev_date = plot_df.index[0]
        season = None

        # Loop through all dates.
        for date in plot_df.index:
            # If season is None, check if current month is in either season.
            if season is None:
                for s in season_dict:
                    if date.month in season_dict[s]:
                        season = s
                        start_date = date
            # If the date gap is too large due to missing data,
            # end the season at the previous date.
            elif date - prev_date > datetime.timedelta(weeks=26):
                season_df = pd.concat(
                    [
                        season_df,
                        pd.DataFrame(
                            {
                                "start": [start_date],
                                "end": [prev_date],
                                "season": [season],
                            }
                        ),
                    ]
                )
                season = None
            # If the month is not in a season, end the season.
            elif date.month not in season_dict[season]:
                season_df = pd.concat(
                    [
                        season_df,
                        pd.DataFrame(
                            {"start": [start_date], "end": [date], "season": [season]}
                        ),
                    ]
                )
                season = None

            prev_date = date

        # Handling if the data ends in a season.
        if season is not None:
            season_df = pd.concat(
                [
                    season_df,
                    pd.DataFrame(
                        {
                            "start": [start_date],
                            "end": [plot_df.index[-1]],
                            "season": [season],
                        }
                    ),
                ]
            )

        # Create season color boxes.
        shape_list = []

        y_min = plot_df.min().min()
        y_max = plot_df.max().max()

        # Create rectangles to indicate seasons.
        if len(season_df) > 0:
            for _, row in season_df.iterrows():
                shape = go.layout.Shape(
                    type="rect",
                    x0=row["start"],
                    y0=y_min,
                    x1=row["end"],
                    y1=y_max,
                    line={"width": 0},
                    fillcolor=get_color("seasons", row["season"]),
                    opacity=0.25,
                    layer="below",
                )

                shape_list.append(shape)

        fig.update_layout(shapes=shape_list)

    # Else set plot background colour to the season.
    else:
        if month in season_dict["summer"]:
            color = "rgb(255, 196, 196)"
        elif month in season_dict["winter"]:
            color = "rgb(196, 196, 255)"
        else:
            color = "white"

        fig.update_layout(plot_bgcolor=color)

    return fig
