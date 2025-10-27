import os
from src.data import Data
from src.execute import execute


def run():
    '''
    Функция запуска. Создает папку .trash для хранения удаленных файлов. Передает исходный путь объекту data, затем проводит цикл ввода.
    :return: Ничего не возвращает.
    '''
    init_dir = os.getcwd()
    if not os.path.isdir(os.path.join(init_dir, ".trash")):
        os.mkdir(os.path.join(init_dir, ".trash"))
    data = Data(init_dir)
    while inp := input(f"{os.getcwd()} > "):
        execute(inp, data)


if __name__ == "__main__":
    run()
