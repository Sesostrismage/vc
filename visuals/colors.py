cdict = {
    'temperature': {
        'value': 'black',
        'reference': 'grey',
        'min': 'blue',
        'max': 'red'
    }
}

def get_color(cat1: str, cat2: str) -> str:
    return cdict[cat1][cat2]