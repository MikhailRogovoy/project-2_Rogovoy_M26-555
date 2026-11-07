import shlex

import prompt
from prettytable import PrettyTable

from . import core, decorators, parser, utils

META_FILE = "db_meta.json"

def print_help():
    """Функция выводит справочное сообщение."""
   
    print("\n***Процесс работы с таблицами***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")

    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")  # noqa: E501
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")  # noqa: E501
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.") # noqa: E501
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")  # noqa: E501
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print("***База данных***")
    print_help()

    select_cache, clear_cache = decorators.create_cacher()

    while True:
        metadata = utils.load_metadata(META_FILE)
        user_input = prompt.string('Введите команду: ')
        user_input = user_input.replace('\'', '"')

        try:
            args = shlex.split(user_input, posix=False)
        except ValueError:
            print('Ошибка: Проверьте запись команды. Возможно пропущены кавычки.')
            continue

        match args[0]:
            case 'create_table':                
                if len(args) < 2:
                    print(f'Ошибка: Неверно передана команда {args[0]}')
                    continue
                if args[1].find(":") != -1:
                    print(f'Некорректное значение: "{args[1]}" Попробуйте снова.')
                    continue
                elif len(args[2:]) == 0:
                    print('Не заданы столбцы таблицы.')
                    continue
                is_correct_data = True
                for arg in args[2:]:
                    if arg.find(":") == -1:
                        print(f'Некорректное значение: "{arg}". Попробуйте снова.')
                        is_correct_data = False
                        break
                
                if not is_correct_data:
                    continue
                result = core.create_table(metadata, args[1], args[2:])
                if isinstance(result, dict):
                    utils.save_metadata(META_FILE, result)
                    print(f'Таблица "{args[1]}" успешно создана со столбцами: {", ".join(args[2:])}.') # noqa: E501
                    utils.create_file(table_name=args[1])

            case 'list_tables':
                if len(metadata.keys()) != 0:
                    for key in metadata.keys():
                        print("- ", key)
                else:
                    print('Таблиц не создано.')

            case 'drop_table':
                if len(args) != 2:
                    print(f'Ошибка: Неверно передана команда {args[0]}')
                    continue

                result = core.drop_table(metadata, args[1])
                if isinstance(result, dict):
                    utils.save_metadata(META_FILE, result)
                    utils.delete_file(table_name=args[1])
                    print(f'Таблица "{args[1]}" успешно удалена.')
                    clear_cache(args[1])

            case 'insert':
                if (len(args) < 5
                    or args[1].strip() != 'into'
                    or args[3].strip() != 'values'):
                    print(f'Ошибка: Неверно передана команда {args[0]}')
                    continue

                values = parser.insert_values_splitter(user_input)
                if values != []:                            
                    table_data = utils.load_table_data(args[2])
                    insert_result = core.insert(metadata, args[2],
                                                table_data,
                                                values)
                    if isinstance(insert_result, dict):
                        utils.save_table_data(args[2], insert_result)
                        key_id = list(insert_result.keys())[-1]
                        print(f'Запись с ID={key_id} успешно добавлена в таблицу "{args[2]}".') # noqa: E501
                        clear_cache(args[2])
                else:
                    print('Ошибка. Неверно переданы значения в insert после values')

            case 'select':
                if (len(args) < 3 
                    or args[1].strip() != 'from'):
                    print(f'Ошибка: Неверно передана команда {args[0]}')
                    continue                
                if metadata.get(args[2], None) is None:
                    print(f'Ошибка: Таблица {args[2]} не существует.')
                    continue

                if len(args) == 3:
                    table_data = utils.load_table_data(args[2])
                    select_result = select_cache(args[2], core.select, table_data)
                    if isinstance(select_result, dict):
                        columns = list(metadata[args[2]].keys())
                        table = PrettyTable()
                        table.field_names = columns
                        for item in select_result.items():
                            table.add_row([item[0]] + list(item[1].values()))
                        print(table)
                    else:
                        print('Данных для прочтения не обнаружено.')

                elif len(args) > 3 and args[3].strip() == 'where':
                    where_str = user_input.strip().split(' ', 4)[4]
                    where_clause = parser.parser_conditions(where_str, 'where')
                    if not isinstance(where_clause, dict):
                        continue
                    if list(where_clause.keys())[0] not in metadata[args[2]].keys():
                        print(f'Ошибка: Столбец {args[4]} в таблице "{args[2]}" не найден.') # noqa: E501
                        continue

                    key_cache = {}
                    key_cache[args[2]] = where_clause

                    table_data = utils.load_table_data(args[2])
                    select_result = select_cache(key_cache, core.select, table_data)
                    if isinstance(select_result, dict):
                        columns = list(metadata[args[2]].keys())
                        table = PrettyTable()
                        table.field_names = columns
                        for item in select_result.items():
                            table.add_row([item[0]] + list(item[1].values()))
                        print(table)
                    else:
                        print('Данных для прочтения по условию не обнаружено.')

                else:
                    print(f'Ошибка: Неверно передана команда {args[0]}')
            
            case 'update':
                if (len(args) != 10
                    or args[2].strip() != 'set'
                    or args[4].strip() != '='
                    or args[6].strip() != 'where'
                    or args[8].strip() != '='):
                    print(f'Ошибка: Неверно передана команда {args[0]}')
                    continue
                if metadata.get(args[1], None) is None:
                    print(f'Ошибка: Таблица {args[1]} не существует.')
                    continue
                
                set_clause_str = ' '.join(map(str.strip, [args[3], args[4], args[5]]))
                where_clause_str = ' '.join(map(str.strip, [args[7], args[8], args[9]]))
                set_clause = parser.parser_conditions(set_clause_str, 'set')
                where_clause = parser.parser_conditions(where_clause_str, 'where')
                
                if (not isinstance(set_clause, dict)
                    or not isinstance(where_clause, dict)):
                    continue
                if list(set_clause.keys())[0] not in metadata[args[1]].keys():
                    print(f'Ошибка: Столбец {args[3]} в set не найден в таблице "{args[1]}".') # noqa: E501
                    continue
                if list(where_clause.keys())[0] not in metadata[args[1]].keys():
                    print(f'Ошибка: Столбец {args[7]} в where не найден в таблице "{args[1]}".') # noqa: E501
                    continue

                table_data = utils.load_table_data(args[1])
                result_update = core.update(table_data, set_clause, where_clause)

                if isinstance(result_update, tuple):
                    utils.save_table_data(args[1], result_update[0])
                    for key in result_update[1]:
                        print(f'Запись с ID={key} в таблице "{args[1]}" успешно обновлена.') # noqa: E501
                    clear_cache(args[1])


            case 'delete':
                if (len(args) != 7
                    or args[1].strip() != 'from'
                    or args[3].strip() != 'where'
                    or args[5].strip() != '='):
                    print(f'Ошибка: Неверно передана команда {args[0]}')
                    continue
                if metadata.get(args[2], None) is None:
                    print(f'Ошибка: Таблица {args[2]} не существует.')
                    continue

                table_data = utils.load_table_data(args[2])
                where_clause_str = ' '.join(map(str.strip, [args[4], args[5], args[6]]))
                where_clause = parser.parser_conditions(where_clause_str, 'where')
                if not isinstance(where_clause, dict):
                    continue
                if list(where_clause.keys())[0] not in metadata[args[2]].keys():
                    print(f'Ошибка: Столбец {args[4]} в таблице "{args[2]}" не найден.')
                    continue

                result_delete = core.delete(table_data, where_clause)

                if isinstance(result_delete, tuple):
                    utils.save_table_data(args[2], result_delete[0])
                    for key in result_delete[1]:
                        print(f'Запись с ID={key} успешно удалена из таблицы "{args[2]}".') # noqa: E501
                    clear_cache(args[2])

            case 'info':
                if len(args) != 2:
                    print(f'Ошибка: Неверно передана команда {args[0]}')
                    continue
                if metadata.get(args[1], None) is None:
                    print(f'Ошибка: Таблица {args[1]} не существует.')
                    continue
                table_data = utils.load_table_data(args[1])
                columns = [f'{item[0]}:{item[1]}' for item in metadata[args[1]].items()]
                print(f'Таблица: {args[1]}')
                print(f'Столбцы: {', '.join(columns)}')
                print(f'Количество записей: {len(table_data)}')

            case 'help':
                if len(args) != 1:
                    print(f'Ошибка: Неверно передана команда {args[0]}')
                    continue              
                print_help()

            case 'exit':
                break

            case _:
                print(f'Функции {args[0]} нет. Попробуйте снова.')