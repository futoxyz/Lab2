import shutil
import os
from src.logging import log_input, log_output
from src.constants import NODIR, FAILED, CANCEL, INVANS, RMREST

def confirm(newdir):
    if newdir == ".." or newdir == "/":
        log_output(RMREST)
        return
    try:
        os.listdir(newdir)
    except:
        log_output(NODIR)
        return
    enter = str(input("Do you want to continue? (Y/N) > "))
    log_input(enter)
    while enter not in ["Y", "y", "N", "n"]:
        log_output(INVANS)
        enter = str(input("Do you want to continue? (Y/N) > "))
    if enter in ["Y", "y"]:
        try:
            shutil.copytree(newdir, ".trash")
            shutil.rmtree(newdir)
        except:
            log_output(FAILED)
    if enter in ["N", "n"]:
        log_output(CANCEL)

