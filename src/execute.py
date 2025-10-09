import os
import shutil
import datetime
from src.data import Data
from src.confirmation import confirm
from src.getname import getname
from src.constants import *


def execute(line, data):
    data.log(line, False)
    line = line.split()
    if line[0] != "history":
        data.hist(" ".join(line))
    match line[0]:
        case "cd":
            line.remove("cd")
            if line:
                new_dir = line.pop()
            else:
                new_dir = "."
            if line:
                data.log(BADINPUT)
                return
            try:
                os.chdir(new_dir)
            except:
                data.log(NODIR)

        case "ls":
            line.remove("ls")
            if not line:
                data.log(os.listdir())
            else:
                new_dir = line.pop()
                if not os.path.isdir(new_dir) and new_dir != "-l":
                    data.log(NODIR)
                    return
                elif new_dir == "-l":
                    new_dir = "."
                    line.append("-l")
                if not line:
                    data.log(os.listdir(new_dir))
                elif line.pop() == "-l" and not line:
                    with os.scandir(new_dir) as files:
                        for file in files:
                            name = file.name
                            size = file.stat().st_size
                            mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime).strftime("%d.%m.%Y %H:%M:%S")
                            mode = file.stat().st_mode
                            data.log(f"{name} - Size: {size} Bytes Last edited: {mtime} Permission: {mode}")
                else:
                    data.log(BADINPUT)

        case "cat":
            line.remove("cat")
            if line:
                new_dir = line.pop()
                if not os.path.isfile(new_dir):
                    data.log(NOFILE)
                    return
            else:
                data.log(BADINPUT)
                return
            if line:
                data.log(BADINPUT)
                return
            try:
                with open(new_dir) as f:
                    for ln in f:
                        data.log(ln.rstrip("\n"))
            except:
                data.log(NOFILE)

        case "rm":
            line.remove("rm")
            if line:
                new_dir = line.pop()
                if not os.path.isdir(new_dir) and not os.path.isfile(new_dir):
                    data.log(NOFD)
                    return
            else:
                data.log(BADINPUT)
                return
            if not line and os.path.isfile(new_dir):
                try:
                    shutil.copy(new_dir, f"{data.init_dir}/.trash/")
                    os.remove(new_dir)
                    data.log(SUCCESS)
                    data = Data(data.init_dir, last_exec="rm", fr_dir=new_dir)
                except:
                    data.log(FAILED)
            elif not line:
                data.log(NOFILE)
                return
            elif line.pop() == '-r' and not line and os.path.isdir(new_dir):
                if confirm(new_dir, data):
                    data = Data(data.init_dir, last_exec="rm", fr_dir=new_dir)
            else:
                data.log(BADINPUT)

        case "cp":
            line.remove("cp")
            if line:
                dest_dir = line.pop()
                if not os.path.isdir(dest_dir):
                    data.log(NODIR)
                    return
            else:
                data.log(BADINPUT)
                return
            if line:
                new_dir = line.pop()
                if not os.path.isdir(new_dir) and not os.path.isfile(new_dir):
                    data.log(NOFD)
                    return
            else:
                data.log(BADINPUT)
                return
            if not line and os.path.isfile(new_dir):
                try:
                    shutil.copy(new_dir, dest_dir)
                    data.log(SUCCESS)
                    data = Data(data.init_dir, last_exec="cp", fr_dir=new_dir, sc_dir=dest_dir)
                    return
                except:
                    data.log(FAILED)
            elif line and line.pop() == '-r' and not line:
                try:
                    shutil.copytree(new_dir, f"{dest_dir}/{getname(new_dir, True)}", dirs_exist_ok=True)
                    data.log(SUCCESS)
                except:
                    data.log(FAILED)
            else:
                data.log(BADINPUT)

        case "mv":
            line.remove("mv")
            if line:
                dest_dir = line.pop()
                if not os.path.isdir(dest_dir):
                    data.log(NODIR)
                    return
            else:
                data.log(BADINPUT)
                return
            if line:
                new_dir = line.pop()
                if not os.path.isdir(new_dir) and not os.path.isfile(new_dir):
                    data.log(NOFD)
                    return
            else:
                data.log(BADINPUT)
                return
            if not line:
                try:
                    shutil.move(new_dir, dest_dir)
                    data.log(SUCCESS)
                    data = Data(data.init_dir, last_exec="mv", fr_dir=new_dir, sc_dir=dest_dir)
                    return
                except:
                    data.log(FAILED)

            else:
                data.log(BADINPUT)

        case "zip":
            line.remove("zip")
            if line:
                name = line.pop()
                if not line:
                    data.log(BADINPUT)
                    return
                for sym in ["/", "\\", " ", ":", "*", "?", '"', "<", ">", "|"]:
                    if sym in name:
                        data.log(BADNAME)
                        return
                new_dir = line.pop()
                if os.path.isdir(new_dir):
                    try:
                        shutil.make_archive(name, "zip", new_dir)
                        data.log(SUCCESS)
                    except:
                        data.log(FAILED)
                else:
                    data.log(NODIR)
            else:
                data.log(BADINPUT)

        case "unzip":
            line.remove("unzip")
            if line:
                new_dir = line.pop()
                if line:
                    data.log(BADINPUT)
                    return
                if not os.path.isfile(new_dir) or ".zip" not in getname(new_dir):
                    data.log(NOFILE)
                    return
                try:
                    shutil.unpack_archive(new_dir, getname(new_dir).replace(".zip", ""), "zip")
                    data.log(SUCCESS)
                except:
                    data.log(FAILED)
                    return
            else:
                data.log(BADINPUT)
                return

        case "tar":
            line.remove("tar")
            if line:
                name = line.pop()
                if not line:
                    data.log(BADINPUT)
                    return
                for sym in ["/", "\\", " ", ":", "*", "?", '"', "<", ">", "|"]:
                    if sym in name:
                        data.log(BADNAME)
                        return
                new_dir = line.pop()
                if os.path.isdir(new_dir):
                    try:
                        shutil.make_archive(name, "gztar", new_dir)
                        data.log(SUCCESS)
                    except:
                        data.log(FAILED)
                else:
                    data.log(NODIR)
            else:
                data.log(BADINPUT)

        case "untar":
            line.remove("untar")
            if line:
                new_dir = line.pop()
                if line:
                    data.log(BADINPUT)
                    return
                if not os.path.isfile(new_dir) or ".tar.gz" not in getname(new_dir):
                    data.log(NOFILE)
                    return
                try:
                    shutil.unpack_archive(new_dir, getname(new_dir).replace(".tar.gz", ""), "gztar")
                    data.log(SUCCESS)
                except:
                    data.log(FAILED)
                    return
            else:
                data.log(BADINPUT)
                return

        case "history":
            line.remove("history")
            if not line:
                with open(f"{data.init_dir}\\.history") as f:
                    f = f.readlines()
                    if len(f) >= 5:
                        for i in range(5):
                            a = f[len(f) - i - 1].rstrip("\n")
                            data.log(f"#{i + 1} {a}")
                    else:
                        for ln in f:
                            a = ln.rstrip("\n")
                            data.log(f"#{f.index(ln) + 1} {a}")
            else:
                a = line.pop()
                try:
                    a = int(a)
                except:
                    data.log(BADINPUT)
                    return
                if a <= 0:
                    data.log(BADINPUT)
                    return
                with open(f"{data.init_dir}\\.history") as f:
                    f = f.readlines()
                    if not line and len(f) >= a:
                        for i in range(a):
                            b = f[len(f) - i - 1].rstrip("\n")
                            data.log(f"#{i + 1} {b}")
                    elif len(f) < a:
                        data.log(OUTHIS)
                    else:
                        data.log(BADINPUT)

        case "undo":
            line.remove("undo")
            if not line:
                data.undo()
            else:
                data.log(BADINPUT)






        case _:
            data.log(BADINPUT)
