import shutil
from src.logging import log_input, log_output
from constants import FAILED, CANCEL

def confirm(newdir):
    enter = str(input("Do you want to continue? (Y/N)"))
    log_input(enter)
    if enter == "Y" or enter == "y":
        try:
            shutil.rmtree(newdir)
        except:
            print(FAILED)
            log_output(FAILED)
    else:
        print(CANCEL)
        log_output(CANCEL)

