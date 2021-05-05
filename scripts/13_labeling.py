import os
import pandas as pd

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import Button, Circle, CustomJS, Dropdown, ColumnDataSource, DatetimeTickFormatter
from bokeh.models.tools import BoxSelectTool
from bokeh.plotting import figure

from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData
from vc.datasets.temp_brazil_cities.labeler import CityDataLabeler
from vc.visuals.colors import get_color
from vc.visuals.plotly_tools.figure import height_standard, width_standard

####################################################################
# Utility functions.
####################################################################

def get_color_series(in_series: pd.Series) -> pd.Series:
    out_series = in_series.map(
        {0: get_color('labeling', 'default'), 1: get_color('labeling', 'tagged')}
    )

    return out_series

def get_size_series(in_series: pd.Series) -> pd.Series:
    out_series = in_series.map({0: 5, 1: 10})

    return out_series

####################################################################
# Setup and data loading.
####################################################################

selection_mode = 'Add'

reset_code = """document.querySelectorAll('.bk-tool-icon-reset[title="Reset"]').forEach(d => d.click())"""

circle_data_dict = {'datetime': [], 'temperature': [], 'color': [], 'size': []}
line_data_dict = {'datetime': [], 'temperature': []}

city_obj = CitiesTempData()
city_df, stat_dict = city_obj.get_data()
data_dict = {}
tag_series = pd.Series()
color_series = pd.Series()
remove_dt_list = []
labeler = None
city_name = None

def city_name_dropdown_handler(event):
    global city_name
    global labeler

    city_name = event.item
    city_name_dropdown.label = city_name
    city_name_dropdown.button_type = 'default'
    labeler = CityDataLabeler(city_name)
    update_data()

city_name_dropdown = vessel_dropdown = Dropdown(
    label='Choose city',
    menu=city_obj.get_cities(),
    button_type='warning'
)
city_name_dropdown.on_click(city_name_dropdown_handler)
city_name_dropdown.js_on_click(CustomJS(code=reset_code))

def update_data():
    global data_dict
    global tag_series
    global color_series
    global labeler
    global city_name
    global circle_source
    global remove_dt_list

    if city_name is not None:
        labeler = CityDataLabeler(city_name)
        existing_dt_list = labeler.get_datetimes()

        tag_series = pd.Series(0, index=city_df.index)
        # Set label series and eliminate any tags not in the data.
        remove_dt_list = []

        for label in existing_dt_list:
            if label in tag_series.index:
                tag_series.loc[label] = 1
            else:
                remove_dt_list.append(label)

        circle_source.data = {
            'datetime': city_df.index,
            'temperature': city_df[city_name],
            'color': get_color_series(tag_series),
            'tagged': tag_series,
            'size': get_size_series(tag_series)
        }
        line_source.data = {
            'datetime': city_df.index,
            'temperature': city_df[city_name]
        }

        fig.title.text = f"{city_name}"
        fig.title.background_fill_color = "#ffffff"

circle_source = ColumnDataSource(data = circle_data_dict)
circle_source.name = 'Circles'
line_source = ColumnDataSource(data = line_data_dict)
line_source.name = 'Lines'

fig = figure(
    title='Density plot',
    tools="box_zoom,reset",
    x_axis_type='datetime',
    plot_width=width_standard,
    plot_height=height_standard
)
axis_format_str = "%y-%m-%d %H:%M"
fig.xaxis.formatter=DatetimeTickFormatter(
    days=axis_format_str,
    months=axis_format_str,
    hours=axis_format_str,
    minutes=axis_format_str
)

temp_lines = fig.line(
    'datetime',
    'temperature',
    line_color='black',
    source=line_source,
    name='temp_line'
)
temp_circles = fig.circle(
    'datetime',
    'temperature',
    line_color=None,
    fill_color='color',
    source=circle_source,
    size='size',
    name='temp_circles'
)
temp_circles.selection_glyph = Circle(
    size=10,
    fill_alpha=1,
    fill_color=get_color('labeling', selection_mode),
    line_color=None
)
temp_circles.nonselection_glyph = Circle(
    fill_alpha=1,
    fill_color='color',
    line_color=None
)
box_select_tool = BoxSelectTool(renderers=[temp_circles])
fig.add_tools(box_select_tool)
fig.toolbar.active_drag = box_select_tool

def select_mode_dropdown_handler(event):
    global selection_mode

    selection_mode = event.item
    temp_circles.selection_glyph.update(fill_color=get_color('labeling', selection_mode))
    select_mode_dropdown.label = f"Selection mode: {selection_mode}"

    if selection_mode == 'Add':
        select_mode_dropdown.button_type = 'success'
    else:
        select_mode_dropdown.button_type = 'danger'

select_mode_dropdown = Dropdown(
    label=f"Selection mode: {selection_mode}",
    menu=['Add', 'Remove'],
    button_type='success'
)
select_mode_dropdown.on_click(select_mode_dropdown_handler)

def update_labels_handler(event):
    global update_labels_button
    global data_dict
    global circle_source
    global tag_series

    if selection_mode == 'Add':
        tag_series.iloc[circle_source.selected.indices] = 1
    else:
        tag_series.iloc[circle_source.selected.indices] = 0

    tag_dt_list = list(tag_series.iloc[circle_source.selected.indices].index)

    if selection_mode == 'Add':
        labeler.insert_datetimes(tag_dt_list)
    else:
        labeler.remove_datetimes(tag_dt_list)

    circle_source.data['tagged'] = tag_series
    circle_source.data['color'] = get_color_series(tag_series)
    circle_source.data['size'] = get_size_series(tag_series)

    circle_source.selected.indices = []

update_labels_button = Button(label='Update tags', button_type='primary')
update_labels_button.on_click(update_labels_handler)

curdoc().add_root(
    row(
        column(
            city_name_dropdown,
            select_mode_dropdown,
            update_labels_button,
        ),
        column(
            fig
        )
    )
)
curdoc().title = os.path.basename(__file__)