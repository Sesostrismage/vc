import plotly.graph_objects as go

from typing import Union

height_standard = 600
width_standard = 1100

def braz_cities_temp(fig: go.Figure, city_name: str, year: int) -> go.Figure:
    fig.update_xaxes(title={'text': 'Months'})
    fig.update_yaxes(title={'text': 'Temperature [deg C]'})
    fig.update_layout(
        title=f"Temperature for {city_name} in {year}",
        hovermode='x',
        height=600,
        width=1100
    )

    return fig