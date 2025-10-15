import shutil
from src.getname import getname
from src.constants import INVANS, RMREST, CANCEL

def confirm(new_dir, data):
    if new_dir == ".." or new_dir == "/":
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
            shutil.copytree(new_dir, f"{data.init_dir}\\.trash\\{getname(new_dir, True)}")
            shutil.rmtree(new_dir)
            return True
        except:
            return
    else:
        data.log(CANCEL)
        return

