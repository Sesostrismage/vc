import plotly.graph_objects as go

from vc.data_treat.maps import month_dict

# Standard width and height for figures, at the top for easy reference.
height_standard = 600
width_standard = 1100

def braz_cities_temp_per_year(month: int=None) -> go.Figure:
    """
    Standard time plot of data.

    Args:
        month (int, optional): Whether or not a specific month is chosen. Defaults to None.

    Returns:
        go.Figure: Plotly figure.
    """
    if month is not None:
        title = f"Temperature for brazilian cities in {month_dict[month]}"
    else:
        title = f"Temperature for brazilian cities"

    fig = skeleton()
    fig.update_xaxes(title={'text': 'Months'})
    fig.update_yaxes(title={'text': 'Temperature [deg C]'})
    fig.update_layout(
        title=title,
        hovermode='x'
    )
    return fig

def corr_map() -> go.Figure:
    """
    Figure for correlation plot.

    Returns:
        go.Figure: Plotly figure.
    """
    fig = skeleton()
    fig.update_xaxes(title={'text': 'City'})
    fig.update_yaxes(title={'text': 'City'})
    fig.update_layout(title=f"Correlation plot for brazilian cities")
    return fig

def heatmap() -> go.Figure:
    """
    Figure for heat map.

    Returns:
        go.Figure: Plotly figure.
    """
    fig = skeleton()
    fig.update_xaxes(title={'text': 'City'})
    fig.update_yaxes(title={'text': 'Datetime'})
    fig.update_layout(title=f"Temperature heatmap for brazilian cities")
    return fig

def phase_space(stat_dict: dict) -> go.Figure:
    """
    Figure for phase-space plot.

    Returns:
        go.Figure: Plotly figure.
    """
    fig = skeleton()
    fig.update_xaxes(range=[stat_dict['min_total'], stat_dict['max_total']])
    fig.update_yaxes(range=[stat_dict['min_total'], stat_dict['max_total']])
    return fig

def skeleton() -> go.Figure:
    """
    This is the common figure 'skeleton' used as a base for all plots
    to set up a shared visual style.

    Returns:
        go.Figure: Plotly figure.
    """
    fig = go.Figure()
    # Set standard width and height, and white background.
    fig.update_layout(
        height=height_standard,
        width=width_standard,
        plot_bgcolor='#ffffff'
    )
    axis_dict = {
        # Move ticks outside the plot.
        'ticks': 'outside',
        # Show plot borders with these four settings.
        'showline': True,
        'linewidth': 2,
        'linecolor': 'black',
        'mirror': True,
        # Remove gridlines in the plot.
        'showgrid': False
    }
    # Apply to both axes.
    fig.update_xaxes(axis_dict)
    fig.update_yaxes(axis_dict)
    return fig