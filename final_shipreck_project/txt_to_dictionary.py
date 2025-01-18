def read_file(dir: str) -> list[list[any]]:
    with open(dir, "r") as file:
        lines = file.readlines()
        file.close()
    
    for line in range(len(lines)):
        lines[line] = lines[line].strip()
        lines[line] = lines[line].split(" ")
    
    for i in range(len(lines)):
        lines[i] = check_int(lines[i])
    
    return lines

def check_int(info: list[str]) -> list[any]:
    l = []
    for line in info:
        if line.isnumeric():
            x = int(line)
            l.append(x)
        else:
            l.append(line)
    return l

def to_dict(info: list[str]) -> dict:
    d = {}
    key = None
    value = None
    for i, line in enumerate(info):
        if i % 2 == 0:
            key = line
        else:
            value = line
            d[key] = value
    return d

def get_all_dict(dir: str) -> list[dict]:
    d = []
    info = read_file(dir)
    for inf in info:
        d.append(to_dict(inf))
    return d