import datetime


def log(s, initdir, userprint = True):
    if userprint:
        print(s)
    with open(f"{initdir}\\shell.log", "a") as f:
        f.write(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {s}\n")

def hist(s, initdir):
    with open(f"{initdir}\\.history", "a") as f:
        f.write(f"{s}\n")
