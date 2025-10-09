import os

def getname(dir: object, folder: object = False) -> object:
    if "/" in dir:
        dir = dir.replace("/", "\\")
    dir = dir.split("\\")
    if os.path.isdir(dir) and folder or not folder:
        return dir[-1]
    elif len(dir) >= 2:
        return dir[-2]
    else:
        return "."
