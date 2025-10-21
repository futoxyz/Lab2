from src.constants import INVANS


def confirm(data):
    '''
    Функция, требующая от пользователя ответ Y/N.
    :param data: Начальный объект data. Используется для логгирования в исходной директории.
    :return: True, если получено подтверждение, иначе False.
    '''
    enter = str(input("Do you want to continue? (Y/N) > "))
    data.log(enter, False)
    while enter not in ["Y", "y", "N", "n"]:
        data.log(INVANS)
        enter = str(input("Do you want to continue? (Y/N) > "))
        data.log(enter, False)
    if enter in ["Y", "y"]:
        return True
    else:
        return False
