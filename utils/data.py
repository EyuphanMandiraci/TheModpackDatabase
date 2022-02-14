import os.path
from json import dump, loads

data = {}


def create_data():
    global data
    if not os.path.exists("data.txt"):
        data = {"downloaded": []}
        with open("data.txt", "w", encoding="utf-8") as data_file:
            dump(data, data_file, indent=4, ensure_ascii=False, sort_keys=True)
    else:
        with open("data.txt", "r", encoding="utf-8") as data_file:
            data = loads(data_file.read())


def write_to_data(modpack):
    with open("data.txt", "w", encoding="utf-8") as data_file:
        data["downloaded"].append(modpack)
        dump(data, data_file, indent=4, ensure_ascii=False, sort_keys=True)


def get_data():
    global data
    with open("data.txt", "r", encoding="utf-8") as data_file:
        data = loads(data_file.read())
    return data
