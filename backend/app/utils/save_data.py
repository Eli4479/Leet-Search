import os
import json


def save_problems(json_problems, file_name=None):
    if file_name is None:
        return None
    from pathlib import Path
    folder_path = str(Path(__file__).parents[3] / 'data')
    print(f"Saving problems to {folder_path}/{file_name}")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.extend(json_problems)
    seen_ids = set()
    unique_data = []
    for problem in existing_data:
        if problem['id'] not in seen_ids:
            seen_ids.add(problem['id'])
            unique_data.append(problem)
    existing_data = unique_data
    sorted_data = sorted(existing_data, key=lambda x: int(x['id']))
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_data, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved {len(json_problems)} problems to {file_path}")
