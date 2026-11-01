import json


def load_metadata(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data
    
    except (FileNotFoundError, IOError):
        return {}

def save_metadata(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, ensure_ascii=False)