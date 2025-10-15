import os
import shutil
import datetime
from argparse import ArgumentParser
from src.confirmation import confirm
from src.getname import getname
from src.constants import *


def execute(inp, data):
    data.log(inp, False)
    inp = inp.split()
    parse = ArgumentParser(prog="command", exit_on_error=False)
    if inp[0] != "history":
        data.hist(" ".join(inp))
    match inp[0]:
        case "cd":
            inp.remove("cd")
            parse.add_argument("new_dir", nargs="?")
            line = parse.parse_args(inp)
            if not line.new_dir:
                line.new_dir = "."
            try:
                os.chdir(line.new_dir)
            except:
                data.log(NODIR)
        case "ls":
            inp.remove("ls")
            parse.add_argument("-l", action="store_true")
            parse.add_argument("new_dir", nargs="?")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if not line.new_dir:
                line.new_dir = "."
            if not os.path.isdir((line.new_dir)):
                data.log(NODIR)
                return
            if not line.l:
                data.log(os.listdir(line.new_dir))
            else:
                with os.scandir(line.new_dir) as files:
                    ls = []
                    for file in files:
                        fname = file.name
                        size = file.stat().st_size
                        mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime).strftime("%d.%m.%Y %H:%M:%S")
                        mode = file.stat().st_mode
                        ls.append(f"{fname} - Size: {size} Bytes Last edited: {mtime} Permission: {mode}\n")
                    data.log("".join(ls)[:-1])

        case "cat":
            inp.remove("cat")
            parse.add_argument("new_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if not os.path.isfile(line.new_dir):
                data.log(NOFILE)
            else:
                with open(line.new_dir) as f:
                    data.log("".join(f))

        case "rm":
            inp.remove("rm")
            parse.add_argument("-r", action="store_true")
            parse.add_argument("new_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if os.path.isfile(line.new_dir) and not line.r:
                try:
                    os.remove(line.new_dir)
                    data.log(SUCCESS)
                    data.last_exec = "rm"
                    data.fr_dir = os.path.abspath(line.new_dir)
                except:
                    data.log(FAILED)
            elif os.path.isdir(line.new_dir) and line.r and confirm(line.new_dir, data):
                    data.log(SUCCESS)
                    data.last_exec = "rm"
                    data.fr_dir = os.path.abspath(line.new_dir)
            else:
                data.log(NOFD)

        case "cp":
            inp.remove("cp")
            parse.add_argument("-r", action="store_true")
            parse.add_argument("new_dir")
            parse.add_argument("dest_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if os.path.isfile(line.new_dir) and os.path.isdir(line.new_dir) and not line.r:
                try:
                    shutil.copy(line.new_dir, line.dest_dir)
                    data.log(SUCCESS)
                    data.last_exec = "cp"
                    data.fr_dir = os.path.abspath(line.new_dir)
                    data.sc_dir = os.path.abspath(line.dest_dir)
                except:
                    data.log(FAILED)
            elif os.path.isdir(line.new_dir) and os.path.isdir(line.new_dir) and line.r:
                try:
                    shutil.copytree(line.new_dir, f"{line.dest_dir}/{getname(line.new_dir, True)}", dirs_exist_ok=True)
                    data.last_exec = "cp"
                    data.fr_dir = os.path.abspath(line.new_dir)
                    data.sc_dir = os.path.abspath(line.dest_dir)
                    data.log(SUCCESS)
                except:
                    data.log(FAILED)
            else:
                data.log(NOFD)

        case "mv":
            inp.remove("mv")
            parse.add_argument("new_dir")
            parse.add_argument("dest_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if (os.path.isfile(line.new_dir) or os.path.isdir(line.new_dir)) and os.path.isdir(line.dest_dir):
                try:
                    shutil.move(line.new_dir, line.dest_dir)
                    data.log(SUCCESS)
                    data.last_exec = "mv"
                    data.fr_dir = os.path.abspath(line.new_dir)
                    data.sc_dir = os.path.abspath(line.dest_dir)
                except:
                    data.log(FAILED)
            else:
                data.log(NOFD)

        case "zip":
            inp.remove("zip")
            parse.add_argument("new_dir")
            parse.add_argument("fname")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            for sym in ["/", "\\", " ", ":", "*", "?", '"', "<", ">", "|"]:
                if sym in line.fname:
                    data.log(BADNAME)
                    return
            if os.path.isdir(line.new_dir) or os.path.isfile(line.new_dir):
                try:
                    shutil.make_archive(line.fname, "zip", line.new_dir)
                    data.log(SUCCESS)
                except:
                    data.log(FAILED)
            else:
                data.log(NOFD)

        case "unzip":
            inp.remove("unzip")
            parse.add_argument("new_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if not os.path.isfile(line.new_dir) or ".zip" not in getname(line.new_dir):
                data.log(NOFILE)
                return
            try:
                shutil.unpack_archive(line.new_dir, getname(line.new_dir).replace(".zip", ""), "zip")
                data.log(SUCCESS)
            except:
                data.log(FAILED)

        case "tar":
            inp.remove("tar")
            parse.add_argument("new_dir")
            parse.add_argument("fname")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            for sym in ["/", "\\", " ", ":", "*", "?", '"', "<", ">", "|"]:
                if sym in line.fname:
                    data.log(BADNAME)
                    return
            if os.path.isdir(line.new_dir) or os.path.isfile(line.new_dir):
                try:
                    shutil.make_archive(line.fname, "gztar", line.new_dir)
                    data.log(SUCCESS)
                except:
                    data.log(FAILED)
            else:
                data.log(NOFD)

        case "untar":
            inp.remove("untar")
            parse.add_argument("new_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if not os.path.isfile(line.new_dir) or ".tar.gz" not in getname(line.new_dir):
                data.log(NOFILE)
                return
            try:
                shutil.unpack_archive(line.new_dir, getname(line.new_dir).replace(".tar.gz", ""), "gztar")
                data.log(SUCCESS)
            except:
                data.log(FAILED)

        case "history":
            inp.remove("history")
            parse.add_argument("num", nargs="?")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return

            if not line.num:
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
            elif line.num.isdigit() and int(line.num) > 0:
                line.num = int(line.num)
                with open(f"{data.init_dir}\\.history") as f:
                    f = f.readlines()
                    if len(f) >= line.num:
                        for i in range(line.num):
                            b = f[len(f) - i - 1].rstrip("\n")
                            data.log(f"{i + 1}. {b}")
                    elif len(f) < line.num:
                        data.log(OUTHIS)
            else:
                data.log(BADINPUT)

        case "undo":
            inp.remove("undo")
            if data.undo():
                data.last_exec = None






        case _:
            data.log(BADINPUT)
