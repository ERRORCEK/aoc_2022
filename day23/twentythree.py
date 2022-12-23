from collections import defaultdict

def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

lines = parse_input()
init_positions = set(complex(x, y) for y, row in enumerate(lines)
                     for x, c in enumerate(row) if c == "#")

positions = set(init_positions)
proposals = [
    lambda elf:(elf-1j, elf-1-1j, elf+1-1j),  # N
    lambda elf:(elf+1j, elf-1+1j, elf+1+1j),  # S
    lambda elf:(elf-1, elf-1-1j, elf-1+1j),  # W
    lambda elf:(elf+1, elf+1-1j, elf+1+1j)   # E
]

r = 0
num_moved = -1
while num_moved:
    if r == 10:
        min_x = min(int(z.real) for z in positions)
        max_x = max(int(z.real) for z in positions)
        min_y = min(int(z.imag) for z in positions)
        max_y = max(int(z.imag) for z in positions)
        p_1 = (max_x - min_x + 1) * (max_y - min_y + 1) - len(positions)
        print("Part 1:", p_1)
    num_moved = 0
    new_positions = defaultdict(list)
    for elf in positions:
        if not {elf+1, elf+1+1j, elf+1j, elf-1+1j, \
                elf-1, elf-1-1j, elf-1j, elf+1-1j} & positions:  # All empty
            new_positions[elf].append(elf)
            continue
        for prop in proposals:
            if not set(prop(elf)) & positions:
                new_positions[prop(elf)[0]].append(elf)
                break
        else:
            new_positions[elf].append(elf)
    old_positions = positions
    positions = {(pro if len(elves) == 1 else elf)
                 for pro, elves in new_positions.items() for elf in elves}
    num_moved = len(old_positions-positions)
    assert len(positions) == len(init_positions)  # Did we lose any elves?
    r += 1
    proposals.append(proposals.pop(0))

print("Part 2:", r)
