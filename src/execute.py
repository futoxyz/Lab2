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
                print(BADINPUT)
                log_output(BADINPUT)
                return
            try:
                os.chdir(newdir)
            except:
                print(NODIR)
                log_output(NODIR)

        case "ls":
            line.remove("ls")
            if not line:
                print(os.listdir())
                log_output(os.listdir())
            elif len(line) == 2:
                newdir = line.pop()
                if line.pop() != "-l":
                    print(BADINPUT)
                    log_output(BADINPUT)
                    return
                try:
                    with os.scandir(newdir) as files:
                        for file in files:
                            name = file.name
                            size = file.stat().st_size
                            mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                            mode = file.stat().st_mode
                            print(f"{name} - size: {size} B last edited: {mtime} permission: {mode}")
                            log_output(f"{name} - size: {size} B last edited: {mtime} permission: {mode}")
                except:
                    print(NODIR)
                    log_output(NODIR)
                    return
            elif line[0] == "-l":
                with os.scandir(".") as files:
                    for file in files:
                        name = file.name
                        size = file.stat().st_size
                        mtime = datetime.datetime.fromtimestamp(file.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        mode = file.stat().st_mode
                        print(f"{name} - size: {size} B last edited: {mtime} permission: {mode}")
                        log_output(f"{name} - size: {size} B last edited: {mtime} permission: {mode}")
            elif len(line) == 1:
                newdir = line.pop()
                try:
                    print(os.listdir(newdir))
                    log_output(os.listdir(newdir))
                except:
                    print(NODIR)
                    log_output(NODIR)
                    return
            else:
                print(BADINPUT)
                log_output(BADINPUT)

        case "cat":
            line.remove("cat")
            if line:
                newdir = line.pop()
            else:
                print(BADINPUT)
                log_output(BADINPUT)
                return
            try:
                with open(newdir) as f:
                    for ln in f:
                        print(ln.rstrip("\n"))
                        log_output(ln.rstrip("\n"))
            except:
                print(NOFILE)
                log_output(NOFILE)


        case "rm":
            line.remove("rm")
            if line:
                newdir = line.pop()
            else:
                print(BADINPUT)
                log_output(BADINPUT)
                return
            if not line:
                try:
                    os.remove(newdir)
                except:
                    print(NOFILE)
                    log_output(NOFILE)
                    return
            elif line.pop() == "-r":
                confirm(newdir)
            else:
                print(BADINPUT)
                log_output(BADINPUT)


        case "cp":
            line.remove("cp")
            if line:
                destdir = line.pop()
            else:
                print(BADINPUT)
                log_output(BADINPUT)
                return
            if line:
                newdir = line.pop()
            else:
                print(BADINPUT)
                log_output(BADINPUT)
                return

            if line and line.pop() == "-r":
                try:
                    os.listdir(newdir)
                except:
                    print(NODIR)
                    log_output(NODIR)
                    return
                try:
                    shutil.copytree(newdir, destdir, dirs_exist_ok=True)
                    print(SUCCESS)
                    log_output(SUCCESS)
                except:
                    print(FAILED)
                    log_output(FAILED)
                    return
            elif not line:
                try:
                    os.listdir(destdir)
                except:
                    print(NODIR)
                    log_output(NODIR)
                    return
                try:
                    open(newdir).close()
                except:
                    print(NOFILE)
                    log_output(NOFILE)
                    return
                try:
                    shutil.copy(newdir, destdir)
                    print(SUCCESS)
                    log_output(SUCCESS)
                except:
                    print(FAILED)
                    log_output(FAILED)


        case "mv":
            line.remove("mv")
            if line:
                destdir = line.pop()
            else:
                print(BADINPUT)
                log_output(BADINPUT)
                return
            if line:
                newdir = line.pop()
            else:
                print(BADINPUT)
                log_output(BADINPUT)
                return
            if not line and fileordir(newdir) is None:
                print(NOFD)
                log_output(NOFD)
                return
            elif not line:
                try:
                    os.listdir(destdir)
                except:
                    print(NODIR)
                    log_output(NODIR)
                    return
                try:
                    shutil.move(newdir, destdir)
                    print(SUCCESS)
                    log_output(SUCCESS)
                except:
                    print(FAILED)
                    log_output(FAILED)
                    return
            else:
                print(BADINPUT)
                log_output(BADINPUT)

                





        case _:
            print(BADINPUT)
            log_output(BADINPUT)





            
            
            





