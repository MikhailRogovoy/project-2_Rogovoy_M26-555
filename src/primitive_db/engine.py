import shlex

import prompt

from . import core, utils

META_FILE = "db_meta.json"

def print_help():
    """Функция выводит справочное сообщение."""
   
    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n") 

def run():
    print("""
***База данных***

***Процесс работы с таблицей***
Функции:
<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> exit - выход из программы
<command> help - справочная информация 
""")

    while True:
        metadata = utils.load_metadata(META_FILE)
        user_input = prompt.string('Введите команду: ')
        args = shlex.split(user_input)
        match args[0]:
            case 'create_table':
                is_correct_data = True
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
            case 'list_tables':
                if len(metadata.keys()) != 0:
                    for key in metadata.keys():
                        print("- ", key)
                else:
                    print('Таблиц не создано.')
            case 'drop_table':
                result = core.drop_table(metadata, args[1])
                if isinstance(result, str):
                    print(result)
                else:
                    utils.save_metadata(META_FILE, result)
            case 'exit':
                break
            case 'help':
                print_help()
            case _:
                print(f'Функции {args[0]} нет. Попробуйте снова.')