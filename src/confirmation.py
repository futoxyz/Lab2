import shutil
from src.logging import log
from src.constants import FAILED, CANCEL, INVANS, RMREST, SUCCESS

def confirm(newdir, initdir):
    if newdir == ".." or newdir == "/":
        log(RMREST, initdir)
        return
    enter = str(input("Do you want to continue? (Y/N) > "))
    log(enter, initdir, False)
    while enter not in ["Y", "y", "N", "n"]:
        log(INVANS, initdir)
        enter = str(input("Do you want to continue? (Y/N) > "))
        log(enter, initdir, False)
    if enter in ["Y", "y"]:
        try:
            shutil.copytree(newdir, f"{initdir}/.trash/")
            shutil.rmtree(newdir)
            log(SUCCESS, initdir)
        except:
            log(FAILED, initdir)
    else:
        log(CANCEL, initdir)

