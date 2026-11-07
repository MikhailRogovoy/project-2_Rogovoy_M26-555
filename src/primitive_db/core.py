from . import constants, decorators

VALID_TYPES = constants.VALID_TYPES

@decorators.handle_db_errors
def create_table(metadata:dict, table_name:str, columns:list[str]) -> dict[str, dict]:
    """Функция для создания таблиц"""
    # Проверяем существование таблицы
    if metadata.get(table_name) is not None:
        raise KeyError(f'Таблица "{table_name}" уже существует.')

    # Добавляем ID:int как первый столбец
    if "ID:int" not in columns:
        columns.insert(0, "ID:int")
    else:
        columns.remove("ID:int")
        columns.insert(0, "ID:int")
    
    # Проверяем соответствие столбцов типам и дублирование имен
    names = [col.split(":")[0] for col in columns]
    types = [col.split(":")[1] for col in columns]
    if len(set(names)) != len(columns):
        raise KeyError('Дублируются имена столбцов.')
    if not set(types).issubset(VALID_TYPES):
        raise TypeError('Добавлены недопустимые типы столбцов.')

    # Заполняем данными
    structure = {name:type_ for name, type_ in zip(names, types)}
    metadata[table_name] = structure
    return metadata

@decorators.handle_db_errors
@decorators.confirm_action('удаление таблицы')
def drop_table(metadata:dict, table_name:str) -> dict[str, dict]:
    """Функция для удаления таблиц"""
    # Проверяем существование таблицы
    if metadata.get(table_name) is None:
        raise KeyError(f'Таблица "{table_name}" не существует.')
    
    del metadata[table_name]
    return metadata

@decorators.log_time
@decorators.handle_db_errors
def insert(metadata:dict, 
           table_name:str, 
           table_data:dict, 
           values: list[str | int | bool]) -> dict[str, dict]:
    """Функция для добавления данных в таблицу"""
    # Проверяем существование таблицы    
    if metadata.get(table_name) is None:
        raise KeyError(f'Таблица "{table_name}" не существует.')
    if len(values) != len(metadata[table_name])- 1:
        raise ValueError('В таблицу передано неверное количество значений.')
    
    columns = list(metadata[table_name].keys())[1:]
    types = list(metadata[table_name].values())[1:]
    data = table_data
    new_id = len(data) + 1
    insert_data = {}
    
    for i in range(0, len(values)):
        if ((values[i][0] in ['+', '-']
            and values[i][1:].isdigit()
            and types[i] == 'int')
            or (values[i].isdigit() 
            and types[i] == 'int')):
                insert_data[columns[i]] = int(values[i])
        elif values[i].lower() in ['true', 'false'] and types[i] == 'bool':
            if values[i].lower() == 'true':
                insert_data[columns[i]] = True
            else:
                insert_data[columns[i]] = False
        elif (values[i][0] == '"'
              and values[i][-1] == '"'
              and types[i] == 'str'):
                insert_data[columns[i]] = values[i].strip().strip('"')
        else:
            raise TypeError(f'{values[i]} не соответствует типу столбца {columns[i]}')

    data[new_id] = insert_data
    
    return data

@decorators.log_time
def select(table_data:dict, where_clause: dict | None=None) -> (dict | None):
    """Функция для выборки данных из таблицы"""
    if where_clause is None:
        if table_data == {}:
           return None 
        return table_data
    else:        
        condition = list(where_clause.items())
        select_data = {}        
        for item in list(table_data.items()):
            if condition[0][0] == 'ID':
                if int(item[0]) == condition[0][1]:
                    select_data[item[0]] = item[1]
                continue

            if ((isinstance(condition[0][1], (int, bool)) 
                    and item[1][condition[0][0]] == condition[0][1])
                or (isinstance(condition[0][1], str)
                    and item[1][condition[0][0]] == condition[0][1].strip('"'))):
                select_data[item[0]] = item[1]

        if select_data == {}:
            return None
        return select_data

def update(table_data:dict, 
           set_clause:dict[str, str | int | bool], 
           where_clause:dict[str, str | int | bool]) -> (tuple[dict, list] 
                                                         | None):
    """Функция для обновления данных в таблице по условию"""
    update_data = select(table_data=table_data, where_clause=where_clause)
    if isinstance(update_data, dict):
        for item in list(update_data.items()):
            if update_data[item[0]].get(list(set_clause.keys())[0], None) is not None:
                update_data[item[0]].update(set_clause)
        
        keys = []
        for item in list(update_data.items()):
            table_data[item[0]] = item[1]
            keys.append(item[0])      
        return (table_data, keys)

    print('Изменений по заданному условию нет.')
    return None

@decorators.confirm_action('удаление данных из таблицы')
def delete(table_data:dict, where_clause:dict) -> (tuple[dict, list] 
                                                   | None):
    """Функция для удаления данных из таблицы по условию"""
    delete_data = select(table_data=table_data, where_clause=where_clause)
    if isinstance(delete_data, dict):
        keys = []
        for key in list(delete_data.keys()):
            table_data.pop(key)
            keys.append(key)

        updated_table_data = {}
        items = list(table_data.items())
        for i in range(1, len(table_data) + 1):
            updated_table_data[i] = items[i-1][1]
        return (updated_table_data, keys)

    print('Нет данных для удаления по заданному условию.')
    return None



        