import plotly.graph_objects as go

from vc.data_treat.maps import month_dict

height_standard = 600
width_standard = 1100

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

# Axis labels and title to reflect chosen cities.
def phase_space(stat_dict: dict) -> go.Figure:
    fig = skeleton()
    fig.update_xaxes(range=[stat_dict['min_total'], stat_dict['max_total']])
    fig.update_yaxes(range=[stat_dict['min_total'], stat_dict['max_total']])

    return fig

def skeleton() -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        height=height_standard,
        width=width_standard,
        plot_bgcolor='#ffffff'
    )
    axis_dict = {
        'ticks': 'outside',
        'showline': True,
        'linewidth': 2,
        'linecolor': 'black',
        'mirror': True,
        'showgrid': False
    }
    fig.update_xaxes(axis_dict)
    fig.update_yaxes(axis_dict)

    return fig