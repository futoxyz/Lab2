import os
import shutil
import datetime
from src.logging import log, hist
from src.confirmation import confirm
from src.getname import getname
from src.constants import *


def execute(line, initdir):
    log(line, initdir, False)
    line = line.split()
    if line[0] != "history":
        hist(" ".join(line), initdir)
    match line[0]:
        case "cd":
            line.remove("cd")
            if line:
                newdir = line.pop()
            else:
                newdir = "."
            if line:
                log(BADINPUT, initdir)
                return
            try:
                os.chdir(newdir)
            except:
                log(NODIR, initdir)

        case "ls":
            line.remove("ls")
            if not line:
                log(os.listdir(), initdir)
            else:
                newdir = line.pop()
                if not os.path.isdir(newdir) and newdir != "-l":
                    log(NODIR, initdir)
                    return
                elif newdir == "-l":
                    newdir = "."
                    line.append("-l")
                if not line:
                    log(os.listdir(newdir), initdir)
                elif line.pop() == "-l" and not line:
                    with os.scandir(newdir) as files:
                        for file in files:
                            name = file.name
                            size = file.stat().st_size
                            mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime).strftime("%d.%m.%Y %H:%M:%S")
                            mode = file.stat().st_mode
                            log(f"{name} - Size: {size} Bytes Last edited: {mtime} Permission: {mode}", initdir)
                else:
                    log(BADINPUT, initdir)

        case "cat":
            line.remove("cat")
            if line:
                newdir = line.pop()
                if not os.path.isfile(newdir):
                    log(NOFILE, initdir)
                    return
            else:
                log(BADINPUT, initdir)
                return
            if line:
                log(BADINPUT, initdir)
                return
            try:
                with open(newdir) as f:
                    for ln in f:
                        log(ln.rstrip("\n"), initdir)
            except:
                log(NOFILE, initdir)

        case "rm":
            line.remove("rm")
            if line:
                newdir = line.pop()
                if not os.path.isdir(newdir) and not os.path.isfile(newdir):
                    log(NOFD, initdir)
                    return
            else:
                log(BADINPUT, initdir)
                return
            if not line and os.path.isfile(newdir):
                try:
                    shutil.copy(newdir, f"{initdir}/.trash/")
                    os.remove(newdir)
                except:
                    log(FAILED, initdir)
            elif not line:
                log(NOFILE, initdir)
                return
            elif line.pop() == '-r' and not line and os.path.isdir(newdir):
                confirm(newdir, initdir)
            else:
                log(BADINPUT, initdir)

        case "cp":
            line.remove("cp")
            if line:
                destdir = line.pop()
                if not os.path.isdir(destdir):
                    log(NODIR, initdir)
                    return
            else:
                log(BADINPUT, initdir)
                return
            if line:
                newdir = line.pop()
                if not os.path.isdir(newdir) and not os.path.isfile(newdir):
                    log(NOFD, initdir)
                    return
            else:
                log(BADINPUT, initdir)
                return
            if not line and os.path.isfile(newdir):
                try:
                    shutil.copy(newdir, destdir)
                    log(SUCCESS, initdir)
                except:
                    log(FAILED, initdir)
            elif line and line.pop() == '-r' and not line:
                try:
                    shutil.copytree(newdir, f"{destdir}/{getname(newdir)}", dirs_exist_ok=True)
                    log(SUCCESS, initdir)
                except:
                    log(FAILED, initdir)
            else:
                log(BADINPUT, initdir)

        case "mv":
            line.remove("mv")
            if line:
                destdir = line.pop()
                if not os.path.isdir(destdir):
                    log(NODIR, initdir)
                    return
            else:
                log(BADINPUT, initdir)
                return
            if line:
                newdir = line.pop()
                if not os.path.isdir(newdir) and not os.path.isfile(newdir):
                    log(NOFD, initdir)
                    return
            else:
                log(BADINPUT, initdir)
                return
            if not line:
                try:
                    shutil.move(newdir, destdir)
                    log(SUCCESS, initdir)
                except:
                    log(FAILED, initdir)

            else:
                log(BADINPUT, initdir)

        case "zip":
            line.remove("zip")
            if line:
                name = line.pop()
                if not line:
                    log(BADINPUT, initdir)
                    return
                for sym in ["/", "\\", " ", ":", "*", "?", '"', "<", ">", "|"]:
                    if sym in name:
                        log(BADNAME, initdir)
                        return
                newdir = line.pop()
                if os.path.isdir(newdir):
                    try:
                        shutil.make_archive(name, "zip", newdir)
                        log(SUCCESS, initdir)
                    except:
                        log(FAILED, initdir)
                else:
                    log(NODIR, initdir)
            else:
                log(BADINPUT, initdir)

        case "unzip":
            line.remove("unzip")
            if line:
                newdir = line.pop()
                if line:
                    log(BADINPUT, initdir)
                    return
                if not os.path.isfile(newdir) or ".zip" not in getname(newdir):
                    log(NOFILE, initdir)
                    return
                try:
                    shutil.unpack_archive(newdir, getname(newdir).replace(".zip", ""), "zip")
                    log(SUCCESS, initdir)
                except:
                    log(FAILED, initdir)
                    return
            else:
                log(BADINPUT, initdir)
                return

        case "tar":
            line.remove("tar")
            if line:
                name = line.pop()
                if not line:
                    log(BADINPUT, initdir)
                    return
                for sym in ["/", "\\", " ", ":", "*", "?", '"', "<", ">", "|"]:
                    if sym in name:
                        log(BADNAME, initdir)
                        return
                newdir = line.pop()
                if os.path.isdir(newdir):
                    try:
                        shutil.make_archive(name, "gztar", newdir)
                        log(SUCCESS, initdir)
                    except:
                        log(FAILED, initdir)
                else:
                    log(NODIR, initdir)
            else:
                log(BADINPUT, initdir)

        case "untar":
            line.remove("untar")
            if line:
                newdir = line.pop()
                if line:
                    log(BADINPUT, initdir)
                    return
                if not os.path.isfile(newdir) or ".tar.gz" not in getname(newdir):
                    log(NOFILE, initdir)
                    return
                try:
                    shutil.unpack_archive(newdir, getname(newdir).replace(".tar.gz", ""), "gztar")
                    log(SUCCESS, initdir)
                except:
                    log(FAILED, initdir)
                    return
            else:
                log(BADINPUT, initdir)
                return

        case "history":
            line.remove("history")
            if not line:
                with open(f"{initdir}\\.history") as f:
                    f = f.readlines()
                    if len(f) >= 5:
                        for i in range(5):
                            log(f"#{i + 1} {f[len(f)-i-1].rstrip("\n")}", initdir)
                    else:
                        for ln in f:
                            log(f"#{f.index(ln) + 1} {ln.rstrip("\n")}", initdir)
            else:
                a = line.pop()
                try:
                    a = int(a)
                except:
                    log(BADINPUT, initdir)
                    return
                if a <= 0:
                    log(BADINPUT, initdir)
                    return
                with open(f"{initdir}\\.history") as f:
                    f = f.readlines()
                    if not line and len(f) >= a:
                        for i in range(a):
                            log(f"#{i + 1} {f[len(f) - i - 1].rstrip("\n")}", initdir)
                    elif len(f) < a:
                        log(OUTHIS, initdir)
                    else:
                        log(BADINPUT, initdir)






        case _:
            log(BADINPUT, initdir)
