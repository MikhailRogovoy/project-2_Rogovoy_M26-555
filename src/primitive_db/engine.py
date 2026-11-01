import prompt


def welcome():
    print("""
Первая попытка запустить проект!

***
<command> exit - выйти из программы
<command> help - справочная информация
Введите команду: help

<command> exit - выйти из программы
<command> help - справочная информация
""")

    prompt.string('Введите команду: ')