from os import getcwd
from src.data import Data
from src.execute import execute

def run():
    init_dir = getcwd()
    data = Data(init_dir)
    execute.log = data.log
    execute.hist = data.hist
    while inp := input(f"{getcwd()} > "):
        execute(inp, data)

        


if __name__ == "__main__":
    run()
