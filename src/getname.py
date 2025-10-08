def getname(dir):
    if "/" in dir:
        dir = dir.replace("/", "\\")
    dir = dir.split("\\")
    return dir[-1]