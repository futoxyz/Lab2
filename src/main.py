from os import getcwd
from src.data import Data
from src.execute import execute


def run():
    '''
    Функция запуска. Передает исходный путь объекту data, затем проводит цикл ввода.
    :return: Ничего не возвращает.
    '''
    data = Data(getcwd())
    while inp := input(f"{getcwd()} > "):
        execute(inp, data)


if __name__ == "__main__":
    run()
