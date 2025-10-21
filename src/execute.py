import os
import shutil
import datetime
import shlex
from argparse import ArgumentParser
from src.grep import grep
from src.confirmation import confirm
from src.constants import *


def execute(inp, data):
    '''
    Обрабатывает ввод и выполняет команды. Для каждой команды происходит парсинг под их формат.
    :param inp: Ввод пользователя.
    :param data: Объект, хранящий в себе лишь исходную директорию, и позволяющий сохранять логи, историю и проводить undo.
    :return: None
    '''
    data.log(inp, False)
    inp = shlex.split(inp, posix=False)
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
                data.log("\n".join(os.listdir(line.dir)))
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
                    shutil.move(line.rm_dir, os.path.join(data.init_dir, ".trash"))
                    data.log(SUCCESS)
                    data.last_exec = "rm"
                    data.fr_dir = os.path.abspath(line.rm_dir)
                except:
                    data.log(FAILED)
            elif os.path.isdir(line.rm_dir) and line.r:
                if line.rm_dir == ".." or line.rm_dir == "/":
                    data.log(RMREST)
                    return
                ans = confirm(data)
                if ans:
                    try:
                        shutil.move(line.rm_dir, os.path.join(data.init_dir, ".trash", os.path.basename(line.rm_dir)))
                        data.log(SUCCESS)
                        data.last_exec = "rm"
                        data.fr_dir = os.path.abspath(line.rm_dir)
                    except:
                        data.log(FAILED)
                else:
                    data.log(CANCEL)
            else:
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
                    shutil.copytree(line.cp_dir, os.path.join(line.dest_dir, os.path.basename(line.cp_dir)), dirs_exist_ok=True)
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
            if not os.path.isfile(line.archive_dir) or ".zip" not in os.path.basename(line.archive_dir):
                data.log(NOFILE)
                return
            try:
                shutil.unpack_archive(line.archive_dir, os.path.basename(line.archive_dir).replace(".zip", ""), "zip")
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
            if not os.path.isfile(line.archive_dir) or ".tar.gz" not in os.path.basename(line.archive_dir):
                data.log(NOFILE)
                return
            try:
                shutil.unpack_archive(line.archive_dir, os.path.basename(line.archive_dir).replace(".tar.gz", ""), "gztar")
                data.log(SUCCESS)
            except:
                data.log(FAILED)

        case "history":
            '''
            По умолчанию выводит 5 (или меньше) последних команд.
            '''
            inp.remove("history")
            parse.add_argument("num", nargs="?")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return

            if not line.num:
                with open(os.path.join(data.init_dir, ".history")) as f:
                    f = f.readlines()
                    lns = []
                    if len(f) >= 5:
                        for i in range(5):
                            a = f[len(f) - i - 1].rstrip("\n")
                            lns.append(f"{i + 1}. {a}")
                        data.log("\n".join(lns))
                    else:
                        for ln in f:
                            a = ln.rstrip("\n")
                            lns.append(f"{f.index(ln) + 1}. {a}")
                        data.log("\n".join(lns))
            elif line.num.isdigit() and int(line.num) > 0:
                line.num = int(line.num)
                with open(os.path.join(data.init_dir, ".history")) as f:
                    f = f.readlines()
                    lns = []
                    if len(f) >= line.num:
                        for i in range(line.num):
                            b = f[len(f) - i - 1].rstrip("\n")
                            lns.append(f"{i + 1}. {b}")
                        data.log("\n".join(lns))
                    elif len(f) < line.num:
                        data.log(OUTHIS)
            else:
                data.log(BADINPUT)

        case "undo":
            '''
            При успешной отмене у объекта data последняя команда заменяется на None, fr_dir и sc_dir остаются.
            '''
            if data.undo():
                data.last_exec = None

        case "grep":
            inp.remove("grep")
            parse.add_argument("pattern")
            parse.add_argument("dir")
            parse.add_argument("-i", action="store_true")
            parse.add_argument("-r", action="store_true")
            try:
                line = parse.parse_args(inp)
            except:
                data.log(BADINPUT)
                return
            if os.path.isfile(line.dir) and not line.r:
                res = grep(line.pattern, os.path.abspath(line.dir), line.i)[:-1]
                data.log(res if res else NOTFOUND)
            elif os.path.isdir(line.dir) and line.r:
                complete_res = []
                for address, dirs, files in os.walk(line.dir):
                    for name in files:
                        res = grep(line.pattern, os.path.join(address, name), line.i)
                        if res:
                            complete_res.append(res)
                data.log("".join(complete_res) if complete_res else NOTFOUND)
            else:
                data.log(NOFD)

        case _:
            data.log(NOCMD)
