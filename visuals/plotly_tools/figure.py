import pandas as pd
import plotly.graph_objects as go

from vc.data_treat.maps import month_dict

height_standard = 600
width_standard = 1100

def braz_cities_temp_per_year(month: int=None) -> go.Figure:
    if month is not None:
        title = f"Temperature for brazilian cities in {month_dict[month]}"
    else:
        title = f"Temperature for brazilian cities"

    fig = go.Figure()
    fig.update_xaxes(title={'text': 'Months'})
    fig.update_yaxes(title={'text': 'Temperature [deg C]'})
    fig.update_layout(
        title=title,
        hovermode='x',
        height=height_standard,
        width=width_standard
    )

    return fig

def corr_map() -> go.Figure:
    fig = go.Figure()
    fig.update_xaxes(title={'text': 'City'})
    fig.update_yaxes(title={'text': 'City'})
    fig.update_layout(
        title=f"Correlation plot for brazilian cities",
        height=height_standard,
        width=width_standard
    )

    return fig

def heatmap() -> go.Figure:
    fig = go.Figure()
    fig.update_xaxes(title={'text': 'City'})
    fig.update_yaxes(title={'text': 'Datetime'})
    fig.update_layout(
        title=f"Temperature heatmap for brazilian cities",
        height=height_standard,
        width=width_standard
    )

    return fig

def phase_space(stat_dict: dict, outlier_series: pd.Series=None) -> go.Figure:
    if outlier_series is None:
        title=f"Temperature phase-space plot for brazilian cities"
    else:
        title=f"Temperature phase-space plot for brazilian cities with {len(outlier_series)} outliers"

    fig = go.Figure()
    fig.update_xaxes(
        title={'text': 'Temperature [deg C]'},
        range=[stat_dict['min_total'], stat_dict['max_total']]
    )
    fig.update_yaxes(
        title={'text': 'Temperature [deg C]'},
        range=[stat_dict['min_total'], stat_dict['max_total']]
    )
    fig.update_layout(
        title=title,
        height=height_standard,
        width=width_standard,
        showlegend=True
    )

    return fig
