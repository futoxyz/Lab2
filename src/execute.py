import os
import shutil
import datetime
from src.logging import log_input, log_output
from src.confirmation import confirm
from src.fileordir import fileordir
from src.constants import NODIR, NOFILE, NOFD, BADINPUT, FAILED, SUCCESS


def execute(line):
    log_input(line)
    line = line.split()
    match line[0]:
        case "cd":
            line.remove("cd")
            if line:
                newdir = line.pop()
            else:
                newdir = "."
            if line:
                log_output(BADINPUT)
                return
            try:
                os.chdir(newdir)
            except:
                log_output(NODIR)

        case "ls":
            line.remove("ls")
            if not line:
                log_output(os.listdir())
            elif len(line) == 2:
                newdir = line.pop()
                if fileordir(newdir) != "dir":
                    log_output(NODIR)
                    return
                if line.pop() != "-l":
                    log_output(BADINPUT)
                    return
                with os.scandir(newdir) as files:
                    for file in files:
                        name = file.name
                        size = file.stat().st_size
                        mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime).strftime("%d.%m.%Y %H:%M:%S")
                        mode = file.stat().st_mode
                        log_output(f"{name} - Size: {size} Bytes Last edited: {mtime} Permission: {mode}")
            elif line[0] == "-l":
                with os.scandir(".") as files:
                    for file in files:
                        name = file.name
                        size = file.stat().st_size
                        mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime).strftime("%d.%m.%Y %H:%M:%S")
                        mode = file.stat().st_mode
                        log_output(f"{name} - Size: {size} Bytes Last edited: {mtime} Permission: {mode}")
            elif len(line) == 1:
                newdir = line.pop()
                if fileordir(newdir) is None:
                    log_output(NODIR)
                    return
                log_output(os.listdir(newdir))
            else:
                log_output(BADINPUT)

        case "cat":
            line.remove("cat")
            if line:
                newdir = line.pop()
                if fileordir(newdir) != "file":
                    log_output(NODIR)
                    return
            else:
                log_output(BADINPUT)
                return
            if line:
                log_output(BADINPUT)
                return
            try:
                with open(newdir) as f:
                    for ln in f:
                        log_output(ln.rstrip("\n"))
            except:
                log_output(NOFILE)

        case "rm":
            line.remove("rm")
            if line:
                newdir = line.pop()
                if fileordir(newdir) is None:
                    log_output(NOFD)
                    return
            else:
                log_output(BADINPUT)
                return
            if not line and fileordir(newdir) == "file":
                try:
                    shutil.copy(newdir, ".trash")
                    os.remove(newdir)
                except:
                    log_output(FAILED)
            elif not line:
                log_output(NOFILE)
                return
            elif line.pop() == '-r' and not line:
                confirm(newdir)
            else:
                log_output(BADINPUT)

        case "cp":
            line.remove("cp")
            if line:
                destdir = line.pop()
                if fileordir(destdir) != "dir":
                    log_output(NODIR)
                    return
            else:
                log_output(BADINPUT)
                return
            if line:
                newdir = line.pop()
                if fileordir(newdir) is None:
                    log_output(NOFD)
                    return
            else:
                log_output(BADINPUT)
                return
            if not line:
                try:
                    shutil.copy(newdir, destdir)
                    log_output(SUCCESS)
                except:
                    log_output(FAILED)
            elif line.pop() == '-r' and not line:
                try:
                    if "/" in newdir:
                        newdir = newdir.replace("/", "\\")
                    shutil.copytree(newdir, f"{destdir}/{newdir.split('\\')[-1]}", dirs_exist_ok=True)
                    log_output(SUCCESS)
                except:
                    log_output(FAILED)
            else:
                log_output(BADINPUT)

        case "mv":
            line.remove("mv")
            if line:
                destdir = line.pop()
                if fileordir(destdir) != "dir":
                    log_output(NODIR)
                    return
            else:
                log_output(BADINPUT)
                return
            if line:
                newdir = line.pop()
                if fileordir(destdir) is None:
                    log_output(NOFD)
                    return
            else:
                log_output(BADINPUT)
                return
            if not line:
                try:
                    shutil.move(newdir, destdir)
                    log_output(SUCCESS)
                except:
                    log_output(FAILED)

            else:
                log_output(BADINPUT)

        case _:
            log_output(BADINPUT)
