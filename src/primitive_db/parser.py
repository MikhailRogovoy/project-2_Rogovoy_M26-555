import shlex


def parser_conditions(string, keyword):
    if '=' in string:
        conditions = string.split('=')
        conditions = [item.strip() for item in conditions]

    else:
        return f"Ошибка: Неверно задано условие {keyword} <столбец> = <значение>"
    
    if len(conditions) == 2:
        if conditions[1][0] in "+-":
            if conditions[1][1:].isdigit():
                return {conditions[0]:int(conditions[1])}
        elif conditions[1].isdigit():
            return {conditions[0]:int(conditions[1])}
        elif conditions[1].lower() == 'true':
            return {conditions[0]:True}
        elif conditions[1].lower() == 'false':
            return {conditions[0]:False}        
        elif (conditions[1][0] in ['\"', '\'']
            and conditions[1][-1] in ['\"', '\'']):
                return {conditions[0]:f'"{conditions[1][1:-1]}"'}
        else:
            return f'Ошибка: Строковое значение {conditions[1]} должны быть в кавычках'
    
    return f"Ошибка: Неверно задано условие {keyword} <столбец> = <значение>"

def insert_values_splitter(user_input):
    string_values = user_input.split(' ', 4)[4].strip()

    if (string_values[0] == '(' 
        and string_values[-1] == ')'
        and '(' not in string_values[1:-1]
        and ')' not in string_values[1:-1]):
        string_values = string_values.strip('()').strip()
        values = shlex.shlex(string_values, posix=False)
        values.whitespace = ','
        values.whitespace_split = True
        values.quotes == '"\''

        values = [value.strip() for value in values]

        return values

    else:
        return []
