import json
from glob import glob
from pathlib import Path
from os import path

parent_path = Path(__file__).parent

strings = {}

glob_search = str(parent_path.joinpath("Language", "*.json"))
langs = [path.basename(x)[:-5] for x in glob(glob_search)]

for lang in langs:
    path = parent_path.joinpath("Language", f"{lang}.json")
    with open(path, "r", encoding="utf-8") as file:
        strings[lang] = json.load(file)


def get_text(key, lang="en"):
    return strings[lang][key]


def get_all_text(key):
    ls = [strings[s][key] for s in langs]
    if len(ls) > 0 and isinstance(ls[0], list):
        return [i for l in ls for i in l]
    return ls
