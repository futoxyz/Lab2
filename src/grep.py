import re


def grep(pattern, file_dir, i):
    match i:
        case True:
            flag = re.IGNORECASE
        case False:
            flag = re.NOFLAG
    with open(file_dir) as f:
        lncount = 1
        lns = []
        for line in f:
            if re.search(pattern, line, flag):
                line = re.sub(pattern, f'"{pattern}"', line, flags=re.IGNORECASE)
                lns.append(f"{file_dir}: {lncount}. {line}")
            lncount += 1
        return "".join(lns)
