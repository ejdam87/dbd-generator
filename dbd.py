import random
from typing import List


def load_data(path: str) -> List[str]:

    with open(path, "r") as f:
        
        res = f.read().split("\n")

        if res[-1] == "":
            res.pop()

        return res


def get_character(character_list: List[str]) -> str:
    
    if character_list == []:
        return ""

    return random.choice(character_list)


def get_build(perk_list: List[str]) -> List[str]:
    
    random.shuffle(perk_list)
    return [perk_list[i] for i in range(4)]


def generate_character(clist_path: str) -> str:
    
    return get_character(load_data(clist_path))


def generate_build(plist_path: str) -> List[str]:

    return get_build(load_data(plist_path))
