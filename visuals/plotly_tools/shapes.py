import plotly.graph_objects as go

from vc.visuals.colors import get_color

def minmax_temp(fig: go.Figure, stat_dict: dict) -> go.Figure:
    # Handle missing data.
    # Find indices where the series doesn't have null values.
    valid_idx = stat_dict['min'].notnull()
    # Use those indices to put together x and y value lists.
    x_part = list(stat_dict['min'][valid_idx].index)
    # Add the same x-coordinates in reversed order to complete the shape.
    x = x_part + list(reversed(x_part))

    y_mean_part = list(stat_dict['mean'][valid_idx])

    y_part = list(stat_dict['min'][valid_idx])
    y_min = y_part + list(reversed(y_mean_part))
    y_part = list(stat_dict['max'][valid_idx])
    y_max = y_part + list(reversed(y_mean_part))

    # Plot the min and max areas as filled polygons.
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