from pathlib import Path

import tomllib


def load_toml(file_name: Path) -> dict:
    data = {}
    with open(file_name, "rb") as file_obj:
        data = tomllib.load(file_obj)
    return data
