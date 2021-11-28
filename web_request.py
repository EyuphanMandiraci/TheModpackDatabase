from requests import get
from json import loads

def get_data(url, get_json=True):
    if get_json:
        print(get(url).text)
        r = loads(get(url).text)
    else:
        r = get(url).text
    return r