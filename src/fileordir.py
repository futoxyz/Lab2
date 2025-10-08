import os

def fileordir(dir):
    if os.path.isdir(dir):
        return "dir"
    elif os.path.isfile(dir):
        return "file"
    else:
        return