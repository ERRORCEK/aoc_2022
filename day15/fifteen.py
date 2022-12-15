import re

from dataclasses import dataclass
from itertools import chain
from operator import attrgetter


def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def distance(self, other) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass(frozen=True)
class Sensor:
    pos: Point
    beacon_pos: Point

    def in_range(self, _p) -> bool:
        return self.pos.distance(_p) <= self.pos.distance(self.beacon_pos)


sensors = []
beacons = set()

for line in parse_input():
    nums = [int(x) for x in re.findall(r"[-\d]+", line)]
    beacon = Point(nums[2], nums[3])
    beacons.add(beacon)
    sensors.append(Sensor(
        pos=Point(nums[0], nums[1]),
        beacon_pos=beacon
    ))

Y = 2000000

x_low = min(chain((s.pos.x for s in sensors), (s.beacon_pos.x for s in sensors))) * 2
x_high = max(chain((s.pos.x for s in sensors), (s.beacon_pos.x for s in sensors))) * 2


def part_1() -> int:
    count = 0
    for x in range(x_low, x_high + 1):
        _p = Point(x, Y)
        if _p in beacons:
            continue
        if any(s.in_range(_p) for s in sensors):
            count += 1

    return count


@dataclass(frozen=True)
class Range:
    low: int
    high: int


def analyze_column(x) -> Point:
    ranges = []
    for sensor in sensors:
        x_delta = abs(sensor.pos.x - x)
        distance = sensor.pos.distance(sensor.beacon_pos)
        y_pos = sensor.pos.y
        y_delta = distance - x_delta

        y_low = y_pos - y_delta
        y_high = y_pos + y_delta
        if y_low <= y_high:
            ranges.append(Range(y_low, y_high))

    ranges.sort(key=attrgetter("lo"))

    for i in range(len(ranges) - 1):
        r_1 = ranges[i]
        r_2 = ranges[i + 1]
        maybe_gap = r_1.high < r_2.low - 1
        if maybe_gap:
            gap_y = r_1.high + 1
            if all(gap_y < r.low or gap_y > r.high for r in ranges):
                return Point(x, gap_y)
    return None


def tuning_frequency(_p) -> int:
    return _p.x * 4000000 + _p.y

def part_2() -> int:
    for x in range(4000001):
        _p = analyze_column(x)
        if _p:
            return tuning_frequency(_p)
    return 0


if __name__ == "__main__":
    print(part_1())
    print(part_2())
