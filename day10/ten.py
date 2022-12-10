def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

def execute_cmds():
    x = 1
    cycle_count = 0
    for line in lines:
        if line == "noop":
            cycle_count += 1
            yield x, cycle_count
        elif line.startswith("addx"):
            delta = int(line[5:])
            cycle_count += 1
            yield x, cycle_count
            cycle_count += 1
            yield x, cycle_count
            x += delta

POINTS = {20, 60, 100, 140, 180, 220}

def part_1() -> int:
    result = 0
    for x, cycle_count in execute_cmds():
        if cycle_count in POINTS:
            result += x * cycle_count
    return result


def execute_cmds_with_crt() -> list[list[int]]:
    crt = [[0] * 40 for _ in range(6)]

    def update_crt():
        i = cycle_count - 1
        y, x = divmod(i, 40)
        if x in (x_register, x_register + 1, x_register -1):
            crt[y][x] = 1

    x_register = 1
    cycle_count = 0
    for line in lines:
        if line == "noop":
            cycle_count += 1
            update_crt()
        elif line.startswith("addx"):
            delta = int(line[5:])
            cycle_count += 1
            update_crt()
            cycle_count += 1
            update_crt()
            x_register += delta

    return crt

def draw_image(crt):
    for row in crt:
        print("".join("#" if val else "." for val in row))

if __name__ == "__main__":
    lines = parse_input()
    print(part_1())
    draw_image(execute_cmds_with_crt())
