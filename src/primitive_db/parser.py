import shlex

from . import decorators


@decorators.handle_db_errors
def parser_conditions(string: str, keyword: str) -> (dict[str, int] 
                                                     | dict[str, bool] 
                                                     | dict[str, str]):
    """Парсер для обработки условий в set и where"""
    if '=' not in string:
        raise ValueError(f'Ошибка: Неверное условие {keyword} <столбец> = <значение>')
    
    conditions = string.split('=')
    conditions = [item.strip() for item in conditions]     
    
    if len(conditions) == 2:
        if ((conditions[1][0] in ['+', '-']
            and conditions[1][1:].isdigit())
            or (conditions[1].isdigit())):
                return {conditions[0]:int(conditions[1])}
        elif conditions[1].lower() == 'true':
            return {conditions[0]:True}
        elif conditions[1].lower() == 'false':
            return {conditions[0]:False}        
        elif (conditions[1][0] == '"'
            and conditions[1][-1] == '"'):
                if keyword == 'set':
                    return {conditions[0]:f'{conditions[1][1:-1]}'}
                return {conditions[0]:conditions[1]}
        else:
            raise ValueError(f'Ошибка: Строка {conditions[1]} должна быть в кавычках')
    
    raise ValueError(f'Ошибка: Неверное условие {keyword} <столбец> = <значение>')

def insert_values_splitter(user_input:str) -> (list[str] | list):
    """Парсер для обработки значений после where в команде insert"""
    string_values = user_input.split(' ', 4)[4].strip()

    if (string_values[0] == '(' 
        and string_values[-1] == ')'
        and '(' not in string_values[1:-1]
        and ')' not in string_values[1:-1]):
        string_values = string_values.strip('()').strip()
        values = shlex.shlex(string_values, posix=False)
        values.whitespace = ','
        values.whitespace_split = True
        values.quotes == '"'

        values = [value.strip() for value in values]

        return values

    else:
        return []
