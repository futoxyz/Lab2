import datetime
import os
from src.constants import FAILED, SUCCESS, NOUNDO
from src.getname import getname
import shutil

class Data:
    def __init__(self, init_dir, last_exec = None, fr_dir = None, sc_dir = None):
        self.init_dir = init_dir
        self.last_exec = last_exec
        self.fr_dir = fr_dir
        self.sc_dir = sc_dir

    def log(self, s, userprint=True):
        if userprint:
            print(s)
        with open(f"{self.init_dir}\\shell.log", "a") as f:
            f.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {s}\n")

    def hist(self, s):
        with open(f"{self.init_dir}\\.history", "a") as f:
            f.write(f"{s}\n")

    def undo(self):
        match self.last_exec:
            case "mv":
                try:
                    shutil.move(f"{self.sc_dir}\\{getname(self.fr_dir)}", f"{self.fr_dir}\\..")
                    Data.log(self, SUCCESS)
                    return True
                except:
                    Data.log(self, FAILED)

            case "cp":
                try:
                    if os.path.isdir(self.fr_dir):
                        try:
                            shutil.rmtree(f"{self.sc_dir}\\{getname(self.fr_dir)}")
                        except:
                            Data.log(self, FAILED)
                            return
                    else:
                        try:
                            os.remove(f"{self.sc_dir}\\{getname(self.fr_dir)}")
                        except:
                            Data.log(self, FAILED)
                            return
                    Data.log(self, SUCCESS)
                    return True
                except:
                    Data.log(self, FAILED)

            case "rm":
                if os.path.isdir(self.fr_dir):
                    try:
                        shutil.move(f"{self.init_dir}\\.trash\\{getname(self.fr_dir)}", f"{self.fr_dir}\\..")
                    except:
                        Data.log(self, FAILED)
                        return
                else:
                    try:
                        shutil.move(f"{self.init_dir}\\.trash\\{getname(self.fr_dir)}", f"{self.fr_dir}\\..")
                    except:
                        Data.log(self, FAILED)
                        return
                Data.log(self, SUCCESS)
                return True

            case None:
                Data.log(self, NOUNDO)





