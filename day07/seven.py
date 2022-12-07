from dataclasses import dataclass
from operator import attrgetter

def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

@dataclass
class File:
    name: str
    size: int

@dataclass
class Directory:
    name: str
    parent: "Directory"
    children: list
    total_size: int = 0

root = Directory("/", None, [])
pwd = root

lines = parse_input()
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("$ cd "):
        new_path = line[5:]
        if new_path == "/":
            pwd = root
        elif new_path == "..":
            pwd = pwd.parent
        else:
            for child in pwd.children:
                if isinstance(child, Directory) and child.name == new_path:
                    pwd = child
                    break
        i += 1
    elif line.startswith("$ ls"):
        i += 1
        while i < len(lines) and not lines[i].startswith("$"):
            line = lines[i]
            code, name = line.split(" ")
            if code == "dir":
                pwd.children.append(Directory(name, pwd, []))
            else:
                pwd.children.append(File(name, int(code)))
            i += 1

def calculate_size(node) -> int:
    if isinstance(node, File):
        return node.size
    node.total_size = sum(calculate_size(child) for child in node.children)
    return node.total_size

calculate_size(root)

def directories(node) -> Directory:
    if isinstance(node, Directory):
        yield node
        for _child in node.children:
            yield from directories(_child)

def part_1() -> int:
    count = 0
    for directory in directories(root):
        if directory.total_size <= 100000:
            count += directory.total_size
    return count

def part_2() -> int:
    unused_space = 70000000 - root.total_size
    must_delete = 30000000 - unused_space
    big_enough = (d for d in directories(root) if d.total_size >= must_delete)

    return min(big_enough, key=attrgetter("total_size")).total_size

if __name__ == "__main__":
    print(part_1())
    print(part_2())
