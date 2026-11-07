import json
import os

from . import decorators


@decorators.handle_db_errors
def load_metadata(filepath:str) -> (dict[str, dict[str, str]] | dict):
    """Функция передает метаданные из указанного файла"""
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        return data   
    except FileNotFoundError:
        return {}
def save_metadata(filepath:str, data:dict[str, dict[str, str]]) -> None:
    """Функция передает метаданные в указанный файл"""
    with open(filepath, 'w') as file:
        json.dump(data, file, ensure_ascii=False)

def load_table_data(table_name:str) -> (dict[str, dict] | dict):
    """Функция передает данные таблицы из указанного файла"""
    try:
        with open(f"./data/{table_name}.json", 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return {}

def save_table_data(table_name:str, data) -> None:
    """Функция передает данные таблицы в указанный файл"""
    with open(f"./data/{table_name}.json", 'w') as file:
        json.dump(data, file, ensure_ascii=False)

def create_file(table_name:str) -> None:
    """Функция создает json-файл таблицы в указанной директории"""
    os.makedirs('./data/', exist_ok=True)
    with open(f"./data/{table_name}.json", 'w') as file:
        file.write('{}')

@decorators.handle_db_errors
def delete_file(table_name:str) -> None:
    """Функция удаляет json-файл таблицы в указанной директории"""
    os.remove(f'./data/{table_name}.json')