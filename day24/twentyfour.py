from collections import defaultdict
from dataclasses import dataclass
from enum import Enum


def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

class Tile(Enum):
    OPEN = 0
    WALL = 1

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def moves(self):
        yield self
        if self.y != HEIGHT - 1:
            yield Point(self.y + 1, self.x)
        if self.x != WIDTH - 1:
            yield Point(self.y, self.x + 1)
        if self.y != 0:
            yield Point(self.y - 1, self.x)
        if self.x != 0:
            yield Point(self.y, self.x - 1)

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)

tiles = []
blizzards = {}

for y, line in enumerate(parse_input()):
    tiles.append([])
    for x, c in enumerate(line):
        if c == "#":
            tiles[-1].append(Tile.WALL)
        else:
            tiles[y].append(Tile.OPEN)
            p = Point(y, x)
            if c == "^":
                blizzards[p] = [Direction.NORTH]
            elif c == ">":
                blizzards[p] = [Direction.EAST]
            elif c == "v":
                blizzards[p] = [Direction.SOUTH]
            elif c == "<":
                blizzards[p] = [Direction.WEST]
            else:
                pass

HEIGHT = len(tiles)
WIDTH = len(tiles[0])

def step_blizzards(_blizzards):
    new_blizzards = defaultdict(list)
    for point in _blizzards:
        for d in _blizzards[point]:
            delta = {
                Direction.NORTH: Point(-1, 0),
                Direction.EAST: Point(0, 1),
                Direction.SOUTH: Point(1, 0),
                Direction.WEST: Point(0, -1),
            }[d]
            q = point + delta
            if tiles[q.y][q.x] == Tile.WALL:
                if d == Direction.NORTH:
                    q = Point(HEIGHT - 2, point.x)
                elif d == Direction.SOUTH:
                    q = Point(1, point.x)
                elif d == Direction.EAST:
                    q = Point(point.y, 1)
                elif d == Direction.WEST:
                    q = Point(point.y, WIDTH - 2)
            new_blizzards[q].append(d)
    return dict(new_blizzards)

def make_memo_table(_blizzards):
    _memo = [_blizzards, step_blizzards(_blizzards)]
    while _memo[-1] != _memo[0]:
        _memo.append(step_blizzards(_memo[-1]))
    return _memo[:-1]

memo = make_memo_table(blizzards)

def pathfind(_start, _dest, minute = 0):
    reached = {(minute % len(memo), _start.y, _start.x): minute}
    positions = [_start]

    while positions:
        minute += 1
        blizz_index = minute % len(memo)
        curr_blizz = memo[blizz_index]
        new_positions = []
        for pos in positions:
            for q in pos.moves():
                if tiles[q.y][q.x] == Tile.WALL:
                    continue
                if q in curr_blizz:
                    continue
                if q == _dest:
                    return minute

                key = (blizz_index, q.y, q.x)
                if key in reached:
                    continue
                reached[key] = minute
                new_positions.append(q)
        positions = new_positions
    return -1

start = Point(0, 1)
dest = Point(HEIGHT - 1, WIDTH - 2)

COUNT = pathfind(start, dest)
print(COUNT)
COUNT = pathfind(dest, start, COUNT)
COUNT = pathfind(start, dest, COUNT)
print(COUNT)
