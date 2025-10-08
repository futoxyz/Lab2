from os import getcwd, chdir
from src.execute import execute

def run():
    chdir("C:/Users/fedor/Downloads")
    while inp := input(f"{getcwd()} > "):
        execute(inp)

        


if __name__ == "__main__":
    run()
