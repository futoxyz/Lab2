import shutil
from src.getname import getname
from src.constants import INVANS, RMREST, CANCEL


def confirm(rm_dir, data):
    '''
    Команда для rm с рекурсивным удалением, требующим подтверждение. Ждёт от пользователя окончательный ответ Y/N.
    :param new_dir: Удаляемая директория.
    :param data: Начальный объект data, хранящий исходную директорию.
    :return: True, если удалось удалить, иначе None.
    '''
    if rm_dir == ".." or rm_dir == "/":
        data.log(RMREST)
        return
    enter = str(input("Do you want to continue? (Y/N) > "))
    data.log(enter, False)
    while enter not in ["Y", "y", "N", "n"]:
        data.log(INVANS)
        enter = str(input("Do you want to continue? (Y/N) > "))
        data.log(enter, False)
    if enter in ["Y", "y"]:
        try:
            shutil.copytree(rm_dir, f"{data.init_dir}\\.trash\\{getname(rm_dir, True)}")
            shutil.rmtree(rm_dir)
            return True
        except:
            return
    else:
        data.log(CANCEL)
        return

