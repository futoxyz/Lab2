import pytest
import os
from src.data import Data
from src.execute import execute


def exec_test():
    '''
    Проверяет команды для изменения файлов (rm, cp, mv), а также команды cd и ls
    Редактирует файлы в /test_env
    :return: Ничего не возвращает
    '''
    init_dir = os.path.join(os.getcwd(), "tests", "test_env")
    data = Data(init_dir)
    execute("cd tests/test_env", data)
    assert execute("cd random\\directory", data) == "ERROR: No such directory"
    assert execute("undo", data) == "ERROR: Cannot undo any command currently"
    assert execute("ls random/directory", data) == "ERROR: No such directory"
    execute("mv file1.txt dir1", data)
    assert execute("ls", data) == "dir1\ndir2\nfile2.txt\nfile3.txt"
    execute("undo asdasd", data)
    assert execute("ls", data) == "dir1\ndir2\nfile1.txt\nfile2.txt\nfile3.txt"
    execute("mv dir2 dir1", data)
    assert execute("ls", data) == "dir1\nfile1.txt\nfile2.txt\nfile3.txt"
    assert execute("ls dir1", data) == "dir2\nfile0.txt"
    execute("undo", data)
    assert execute("undo", data) == "ERROR: Cannot undo any command currently"
    assert execute("ls /dir1", data) == "file0.txt"
    assert execute("ls", data) == "dir1\ndir2\nfile1.txt\nfile2.txt\nfile3.txt"
    execute("cp file2.txt ./dir1", data)
    assert execute("ls dir1", data) == "file0.txt\nfile2.txt"
    execute("undo", data)
    assert execute("ls dir1", data) == "file0.txt"
    execute("cp dir2 dir1 -r", data)
    assert execute("ls dir1/", data) == "dir2\nfile0.txt"
    execute("undo", data)
    assert execute("ls /dir1/", data) == "file0.txt"
    execute("rm file3.txt", data)
    assert execute("ls .", data) == "dir1\ndir2\nfile1.txt\nfile2.txt"
    execute("undo", data)
    assert execute("ls /", data) == "dir1\ndir2\nfile1.txt\nfile2.txt\nfile3.txt"
