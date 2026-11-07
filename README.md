# Примитивная база данных

Настоящий проект является примитивной базой данных с минимальными возможностями по созданию таблиц, их наполнению и манипуляций с данными.

## Структура 

project-2-database/

├── src/<br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   └── primitive_db/<br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       ├── __init__.py<br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       ├── engine.py<br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       ├── main.py<br />
│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       ├── core.py<br />
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       ├── utils.py<br />
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       ├── parser.py<br />
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       └── decorators.py<br />
|<br />
├── pyproject.toml<br />
├── uv.lock<br />
├── README.md<br />
└── .gitignore<br />

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

- create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу

- list_tables - показать список всех таблиц;

- drop_table <имя_таблицы> - удалить таблицу;

- info <имя_таблицы> - вывести информацию о таблице.

### Функции для работы с данными (CRUD-операции)

- insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.;

- select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию;

- select from <имя_таблицы> - прочитать все записи;

- update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись;

- delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.

### Общие функции

- exit - выход из программы;

- help - справочная информация

## Пример работы

[![Перейти для просмотра](https://asciinema.org/a/uVjW9BwHBmpehfSE.svg)](https://asciinema.org/a/uVjW9BwHBmpehfSE)
