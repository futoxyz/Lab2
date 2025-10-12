import os

def getname(dir, folder= False):
    if "/" in dir:
        dir = dir.replace("/", "\\")
    if os.path.isdir(dir) and folder or not folder:
        return dir.split("\\")[-1]
    elif len(dir) >= 2:
        return dir.split("\\")[-2]
    else:
        return "."
