import plotly.express as px

cdict = {
    'temperature': {
        'value': 'black',
        'mean': '#999999',
        'min': 'blue',
        'max': 'red'
    },
    'labeling': {
        'Add': '#00ff00',
        'Remove': 'red',
        'default': 'black',
        'tagged': 'magenta'
    }
}

def get_color(cat1: str, cat2: str) -> str:
    return cdict[cat1][cat2]

def map_color_sequence(input_list: list) -> dict:
    cmap = {}
    sorted_list = sorted(input_list)

    for idx, item in enumerate(sorted_list):
        cmap[item] = px.colors.qualitative.Alphabet[idx]

    return cmap