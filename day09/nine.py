from dataclasses import dataclass
from itertools import product


def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def touching(self, other) -> bool:
        for x_delta, y_delta in product((-1, 0, 1), repeat=2):
            if self == Point(other.x + x_delta, other.y + y_delta):
                return True
        return False


def update_tail(head, tail):
    if head == Point(tail.x - 2, tail.y):
        tail = Point(tail.x - 1, tail.y)
    elif head == Point(tail.x + 2, tail.y):
        tail = Point(tail.x + 1, tail.y)
    elif head == Point(tail.x, tail.y - 2):
        tail = Point(tail.x, tail.y - 1)
    elif head == Point(tail.x, tail.y + 2):
        tail = Point(tail.x, tail.y + 1)
    elif not head.touching(tail):
        x_delta = 1 if head.x > tail.x else -1
        y_delta = 1 if head.y > tail.y else -1
        tail = Point(tail.x + x_delta, tail.y + y_delta)
    return tail


DIRECTIONS = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0)
}


def part_1() -> int:
    head = Point(0, 0)
    tail = Point(0, 0)

    visited = set()
    visited.add(tail)

    for command in lines:
        direction, count = command.split(" ")
        count = int(count)
        delta = DIRECTIONS[direction]
        for _ in range(count):
            head = Point(head.x + delta[0], head.y + delta[1])
            tail = update_tail(head, tail)
            visited.add(tail)

    return len(visited)


def part_2() -> int:
    knots = [Point(0, 0)] * 10

    visited = set()
    visited.add(Point(0, 0))

    for command in lines:
        direction, count = command.split(" ")
        count = int(count)
        delta = DIRECTIONS[direction]
        for _ in range(count):
            knots[0] = Point(knots[0].x + delta[0], knots[0].y + delta[1])
            for i in range(1, 10):
                head = knots[i - 1]
                tail = knots[i]
                tail = update_tail(head, tail)
                knots[i] = tail
            visited.add(knots[-1])

    return len(visited)


if __name__ == "__main__":
    lines = parse_input()
    print(part_1())
    print(part_2())
