from datetime import datetime
import re
from typing import List


def log(content):
    print("{} {}".format(now(), content))


def now() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def isValidHexaCode(str: str) -> bool:
    if str == None:
        return False

    regex = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    p = re.compile(regex)
    return re.search(p, str)


def split(list: List[any], amount: int):
    if amount >= (len(list)):
        return [list]
