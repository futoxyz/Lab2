import os
import shutil
import datetime
import shlex
from argparse import ArgumentParser
from src.confirmation import confirm
from src.getname import getname
from src.constants import *


def execute(inp, data):
    '''
    Обрабатывает ввод и выполняет команды. Для каждой команды происходит парсинг.
    :param inp: Ввод пользователя.
    :param data: Объект, хранящий в себе лишь исходную директорию, и позволяющий сохранять логи, историю и проводить undo.
    :return: None
    '''
    data.log(inp, False)
    inp = shlex.split(inp)
    parse = ArgumentParser(prog="Command", exit_on_error=False)
    if inp[0] != "history":
        data.hist(" ".join(inp))
    match inp[0]:
        case "cd":
            inp.remove("cd")
            parse.add_argument("new_dir", nargs="?")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if not line.new_dir:
                return
            try:
                os.chdir(line.new_dir)
            except:
                data.log(NODIR)
        case "ls":
            inp.remove("ls")
            parse.add_argument("-l", action="store_true")
            parse.add_argument("dir", nargs="?")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if not line.dir:
                line.dir = "."
            if not os.path.isdir(line.dir):
                data.log(NODIR)
                return
            if not line.l:
                data.log(os.listdir(line.dir))
            else:
                with os.scandir(line.dir) as files:
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
            parse.add_argument("file_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if not os.path.isfile(line.file_dir):
                data.log(NOFILE)
            else:
                with open(line.file_dir) as f:
                    data.log("".join(f))

        case "rm":
            '''
            При успешном выполнении передает data команду rm директорию удаления, sc_dir остается без изменений.
            '''
            inp.remove("rm")
            parse.add_argument("-r", action="store_true")
            parse.add_argument("rm_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if os.path.isfile(line.rm_dir) and not line.r:
                try:
                    shutil.copy(line.rm_dir, f"{data.init_dir}\\.trash")
                    os.remove(line.rm_dir)
                    data.log(SUCCESS)
                    data.last_exec = "rm"
                    data.fr_dir = os.path.abspath(line.rm_dir)
                except:
                    data.log(FAILED)
            elif os.path.isdir(line.rm_dir) and line.r and confirm(line.rm_dir, data):
                    '''
                    Выполняется при успешном подтверждении пользователя.
                    '''
                    data.log(SUCCESS)
                    data.last_exec = "rm"
                    data.fr_dir = os.path.abspath(line.rm_dir)
            elif not os.path.isdir(line.rm_dir) or not line.r:
                data.log(NOFD)

        case "cp":
            '''
            При успешном выполнении передает data команду cp, исходную директорию и директорию копирования.
            '''
            inp.remove("cp")
            parse.add_argument("-r", action="store_true")
            parse.add_argument("cp_dir")
            parse.add_argument("dest_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if os.path.isfile(line.cp_dir) and os.path.isdir(line.dest_dir) and not line.r:
                try:
                    shutil.copy(line.cp_dir, line.dest_dir)
                    data.log(SUCCESS)
                    data.last_exec = "cp"
                    data.fr_dir = os.path.abspath(line.cp_dir)
                    data.sc_dir = os.path.abspath(line.dest_dir)
                except:
                    data.log(FAILED)
            elif os.path.isdir(line.cp_dir) and os.path.isdir(line.dest_dir) and line.r:
                try:
                    shutil.copytree(line.cp_dir, f"{line.dest_dir}/{getname(line.cp_dir, True)}", dirs_exist_ok=True)
                    data.last_exec = "cp"
                    data.fr_dir = os.path.abspath(line.cp_dir)
                    data.sc_dir = os.path.abspath(line.dest_dir)
                    data.log(SUCCESS)
                except:
                    data.log(FAILED)
            else:
                data.log(NOFD)

        case "mv":
            '''
            При успешном выполнении передает data команду mv, исходную директорию и директорию перемещения.
            '''
            inp.remove("mv")
            parse.add_argument("mv_dir")
            parse.add_argument("dest_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if (os.path.isfile(line.mv_dir) or os.path.isdir(line.mv_dir)) and os.path.isdir(line.dest_dir):
                try:
                    shutil.move(line.mv_dir, line.dest_dir)
                    data.log(SUCCESS)
                    data.last_exec = "mv"
                    data.fr_dir = os.path.abspath(line.mv_dir)
                    data.sc_dir = os.path.abspath(line.dest_dir)
                except:
                    data.log(FAILED)
                    return
            else:
                data.log(NOFD)

        case "zip":
            '''
            Название архива не может содержать некоторые символы.
            '''
            inp.remove("zip")
            parse.add_argument("archive_dir")
            parse.add_argument("fname")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            for sym in ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]:
                if sym in line.fname:
                    data.log(BADNAME)
                    return
            if os.path.isdir(line.archive_dir) or os.path.isfile(line.archive_dir):
                try:
                    shutil.make_archive(line.fname, "zip", line.archive_dir)
                    data.log(SUCCESS)
                except:
                    data.log(FAILED)
            else:
                data.log(NOFD)

        case "unzip":
            inp.remove("unzip")
            parse.add_argument("archive_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if not os.path.isfile(line.archive_dir) or ".zip" not in getname(line.archive_dir):
                data.log(NOFILE)
                return
            try:
                shutil.unpack_archive(line.archive_dir, getname(line.archive_dir).replace(".zip", ""), "zip")
                data.log(SUCCESS)
            except:
                data.log(FAILED)

        case "tar":
            inp.remove("tar")
            parse.add_argument("archive_dir")
            parse.add_argument("fname")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            for sym in ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]:
                if sym in line.fname:
                    data.log(BADNAME)
                    return
            if os.path.isdir(line.archive_dir) or os.path.isfile(line.archive_dir):
                try:
                    shutil.make_archive(line.fname, "gztar", line.archive_dir)
                    data.log(SUCCESS)
                except:
                    data.log(FAILED)
            else:
                data.log(NOFD)

        case "untar":
            inp.remove("untar")
            parse.add_argument("archive_dir")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if not os.path.isfile(line.archive_dir) or ".tar.gz" not in getname(line.archive_dir):
                data.log(NOFILE)
                return
            try:
                shutil.unpack_archive(line.archive_dir, getname(line.archive_dir).replace(".tar.gz", ""), "gztar")
                data.log(SUCCESS)
            except:
                data.log(FAILED)

        case "history":
            '''
            По умолчанию выводит до 5 последних команд.
            '''
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
            '''
            При успешной отмене у объекта data последняя команда заменяется на None.
            '''
            if data.undo():
                data.last_exec = None






        case _:
            data.log(NOCMD)
