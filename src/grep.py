import re


def grep(pattern, file_dir, i):
    '''
    Ищет шаблон в файле. Учёт регистра определяет i.
    :param pattern: Шаблон.
    :param file_dir: Директория файла.
    :param i: Если поиск без учёта регистра - True, иначе False.
    :return: Все найденные строки с выделенным шаблоном. Если файл не удалось прочитать - передает ошибку.
    '''
    match i:
        case True:
            flag = re.IGNORECASE
        case False:
            flag = re.NOFLAG
    try:
        with open(file_dir) as f:
            lncount = 1
            lns = []
            for line in f:
                if re.search(pattern, line, flag):
                    line = re.sub(pattern, f'"{pattern}"', line, flags=re.IGNORECASE)
                    lns.append(f"File {file_dir}: line {lncount} - {line}")
                lncount += 1
            return "".join(lns)
    except:
        return f"Could not search in {file_dir}\n"
