import json
from pathlib import Path

__all__ = ['load_data']


def load_data(file_name=None):
    if file_name is None:
        return None
    try:
        folder_path = Path(__file__).resolve().parents[3] / 'data'
    except IndexError:
        raise RuntimeError(
            "Not enough parent directories in the path to reach "
            "'data' folder."
        )
    file_path = folder_path / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded data from {file_path}")
    return data
