from json import dump, loads
from os import path


def check_path(file_path):
    return path.exists(file_path)


def set_data(file_path, data_dict):
    dosya = open(file_path, "w", encoding="utf-8")
    dump(data_dict, dosya, ensure_ascii=False, indent=4, sort_keys=True)
    dosya.close()


def get_data(file_path):
    dosya = open(file_path, "r", encoding="utf-8")
    data_dict = loads(dosya.read())
    dosya.close()
    return data_dict
