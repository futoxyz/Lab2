import os

def fileordir(dir):
    try:
        os.listdir(dir)
        return "Dir"
    except:
        try:
            open(dir).close()
            return "File"
        except:
            return