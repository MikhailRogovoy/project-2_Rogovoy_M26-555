# Примитивная база данных

Настоящий проект является примитивной базой данных с минимальными возможностями по созданию таблиц, их наполенению и манипуляций с данными.

## Структура 

project-2-database/

├── src/
│   └── primitive_db/
│       ├── __init__.py
│       ├── engine.py
│       ├── main.py
│       ├── core.py
|       ├── utils.py
|       ├── parser.py
|       └── decorators.py
|
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore 

## Установка 
1. Установите пакетный и проектный менеджер uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Клонируйте репозиторий и перейдите в папку проекта:
```bash
git clone https://github.com/MikhailRogovoy/project-2_Rogovoy_M26-555
```
```bash
cd project-2_Rogovoy_M26-555
```

3. Соберите проект (пакеты `.whl` и `.tar.gz` появятся в папке `dist/`):
```bash
uv build
```

4. Установите собранный пакет как инструмент:
```bash
uv tool install dist/*.whl
```

5. Запустите пакет напрямую из любого места в терминале по её имени:
```bash
database
```

## Возможности

### Функции для работы с таблицей

'<command>' create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу

'<command>' list_tables - показать список всех таблиц;

'<command>' drop_table <имя_таблицы> - удалить таблицу;

'<command>' info <имя_таблицы> - вывести информацию о таблице.

### Функции для работы с данными (CRUD-операции)

'<command>' insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.;

'<command>' select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию;

'<command>' select from <имя_таблицы> - прочитать все записи;

'<command>' update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись;

'<command>' delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.

### Общие функции

'<command>' exit - выход из программы;

'<command>' help - справочная информация

## Пример работы

[![asciicast](https://asciinema.org/a/uVjW9BwHBmpehfSE.svg)](https://asciinema.org/a/uVjW9BwHBmpehfSE)