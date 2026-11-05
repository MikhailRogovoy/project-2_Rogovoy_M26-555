import shlex

import prompt
from prettytable import PrettyTable

from . import core, parser, utils

META_FILE = "db_meta.json"

def print_help():
    """Функция выводит справочное сообщение."""
   
    print("\n***Процесс работы с таблицами***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")  # noqa: E501
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")  # noqa: E501
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.") # noqa: E501
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")  # noqa: E501
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    print("***База данных***")
    print_help()

    while True:
        metadata = utils.load_metadata(META_FILE)
        user_input = prompt.string('Введите команду: ')
        args = shlex.split(user_input, posix=False)        
        match args[0]:
            case 'create_table':
                is_correct_data = True
                if len(args) < 2:
                    print(f'Ошибка: Неверно записана команда {args[0]}')
                    continue
                if args[1].find(":") != -1:
                    print(f'Некорректное значение: "{args[1]}" Попробуйте снова.')
                    is_correct_data = False
                elif len(args[2:]) == 0:
                    print('Не заданы столбцы таблицы.')
                    is_correct_data = False
                for arg in args[2:]:
                    if arg.find(":") == -1:
                        print(f'Некорректное значение: "{arg}". Попробуйте снова.')
                        is_correct_data = False
                        break
                
                if is_correct_data:
                    result = core.create_table(metadata, args[1], args[2:])
                    if isinstance(result, str):
                        print(result)                    
                    else:
                        utils.save_metadata(META_FILE, result)
                        utils.create_file(table_name=args[1])

            case 'list_tables':
                if len(metadata.keys()) != 0:
                    for key in metadata.keys():
                        print("- ", key)
                else:
                    print('Таблиц не создано.')

            case 'drop_table':
                if len(args) != 2:
                    print(f'Ошибка: Неверно записана команда {args[0]}')
                    continue
                result = core.drop_table(metadata, args[1])
                if isinstance(result, str):
                    print(result)
                else:
                    utils.save_metadata(META_FILE, result)
                    utils.delete_file(table_name=args[1])

            case 'insert':
                if (len(args) < 5
                    or args[1].strip() != 'into'
                    or args[3].strip() != 'values'):
                    print(f'Ошибка: Неверно записана команда {args[0]}')
                    continue                
                if metadata.get(args[2], None) is None:
                    print(f'Таблица {args[2]} не существует.')
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
                    else:
                        print(insert_result)
                else:
                    print('Ошибка. Неверно переданы значения в insert после values')

            case 'select':
                if (len(args) < 3 
                    or args[1].strip() != 'from'):
                    print(f'Ошибка: Неверно записана команда {args[0]}')
                    continue                
                if metadata.get(args[2], None) is None:
                    print(f'Таблица {args[2]} не существует.')
                    continue
                if len(args) == 3:
                    table_data = utils.load_table_data(args[2])
                    select_result = core.select(table_data)  
                    if isinstance(select_result, dict):
                        columns = list(metadata[args[2]].keys())
                        table = PrettyTable()
                        table.field_names = columns
                        for item in select_result.items():
                            table.add_row([item[0]] + list(item[1].values()))
                        print(table)
                    else:
                        print(select_result)
                elif len(args) > 3 and args[3].strip() == 'where':
                    where_str = user_input.split(' ', 4)[4]
                    where_clause = parser.parser_conditions(where_str, 'where')
                    table_data = utils.load_table_data(args[2])
                    select_result = core.select(table_data, where_clause) 
                    if isinstance(select_result, dict):
                        columns = list(metadata[args[2]].keys())
                        table = PrettyTable()
                        table.field_names = columns
                        for item in select_result.items():
                            table.add_row([item[0]] + list(item[1].values()))
                        print(table)
                    else:
                        print(select_result)
                else:
                    print(f'Ошибка: Неверно записана команда {args[0]}')
            
            case 'update':
                if (len(args) != 10
                    or args[2].strip() != 'set'
                    or args[4].strip() != '='
                    or args[6].strip() != 'where'
                    or args[8].strip() != '='):
                    print(f'Ошибка: Неверно записана команда {args[0]}')
                    continue
                if metadata.get(args[1], None) is None:
                    print(f'Таблица {args[1]} не существует.')
                    continue
                
                map(str.strip, [args[3], args[4], args[5]])
                set_clause_str = ' '.join(map(str.strip, [args[3], args[4], args[5]]))
                where_clause_str = ' '.join(map(str.strip, [args[7], args[8], args[9]]))
                set_clause = parser.parser_conditions(set_clause_str, 'set')
                where_clause = parser.parser_conditions(where_clause_str, 'where')
                print(set_clause, where_clause)
                table_data = utils.load_table_data(args[1])
                result_update, keys = core.update(table_data, set_clause, where_clause)

                if isinstance(result_update, dict):
                    utils.save_table_data(args[1], result_update)
                    for key in keys:
                        print(f'Запись с ID={key} в таблице "{args[1]}" успешно обновлена.') # noqa: E501
                else:
                    print(result_update)

            case 'delete':
                if (len(args) != 7
                    or args[1].strip() != 'from'
                    or args[3].strip() != 'where'
                    or args[5].strip() != '='):
                    print(f'Ошибка: Неверно записана команда {args[0]}')
                    continue
                if metadata.get(args[2], None) is None:
                    print(f'Таблица {args[2]} не существует.')
                    continue

                table_data = utils.load_table_data(args[2])
                where_clause_str = ' '.join(map(str.strip, [args[4], args[5], args[6]]))
                where_clause = parser.parser_conditions(where_clause_str, 'where')
                result_delete, keys = core.delete(table_data, where_clause)

                if isinstance(result_delete, dict):
                    utils.save_table_data(args[2], result_delete)
                    for key in keys:
                        print(f'Запись с ID={key} успешно обновлена из таблицы "{args[2]}".') # noqa: E501
                else:
                    print(result_delete)

            case 'info':
                if len(args) != 2:
                    print(f'Ошибка: Неверно записана команда {args[0]}')
                    continue
                if metadata.get(args[1], None) is None:
                    print(f'Таблица {args[1]} не существует.')
                    continue
                table_data = utils.load_table_data(args[1])
                columns = [f'{item[0]}:{item[1]}' for item in metadata[args[1]].items()]
                print(f'Таблица: {args[1]}')
                print(f'Столбцы: {', '.join(columns)}')
                print(f'Количество записей: {len(table_data)}')

            case 'help':
                if len(args) != 1:
                    print(f'Ошибка: Неверно записана команда {args[0]}')
                    continue              
                print_help()

            case 'exit':
                break

            case _:
                print(f'Функции {args[0]} нет. Попробуйте снова.')