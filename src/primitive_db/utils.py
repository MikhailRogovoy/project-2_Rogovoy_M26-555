import json
import os


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

def load_table_data(table_name):    
    try:
        with open(f"./data/{table_name}.json", 'r') as file:
            data = json.load(file)
        return data
    
    except (FileNotFoundError, IOError):
        return {}    

def save_table_data(table_name, data):
    with open(f"./data/{table_name}.json", 'w') as file:
        json.dump(data, file, ensure_ascii=False)

def create_file(table_name):

    os.makedirs('./data/', exist_ok=True)
    with open(f"./data/{table_name}.json", 'w') as file:
        file.write('{}')

def delete_file(table_name):
    try:
        os.remove(f'./data/{table_name}.json')

    except (FileNotFoundError, IOError):
        print(f'Ошибка: Файл с таблицей {table_name} отсутствует') 