import os

import pandas as pd
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import (
    Button,
    Circle,
    ColumnDataSource,
    CustomJS,
    DatetimeTickFormatter,
    Dropdown,
)
from bokeh.models.tools import BoxSelectTool
from bokeh.plotting import figure
from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData
from vc.datasets.temp_brazil_cities.labeler import CityDataLabeler
from vc.visuals.colors import get_color
from vc.visuals.plotly_tools.figure import height_standard, width_standard

####################################################################
# Utility functions.
####################################################################

# Get color series from a boolean series.
def get_color_series(in_series: pd.Series) -> pd.Series:
    out_series = in_series.map(
        {0: get_color("labeling", "default"), 1: get_color("labeling", "labeled")}
    )
    return out_series


# Get size series from a boolean series.
def get_size_series(in_series: pd.Series) -> pd.Series:
    out_series = in_series.map({0: 5, 1: 10})
    return out_series


####################################################################
# Setup and data loading.
####################################################################

# Default selection mode.
selection_mode = "Add"
# Code to reset plot view.
reset_code = """document.querySelectorAll('.bk-tool-icon-reset[title="Reset"]').forEach(d => d.click())"""
# Data dicts for initializing and resetting data source objects.
circle_data_dict = {"datetime": [], "temperature": [], "color": [], "size": []}
line_data_dict = {"datetime": [], "temperature": []}
# Get Cities data object.
city_obj = CitiesTempData()
# Extract all data.
city_df, stat_dict = city_obj.get_data()
# Initialize variables for later use.
data_dict = {}
labeled_data_bool = pd.Series()
color_series = pd.Series()
labeler = None
city_name = None

# Dropdown handler to execute code when a choice is made in the city name dropdown menu.
def city_name_dropdown_handler(event):
    # Some variables are called globally so their state can be changed from within this function.
    global city_name
    global labeler
    # Change dropdown menu name to the chosen city.
    city_name = event.item
    city_name_dropdown.label = city_name
    # Change the button type to standard.
    city_name_dropdown.button_type = "default"
    # Instantiate a labeling object.
    labeler = CityDataLabeler(city_name)
    # Update all data based on the city chosen.
    update_data()


# Dropdown menu for choosing a city.
city_name_dropdown = vessel_dropdown = Dropdown(
    label="Choose city",
    # Choices are all cities.
    menu=city_obj.get_cities(),
    # Default button type is 'warning' to show that a choice needs to be made.
    button_type="warning",
)
# When the menu is activated, call the handler above.
city_name_dropdown.on_click(city_name_dropdown_handler)
# Reset the plot view so the new data is shown properly.
city_name_dropdown.js_on_click(CustomJS(code=reset_code))

# Function to update data based on current choices.
def update_data():
    # Some variables are called globally so their state can be changed from within this function.
    global data_dict
    global labeled_data_bool
    global color_series
    global labeler
    global city_name
    global circle_source

    # Only execute if a city name is chosen.
    if city_name is not None:
        # Instantiate a labeling object with the chosen city.
        labeler = CityDataLabeler(city_name)
        # Get all existing labels for that city.
        existing_dt_list = labeler.get_datetimes()
        # Pandas Series with index from the data to match against existing labels.
        labeled_data_bool = pd.Series(0, index=city_df.index)
        for label in existing_dt_list:
            if label in labeled_data_bool.index:
                labeled_data_bool.loc[label] = 1

        # Set source data for circles that show labeling status.
        circle_source.data = {
            # Dates from the data index.
            "datetime": city_df.index,
            # Temperature from the data.
            "temperature": city_df[city_name],
            # Colour depending on the label status.
            "color": get_color_series(labeled_data_bool),
            # Currently labeled data bool.
            "labeled": labeled_data_bool,
            # Size based on labeling.
            "size": get_size_series(labeled_data_bool),
        }
        # Line plot to show the data over time irrespective of tagging.
        line_source.data = {
            "datetime": city_df.index,
            "temperature": city_df[city_name],
        }
        fig.title.text = f"{city_name}"
        fig.title.background_fill_color = "#ffffff"


# Instantiate data source for circle plot with empty data.
circle_source = ColumnDataSource(data=circle_data_dict)
circle_source.name = "Circles"
# Instantiate data source for line plot with empty data.
line_source = ColumnDataSource(data=line_data_dict)
line_source.name = "Lines"

# Create the figure with formatting and plot tools.
fig = figure(
    title="Density plot",
    tools="box_zoom,reset",
    x_axis_type="datetime",
    plot_width=width_standard,
    plot_height=height_standard,
)
axis_format_str = "%y-%m-%d %H:%M"
fig.xaxis.formatter = DatetimeTickFormatter(
    days=axis_format_str,
    months=axis_format_str,
    hours=axis_format_str,
    minutes=axis_format_str,
)
# Add temperature as a line plot for reference.
temp_lines = fig.line(
    "datetime", "temperature", line_color="black", source=line_source, name="temp_line"
)
# Add temperature as a circle plot to show label status.
temp_circles = fig.circle(
    "datetime",
    "temperature",
    line_color=None,
    fill_color="color",
    source=circle_source,
    size="size",
    name="temp_circles",
)
# selection_glyph determines how the data points look when selected in the plot.
temp_circles.selection_glyph = Circle(
    size=10,
    fill_alpha=1,
    fill_color=get_color("labeling", selection_mode),
    line_color=None,
)
# nonselection_glyph determines how the data points look when not selected in the plot.
temp_circles.nonselection_glyph = Circle(
    fill_alpha=1, fill_color="color", line_color=None
)
# Add a box select tool that only affect the circle plot
box_select_tool = BoxSelectTool(renderers=[temp_circles])
fig.add_tools(box_select_tool)
# Set the box select tool as the active tool.
fig.toolbar.active_drag = box_select_tool

# Handler for when changing the selection mode.
def select_mode_dropdown_handler(event):
    global selection_mode

    selection_mode = event.item
    # Change the color of selected circles to match the selection mode.
    temp_circles.selection_glyph.update(
        fill_color=get_color("labeling", selection_mode)
    )
    # Update the dropdown label to show the selection mode.
    select_mode_dropdown.label = f"Selection mode: {selection_mode}"
    # Update the button type to show the selection mode.
    if selection_mode == "Add":
        select_mode_dropdown.button_type = "success"
    else:
        select_mode_dropdown.button_type = "danger"


# Dropdown to choose whether to add or remove selected points from the labels.
select_mode_dropdown = Dropdown(
    label=f"Selection mode: {selection_mode}",
    menu=["Add", "Remove"],
    button_type="success",
)
select_mode_dropdown.on_click(select_mode_dropdown_handler)

# Handler to interact with the labeler object when a label update is chosen.
def update_labels_handler(event):
    global update_labels_button
    global data_dict
    global circle_source
    global labeled_data_bool

    # Get a list of all dates that are selected in the plot.
    tag_dt_list = list(labeled_data_bool.iloc[circle_source.selected.indices].index)

    # If selection is 'add', add these dates to the labels.
    if selection_mode == "Add":
        labeler.insert_datetimes(tag_dt_list)
    # Else remove them.
    else:
        labeler.remove_datetimes(tag_dt_list)

    # Update the visual presentation to match the new labels.
    if selection_mode == "Add":
        labeled_data_bool.iloc[circle_source.selected.indices] = 1
    else:
        labeled_data_bool.iloc[circle_source.selected.indices] = 0

    circle_source.data["labeled"] = labeled_data_bool
    circle_source.data["color"] = get_color_series(labeled_data_bool)
    circle_source.data["size"] = get_size_series(labeled_data_bool)
    # Reset selection.
    circle_source.selected.indices = []


update_labels_button = Button(label="Update tags", button_type="primary")
update_labels_button.on_click(update_labels_handler)

# Create the layout of the page.
curdoc().add_root(
    row(
        column(city_name_dropdown, select_mode_dropdown, update_labels_button,),
        column(fig),
    )
)
curdoc().title = os.path.basename(__file__)
