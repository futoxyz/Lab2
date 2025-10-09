from os import getcwd, chdir
from src.execute import execute

def run():
    initdir = getcwd()
    while inp := input(f"{getcwd()} > "):
        execute(inp, initdir)

        


if __name__ == "__main__":
    run()
