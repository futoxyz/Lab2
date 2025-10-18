import pytest
from os import getcwd
from src.data import Data
from src.execute import execute
from command_list import *

def exec_test():
    init_dir = getcwd()
    data = Data(f"{init_dir}\\tests\\test_env")
    '''
    Проверка команд над файлами и каталогами в test_env/
    :return: Ничего не возвращает
    '''
    data.log("TEST START")
    for inp in [MVF, CPF, RMF]:
        execute(inp, data)
    assert execute("ls", data) == ['dir1', 'dir2', 'file2.txt']
    assert execute("ls dir1", data) == ['file0.txt', 'file1.txt', 'file2.txt']
    assert execute(f"ls {init_dir}\\.trash") == ['file3.txt']