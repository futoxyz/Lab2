import shutil
from src.logging import log_input, log_output
from src.constants import NODIR, FAILED, CANCEL

def confirm(newdir):
    try:
        shutil.disk_usage(newdir)
    except:
        print(NODIR)
        log_output(NODIR)
        return
    enter = str(input("Do you want to continue? (Y/N) > "))
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

