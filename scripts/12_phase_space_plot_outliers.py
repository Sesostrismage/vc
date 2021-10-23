import os

import plotly.graph_objects as go
import streamlit as st
import vc.visuals.plotly_tools.figure as pt_figure
from vc.datasets.temp_brazil_cities.cities_data import CitiesTempData

####################################################################
# Setup and data loading.
####################################################################

# Standard Streamlit settings.
st.set_page_config(layout="wide")
# Title becomes the file name for easy reference to the presentation.
st.title(os.path.basename(__file__))
# Object with city temp data.
city_data = CitiesTempData()


####################################################################
# User input and calculations.
####################################################################

# Select cities for the x- and y-axes.
city_x = st.sidebar.selectbox(
    "Select x-axis city", options=city_data.get_cities(selection_only=False), key="x"
)
city_y = st.sidebar.selectbox(
    "Select y-axis city",
    options=city_data.get_cities(selection_only=False),
    key="y",
    index=1,
)

# Select if the color is set by a city or outlier detection.
color_option = st.sidebar.selectbox(
    "Color option", options=["City", "Outlier detection"]
)

# If city, choose city and get data.
if color_option == "City":
    city_color = st.sidebar.selectbox(
        "Select color city",
        options=city_data.get_cities(selection_only=False),
        key="c",
        index=2,
    )

    city_data.set_city_selection([city_x, city_y, city_color])
    plot_df, stat_dict = city_data.get_data()
    # Remove rows where data is missing from any of the cities.
    plot_df.dropna(how="any", axis=0, inplace=True)

# Else...
elif color_option == "Outlier detection":
    city_data.set_city_selection([city_x, city_y])
    plot_df, stat_dict = city_data.get_data()
    # Remove rows where data is missing from any of the cities.
    plot_df.dropna(how="any", axis=0, inplace=True)

    # Set outlier tolerance via slider.
    outlier_tolerance = st.sidebar.slider(
        "Outlier tolerance", min_value=0.0, max_value=1.0, step=0.01, value=1.0
    )
    # Outlier calculation based on ratio of difference between x and y value.
    outlier_bool = (plot_df[city_y] - plot_df[city_x]).abs() / plot_df[
        city_x
    ] > outlier_tolerance
    # Make plot series for inliers and outliers.
    inlier_x = plot_df.loc[~outlier_bool, city_x]
    inlier_y = plot_df.loc[~outlier_bool, city_y]
    outlier_x = plot_df.loc[outlier_bool, city_x]
    outlier_y = plot_df.loc[outlier_bool, city_y]


####################################################################
# Plotting.
####################################################################

# Base figure is common to both options.
fig = pt_figure.phase_space(stat_dict)

if color_option == "City":
    text_list = [
        f"{idx}<br>"
        + f"{city_x}: {plot_df.loc[idx, city_x]} deg C<br>"
        + f"{city_y}: {plot_df.loc[idx, city_y]} deg C<br>"
        + f"{city_color}: {plot_df.loc[idx, city_color]} deg C<br>"
        for idx, _ in plot_df.iterrows()
    ]

    fig.add_trace(
        go.Scattergl(
            x=plot_df[city_x],
            y=plot_df[city_y],
            hoverinfo="text",
            hovertext=text_list,
            mode="markers",
            marker={"color": plot_df[city_color]},
            name="Temperatures",
        )
    )
    fig.update_layout(title={"text": f"{city_x} vs. {city_y} coloured by {city_color}"})

# If outlier detection, plot inliers and outliers as separate traces with different colours.
elif color_option == "Outlier detection":
    text_list = [
        f"{idx}<br>"
        + f"{city_x}: {inlier_x.loc[idx]} deg C<br>"
        + f"{city_y}: {inlier_y.loc[idx]} deg C<br>"
        + f"Inlier<br>"
        + f"Outlier degree: {round(((inlier_y - inlier_x).abs()/inlier_x).loc[idx], 2)}<br>"
        for idx, _ in inlier_x.iteritems()
    ]

    fig.add_trace(
        go.Scattergl(
            x=inlier_x,
            y=inlier_y,
            hoverinfo="text",
            hovertext=text_list,
            mode="markers",
            marker={"color": "lime"},
            name="Inliers",
        )
    )

    text_list = [
        f"{idx}<br>"
        + f"{city_x}: {outlier_x.loc[idx]} deg C<br>"
        + f"{city_y}: {outlier_y.loc[idx]} deg C<br>"
        + f"Outlier<br>"
        + f"Outlier degree: {round(((outlier_y - outlier_x).abs()/outlier_x).loc[idx], 2)}<br>"
        for idx, _ in outlier_x.iteritems()
    ]

    fig.add_trace(
        go.Scattergl(
            x=outlier_x,
            y=outlier_y,
            hoverinfo="text",
            hovertext=text_list,
            mode="markers",
            marker={"color": "red"},
            name="Outliers",
        )
    )
    fig.update_layout(
        title={
            "text": f"{city_x} vs. {city_y} with {len(outlier_x)} outliers out of {len(plot_df)} data points @{outlier_tolerance} tolerance"
        }
    )

fig.update_xaxes(title={"text": f"{city_x} temperature [deg C]"})
fig.update_yaxes(title={"text": f"{city_y} temperature [deg C]"})
st.plotly_chart(fig)
