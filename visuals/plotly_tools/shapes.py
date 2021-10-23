import datetime

import pandas as pd
import plotly.graph_objects as go
from vc.visuals.colors import get_color


def minmax_temp(fig: go.Figure, stat_dict: dict) -> go.Figure:
    """
    This function creates shapes to show min and max temperature
    across all cities for each date.

    Args:
        fig (go.Figure): Existing figure.
        stat_dict (dict): Dict with statistical series.

    Returns:
        go.Figure: Input figure with shapes added.
    """
    # Handle missing data.
    # Find indices where the series doesn't have null values.
    valid_idx = stat_dict["min"].notnull()
    # Use those indices to put together x and y value lists.
    x_part = list(stat_dict["min"][valid_idx].index)
    # Add the same x-coordinates in reversed order to complete the shape.
    x = x_part + list(reversed(x_part))
    # Create y-components of the shapes.
    y_mean_part = list(stat_dict["mean"][valid_idx])
    y_part = list(stat_dict["min"][valid_idx])
    y_min = y_part + list(reversed(y_mean_part))
    y_part = list(stat_dict["max"][valid_idx])
    y_max = y_part + list(reversed(y_mean_part))

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


def summer_winter(
    fig: go.Figure, data: pd.Series, stat_dict: dict, month: int = None
) -> go.Figure:
    """
    Creates shapes to show summer and winter months.

    Args:
        fig (go.Figure): Existing figure.
        data (pd.Series): Temperature data.
        stat_dict (dict): Dict with statistical variables.
        month (int, optional): Month to show, if any. Defaults to None.

    Returns:
        go.Figure: Input figure with shapes added.
    """
    # Dict to indicate which months belong to summer and winter.
    season_dict = {"Summer": [1, 2, 3, 12], "Winter": [6, 7, 8, 9]}

    # If no month is chosen, make shapes.
    if month is None:
        # Create season DataFrame to hold shape data.
        season_df = pd.DataFrame(columns=["start", "end", "season"])
        # Set starting values.
        start_date = data.index[0]
        prev_date = data.index[0]
        season = None

        # Loop through all dates.
        for date in data.index:
            # If no season is currently chosen, checkif current month
            # is in a season.
            if season is None:
                for s in season_dict:
                    if date.month in season_dict[s]:
                        season = s
                        start_date = date
            # Check if more than half year if between current and previous date.
            # If yes, assume missing data and end the season at the previous date.
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
            # If the current month is not in the currently set season, end the shape.
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

        # Handling if end-of-data when a season is ongoing.
        if season is not None:
            season_df = pd.concat(
                [
                    season_df,
                    pd.DataFrame(
                        {
                            "start": [start_date],
                            "end": [data.index[-1]],
                            "season": [season],
                        }
                    ),
                ]
            )

        # Create season color boxes.
        shape_list = []

        # Create rectangles to indicate seasons.
        if len(season_df) > 0:
            for _, row in season_df.iterrows():
                shape = go.layout.Shape(
                    type="rect",
                    x0=row["start"],
                    y0=stat_dict["min_total"],
                    x1=row["end"],
                    y1=stat_dict["max_total"],
                    line={"width": 0},
                    fillcolor=get_color("season", [row["season"]]),
                    opacity=0.25,
                    layer="below",
                )

                shape_list.append(shape)

        fig.update_layout(shapes=shape_list)

    # Else set plot background colour to the season
    # if a month is chosen and that month is in a season.
    else:
        if month in season_dict["Summer"]:
            color = "rgb(255, 196, 196)"
        elif month in season_dict["Winter"]:
            color = "rgb(196, 196, 255)"
        else:
            color = "white"

        fig.update_layout(plot_bgcolor=color)

    return fig
