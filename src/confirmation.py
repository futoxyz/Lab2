import shutil
from src.logging import log_input, log_output
from src.constants import NODIR, FAILED, CANCEL, INVANS, RMREST

def confirm(newdir):
    if newdir == ".." or newdir == "/":
        print(RMREST)
        log_output(RMREST)
        return
    try:
        shutil.disk_usage(newdir)
    except:
        print(NODIR)
        log_output(NODIR)
        return
    enter = str(input("Do you want to continue? (Y/N) > "))
    log_input(enter)
    while enter not in ["Y", "y", "N", "n"]:
        print(INVANS)
        log_output(INVANS)
        enter = str(input("Do you want to continue? (Y/N) > "))
    if enter in ["Y", "y"]:
        try:
            shutil.rmtree(newdir)
        except:
            print(FAILED)
            log_output(FAILED)
    if enter in ["N", "n"]:
        print(CANCEL)
        log_output(CANCEL)

