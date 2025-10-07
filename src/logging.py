import datetime


def log_input(s):
    with open("C:/Users/fedor/OneDrive/Documents/lab2/shell.log", "a") as f:
            f.write(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {s}\n")

def log_output(s):
     with open("C:/Users/fedor/OneDrive/Documents/lab2/shell.log", "a") as f:
            f.write(f"[{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {s}\n")
    