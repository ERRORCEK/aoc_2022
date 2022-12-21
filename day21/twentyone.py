from dataclasses import dataclass
from operator import add, floordiv, mul, sub
from types import FunctionType

def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

@dataclass(frozen=True)
class Op:
    left: str
    operator: FunctionType
    right: str


def parse_monkeys() -> dict[str, Op]:
    for line in parse_input():
        name, job = line.split(": ")
        if job.isdigit():
            monkeys[name] = int(job)
        else:
            left, operator, right = job.split(" ")
            operator = {
                "+": add,
                "-": sub,
                "*": mul,
                "/": floordiv,
            }[operator]
            monkeys[name] = Op(left, operator, right)
    return monkeys


def part_1() -> int:
    while not isinstance(monkeys["root"], int):
        for name, job in monkeys.items():
            if (isinstance(job, int) or
                not isinstance(monkeys[job.left], int) or
                not isinstance(monkeys[job.right], int)
                ):
                continue
            monkeys[name] = job.operator(monkeys[job.left], monkeys[job.right])

    return monkeys["root"]

def get_desired_value_right(x, operator, z):
    if operator is add:
        return z - x
    if operator is sub:
        return x - z
    if operator is mul:
        return z // x
    if operator is floordiv:
        return x // z
    assert False

def get_desired_value_left(operator, y, z):
    if operator is add:
        return z - y
    if operator is sub:
        return y + z
    if operator is mul:
        return z // y
    if operator is floordiv:
        return y * z
    assert False

def part_2():
    while True:
        evaluated = False
        to_delete = set()

        for name, job in monkeys.items():
            if (isinstance(job, int) or
                not isinstance(monkeys[job.left], int) or
                not isinstance(monkeys[job.right], int)
                ):
                continue
            if job.left == "humn" or job.right == "humn":
                continue

            monkeys[name] = job.operator(monkeys[job.left], monkeys[job.right])
            to_delete.add(job.left)
            to_delete.add(job.right)
            evaluated = True

        for key in to_delete:
            del monkeys[key]

        if not evaluated:
            break

    desired_vals = []
    root = monkeys["root"]
    if isinstance(monkeys[root.left], int):
        desired_vals.append((root.right, monkeys[root.left]))
    else:
        desired_vals.append((root.left, monkeys[root.right]))

    monkeys["humn"] = Op("plac", print, "hold")

    while True:
        name, val = desired_vals[-1]
        if name == "humn":
            print(val)
            break
        job = monkeys[name]
        if isinstance(monkeys[job.left], int):
            target_name = job.right
            target_val = get_desired_value_right(monkeys[job.left], job.operator, val)
            desired_vals.append((target_name, target_val))
        else:
            target_name = job.left
            target_val = get_desired_value_left(job.operator, monkeys[job.right], val)
            desired_vals.append((target_name, target_val))


if __name__ == "__main__":
    monkeys = {}
    parse_monkeys()
    initial_monkeys = monkeys.copy()
    print(part_1())
    monkeys = initial_monkeys.copy()
    part_2()
