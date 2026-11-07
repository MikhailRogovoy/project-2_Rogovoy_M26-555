import time


def handle_db_errors(func):
    """Декоратор для обработки исключений"""
    def wrapper(*args, **kwargs):        
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.") # noqa: E501
        except KeyError as e:
            print(f"Ошибка: {e.args[0]}")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except TypeError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    wrapper.__name__ = f'{func.__name__}'
    return wrapper

def confirm_action(action_name:str):
    """Декоратор для подтверждения действий пользователя"""
    def decorator_confirm_action(func):    
        def wrapper(*args, **kwargs):             
            user_input = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ') # noqa: E501
            if user_input.lower() == 'y':
                return func(*args, **kwargs)
            else:
                print(f'Операция {action_name} отменена.')
        wrapper.__name__ = f'{func.__name__}'
        return wrapper        
    return decorator_confirm_action

def log_time(func):
    """Декоратор для измерения времени выполнения функции"""
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()        
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        interval = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {interval:.3f} секунд.")
        return result
    wrapper.__name__ = f'{func.__name__}'
    return wrapper


def create_cacher():
    "Функция с замыканием для создания кэша и удаления из данных из кэша"
    cache = {}
    @handle_db_errors
    def cache_result(key: str | dict[str, dict[str, (str | int | bool)]],
                     value_func, table_data:dict) -> dict:
        nonlocal cache

        if isinstance(key, str):
            table_name = key
            if cache.get(table_name, None) is None:
                select_result = value_func(table_data)
                all_table_cache = {}
                all_table_cache['all'] = select_result
                cache[table_name] = all_table_cache
            elif cache[table_name].get('all', None) is None:
                select_result = value_func(table_data)
                cache[table_name]['all'] = select_result
            else:
                print('Данные переданы из кэша.')
            return cache[table_name]['all']
        elif isinstance(key, dict):
            table_name = list(key.keys())[0]
            where_condition = list(key.values())[0]
            column_name = list(key[table_name].keys())[0]
            value = list(key[table_name].values())[0]

            if cache.get(table_name, None) is None:             
                select_result = value_func(table_data, where_condition)
                value_cache, column_cache = {}, {}
                value_cache[value] = select_result
                column_cache[column_name] = value_cache
                cache[table_name] = column_cache
            elif cache[table_name].get(column_name, None) is None:
                select_result = value_func(table_data, where_condition)
                value_cache = {}
                value_cache[value] = select_result
                cache[table_name][column_name] = value_cache
            elif cache[table_name][column_name].get(value, None) is None:
                select_result = value_func(table_data, where_condition)
                cache[table_name][column_name][value] = select_result
            else:
                print('Данные переданы из кэша.')
            return cache[table_name][column_name][value]

    @handle_db_errors
    def clear_cache(key: str):
        nonlocal cache
        table_name = key
        if cache.get(table_name, None) is not None:            
            del cache[table_name]            

    return cache_result, clear_cache