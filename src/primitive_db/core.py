VALID_TYPES = {'int', 'str', 'bool'}

def create_table(metadata, table_name, columns):
    """Функция для создания таблиц"""
    # Проверяем существование таблицы
    if metadata.get(table_name) is not None:
        return f'Ошибка: Таблица "{table_name}" уже существует.'

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
        return "Дублируются имена столбцов."
    if not set(types).issubset(VALID_TYPES):
        return "Добавлены недопустимые типы столбцов."

    # Заполняем данными
    structure = {name:type_ for name, type_ in zip(names, types)}
    metadata[table_name] = structure    
    print(f'Таблица {table_name} успешно создана со столбцами: {", ".join(columns)}.')
    return metadata

def drop_table(metadata, table_name):
    """Функция для удаления таблиц"""
    # Проверяем существование таблицы
    if metadata.get(table_name) is None:
        return f'Ошибка: Таблица "{table_name}" не существует.'
    
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata