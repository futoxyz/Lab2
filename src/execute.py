import os
from src.logging import log_input, log_output
from src.constants import NODIR, BADINPUT

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
                print(f"ERROR: {BADINPUT}")
                log_output(BADINPUT)
                return
            try:
                os.chdir(newdir)
            except:
                print(f"ERROR: {NODIR}")
                log_output(NODIR)
                return
        case "ls":
            line.remove("ls")
            if not line:
                print(os.listdir())
            elif len(line) == 2:
                newdir = line.pop()
                if line.pop() != "-l":
                    print(f"ERROR: {BADINPUT}")
                    log_output(BADINPUT)
                    return
                

            elif line[0] == "-l":

            elif len(line) == 1:
                newdir = line.pop()
                try:
                    print(os.listdir(newdir))
                    log_output(os.listdir(newdir))
                except:
                    print(f"ERROR: {NODIR}")
                    log_output(NODIR)
                    return
            else:
                print(f"ERROR: {BADINPUT}")
                log_output(BADINPUT)
                return




            
            
            





