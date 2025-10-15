import os


def getname(dir, folder=False):
    '''
    Позволяет получить название файла/папки из названия директории (необязательно целого).
    :param dir: Директория, может вести либо к файлу, либо к каталогу.
    :param folder: Вводится True если требуется именно каталог файла при исходной директории файла.
    :return: Название файла/папки.
    '''
    if "/" in dir:
        dir = dir.replace("/", "\\")
    if os.path.isdir(dir) and folder or not folder:
        return dir.split("\\")[-1]
    elif len(dir) >= 2:
        return dir.split("\\")[-2]
    else:
        return "."
