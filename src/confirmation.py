import shutil
from src.data import Data
from src.constants import FAILED, CANCEL, INVANS, RMREST, SUCCESS

def confirm(newdir, data):
    if newdir == ".." or newdir == "/":
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
            shutil.copytree(newdir, f"{data.init_dir}/.trash/")
            shutil.rmtree(newdir)
            data.log(SUCCESS)
            return True
        except:
            data.log(FAILED)
            return
    else:
        data.log(CANCEL)
        return

