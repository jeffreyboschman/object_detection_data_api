import os
import pathlib


def ensure_directory_exists(dir_path):
    if not os.path.exists(dir_path):
        pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)