import pytest
import os
from src.data import Data
from src.execute import execute
from src.grep import grep

def reading_test():
    '''
    Проверка команд для чтения файлов (cat и grep)
    Читает файлы из /test_env
    :return: Ничего не возвращает
    '''
    init_dir = os.path.join(os.getcwd(), "tests")
    os.chdir(init_dir)
    data = Data(init_dir)
    assert execute("cat test_env/dir2/file0.txt", data) == 'This file supposed to stay in dir2/ and only be read.\n\nPattern is shown with -i.'
    assert execute("cat          test_env\\dir2\\file01.txt", data) == 'This file supposed to stay in dir1/ and     only be read.\n\npattern is shown with no -i.'
    assert execute("cat nonexistingfile.txt", data) == "ERROR: No such file in directory"
    assert execute("cat first_argument.txt exceptional_argument", data) == "ERROR: Wrong command input"
    assert grep("pattern", os.path.join(init_dir, "test_env", "dir2", "file0.txt"), False) == "No pattern was found"
    assert grep("pattern", os.path.join(init_dir, "test_env", "dir2", "file0.txt"), True) == f'File {os.path.join(init_dir, "test_env", "dir2", "file0.txt")}: line 3 - "pattern" is shown with -i.'
    assert execute("grep -r pattern test_env\\dir2", data) == f'File {os.path.join(init_dir, "test_env", "dir2", "file01.txt")}: line 3 - "pattern" is shown with no -i.'
    assert execute("grep -r pattern -i test_env\\dir2", data) == f'File {os.path.join(init_dir, "test_env", "dir2", "file0.txt")}: line 3 - "pattern" is shown with -i.\nFile {os.path.join(init_dir, "test_env", "dir2", "file01.txt")}: line 3 - "pattern" is shown with no -i.'
    assert execute("grep pattern test_env/dir2", data) == "ERROR: No such file or directory"
    assert execute("grep -r test_env/dir2 pattern", data) == "ERROR: No such file or directory"
    assert execute("grep first_arg second_arg exceptional_arg", data) == "ERROR: Wrong command input"
