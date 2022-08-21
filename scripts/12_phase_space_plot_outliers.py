from pathlib import Path

import numpy as np
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
st.title(Path(__file__).name)
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

    mean_x = plot_df[city_x].mean()
    mean_y = plot_df[city_y].mean()
    plot_df["deviation"] = np.sqrt(
        (plot_df[city_x] - mean_x).pow(2) + (plot_df[city_y] - mean_y).pow(2)
    ).round(decimals=1)

    # Set outlier tolerance via slider.
    outlier_tolerance = st.sidebar.slider(
        "Outlier tolerance",
        min_value=0.0,
        max_value=plot_df["deviation"].max(),
        step=0.1,
        value=1.0,
        format="%3.1f",
    )
    # Outlier calculation based on temperature difference a point and the mean temperature.
    plot_df["outlier"] = plot_df["deviation"] > outlier_tolerance
    # Make columns for plotting.
    plot_df["text"] = ["outlier" if o else "inlier" for o in plot_df["outlier"]]
    plot_df["color"] = ["red" if o else "lime" for o in plot_df["outlier"]]


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
    fig.update_layout(
        title={"text": f"{city_x} vs. {city_y} coloured by {city_color}"},
        height=800,
        width=800,
    )

# If outlier detection, plot inliers and outliers as separate traces with different colours.
elif color_option == "Outlier detection":
    text_list = [
        f"{idx}<br>"
        + f"{city_x}: {row[city_x]} deg C<br>"
        + f"{city_y}: {row[city_y]} deg C<br>"
        + f"{row['text']}<br>"
        + f"Outlier degree: {round(row['deviation'], 1)}<br>"
        for idx, row in plot_df.iterrows()
    ]

    fig.add_trace(
        go.Scattergl(
            x=plot_df[city_x],
            y=plot_df[city_y],
            hoverinfo="text",
            hovertext=text_list,
            mode="markers",
            marker={"color": plot_df["color"]},
        )
    )

    fig.update_layout(
        title={
            "text": (
                f"{city_x} vs. {city_y} with {sum(plot_df['outlier'])} outliers "
                f"out of {len(plot_df)} data points @{outlier_tolerance} deg C tolerance"
            )
        },
        height=800,
        width=800,
    )

fig.update_xaxes(title={"text": f"{city_x} temperature [deg C]"})
fig.update_yaxes(title={"text": f"{city_y} temperature [deg C]"})
st.plotly_chart(fig)
