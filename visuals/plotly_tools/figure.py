import pandas as pd
import plotly.graph_objects as go

from vc.data_treat.maps import month_dict

height_standard = 600
width_standard = 1100

#TODO Set white background and remove ticklines.

def braz_cities_temp_per_year(month: int=None) -> go.Figure:
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
    fig = skeleton()
    fig.update_xaxes(title={'text': 'City'})
    fig.update_yaxes(title={'text': 'City'})
    fig.update_layout(title=f"Correlation plot for brazilian cities")

    return fig

def heatmap() -> go.Figure:
    fig = skeleton()
    fig.update_xaxes(title={'text': 'City'})
    fig.update_yaxes(title={'text': 'Datetime'})
    fig.update_layout(title=f"Temperature heatmap for brazilian cities")

    return fig

def phase_space(stat_dict: dict, outlier_series: pd.Series=None) -> go.Figure:
    if outlier_series is None:
        title=f"Temperature phase-space plot for brazilian cities"
    else:
        title=f"Temperature phase-space plot for brazilian cities with {len(outlier_series)} outliers"

    fig = skeleton()
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
        showlegend=True
    )

    return fig

def skeleton() -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        height=height_standard,
        width=width_standard,
        plot_bgcolor='#ffffff'
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    return fig