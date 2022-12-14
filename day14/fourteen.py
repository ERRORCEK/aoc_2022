from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from itertools import count, pairwise

def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

class Tile(Enum):
    AIR = 1
    SAND = 2
    ROCK = 3

@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def delta_to(self, other) -> "Point":
        if self.x < other.x:
            return Point(1, 0)
        if self.x > other.x:
            return Point(-1, 0)
        if self.y < other.y:
            return Point(0, 1)
        if self.y > other.y:
            return Point(0, -1)
        assert False

    def __add__(self, other) -> "Point":
        return Point(self.x + other.x, self.y + other.y)

tiles = defaultdict(lambda: Tile.AIR)

for line in parse_input():
    point_specs = line.split(" -> ")
    points = []
    for point_spec in point_specs:
        x, y = point_spec.split(",")
        x = int(x)
        y = int(y)
        points.append(Point(x, y))
    for start, end in pairwise(points):
        step = start.delta_to(end)
        pos = start
        while pos != end:
            tiles[pos] = Tile.ROCK
            pos += step
        tiles[pos] = Tile.ROCK

void = max(p.y for p in tiles.keys())

def blocked(_p):
    return tiles[_p] != Tile.AIR or _p.y == void + 2

def make_sand(part1 = True) -> bool:
    sand = Point(500, 0)
    while True:
        if part1 and sand.y > void:
            return False
        if not blocked(sand + Point(0, 1)):
            sand += Point(0, 1)
        elif not blocked(sand + Point(-1, 1)):
            sand += Point(-1, 1)
        elif not blocked(sand + Point(1, 1)):
            sand += Point(1, 1)
        else:
            tiles[sand] = Tile.SAND
            return sand != Point(500, 0)

def part_1() -> int:
    for a in count():
        if not make_sand():
            return a
    return 0

def part_2() -> int:
    for b in count():
        if not make_sand(part1=False):
            return b + 1
    return 0

if __name__ == "__main__":
    initial_state = tiles.copy()
    print(part_1())
    tiles = initial_state
    print(part_2())
