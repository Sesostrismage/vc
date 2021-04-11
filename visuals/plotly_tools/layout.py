import pandas as pd
import plotly.graph_objects as go

height_standard = 600
width_standard = 1100

def braz_cities_temp(fig: go.Figure, city_name: str, year: int) -> go.Figure:
    fig.update_xaxes(title={'text': 'Months'})
    fig.update_yaxes(title={'text': 'Temperature [deg C]'})
    fig.update_layout(
        title=f"Temperature for {city_name} in {year}",
        hovermode='x',
        height=height_standard,
        width=width_standard
    )

    return fig


def braz_cities_temp_all(fig: go.Figure, city_series: pd.Series) -> go.Figure:
    fig.update_xaxes(title={'text': 'Date'})
    fig.update_yaxes(title={'text': 'Temperature [deg C]'})
    fig.update_layout(
        title=f"Temperature for {city_series.name} from {str(city_series.index[0])[:-3]} to {str(city_series.index[-1])[:-3]}",
        hovermode='x',
        height=height_standard,
        width=width_standard
    )

    return fig