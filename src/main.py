from sys import stdin
from os import getcwd
from src.execute import execute

def run():
    while inp := input(f"{getcwd()} > "):
        execute(inp)

        


if __name__ == "__main__":
    run()
