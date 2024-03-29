import plotly.express as px

# Function to get any given colour.
def get_color(cat1: str, cat2: str) -> str:
    # Dict for all standard colours to be used in this module.
    cdict = {
        "seasons": {"summer": "red", "winter": "blue"},
        "temperature": {
            "value": "black",
            "mean": "#999999",
            "min": "blue",
            "max": "red",
        },
        "labeling": {
            "Add": "#00ff00",
            "Remove": "red",
            "default": "black",
            "labeled": "magenta",
        },
    }
    return cdict[cat1][cat2]


# Map a list of items to the Alphabet colour sequence to get a consistent sequence of colours.
def map_color_sequence(input_list: list) -> dict:
    cmap = {}
    sorted_list = sorted(input_list)

    for idx, item in enumerate(sorted_list):
        cmap[item] = px.colors.qualitative.Alphabet[idx]

    return cmap
