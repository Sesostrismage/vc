import plotly.graph_objects as go

height_standard = 600
width_standard = 1100

def braz_cities_temp_per_year(year: int) -> go.Figure:
    fig = go.Figure()
    fig.update_xaxes(title={'text': 'Months'})
    fig.update_yaxes(title={'text': 'Temperature [deg C]'})
    fig.update_layout(
        title=f"Temperature for brazilian cities in {year}",
        hovermode='x',
        height=height_standard,
        width=width_standard
    )

    return fig
