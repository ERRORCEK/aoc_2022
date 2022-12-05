from collections import namedtuple
from copy import deepcopy
from string import ascii_uppercase

def parse_input(filename: str = "input") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

stacks = [[] for _ in range(20)]

it = iter(parse_input("input.txt"))

# Parse input stacks
while True:
    line = next(it)
    if line.startswith(" 1"):
        break
    for i, c in enumerate(line):
        if c in ascii_uppercase:
            real_index = (i - 1) // 4
            stacks[real_index].append(c)

for i in range(len(stacks) -1, -1, -1):
    if stacks[i]:
        del stacks[i+1:]
        break

next(it)

MoveCommand = namedtuple("MoveCommand", ("count", "src", "dest"))

def parse_commands():
    cmd = []
    for _line in it:
        parts = _line.split(" ")
        count = int(parts[1])
        src = int(parts[3]) - 1
        dest = int(parts[5]) - 1
        cmd.append(MoveCommand(count, src, dest))
    return cmd

commands = parse_commands()

stacks_orig = deepcopy(stacks) # Saving for part 2

# Part 1
def exec_move(cmd):
    for _ in range(cmd.count):
        stacks[cmd.dest].insert(0, stacks[cmd.src].pop(0))

for _cmd in commands:
    exec_move(_cmd)

print("".join(i[0] for i in stacks))

stacks = stacks_orig

# Part 2
def exec_move2(cmd):
    temp = []
    for _ in range(cmd.count):
        temp.append(stacks[cmd.src].pop(0))
    stacks[cmd.dest] = temp + stacks[cmd.dest]

for _cmd in commands:
    exec_move2(_cmd)

print("".join(i[0] for i in stacks))
