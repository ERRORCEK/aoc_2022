from dataclasses import dataclass


def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def adjacent(self):
        x = self.x
        y = self.y
        z = self.z
        yield Point(x + 1, y, z)
        yield Point(x - 1, y, z)
        yield Point(x, y + 1, z)
        yield Point(x, y - 1, z)
        yield Point(x, y, z + 1)
        yield Point(x, y, z - 1)

    def small(self) -> bool:
        return abs(self.x) < 25 and abs(self.y) < 25 and abs(self.z) < 25


def parse_cubes(lines) -> set:
    _cubes = []
    for line in lines:
        x, y, z = line.split(',')
        x = int(x)
        y = int(y)
        z = int(z)
        _cubes.append(Point(x, y, z))
    return set(_cubes)


def part_1() -> int:
    count = 0
    for cube in cubes:
        for p in cube.adjacent():
            if p not in cubes:
                count += 1
    return count


def part_2() -> int:
    air = set((Point(0, 0, 0),))
    last_air = air.copy()
    for _ in range(100):
        new_air = set()
        for p in last_air:
            for q in p.adjacent():
                if q not in cubes and q not in air and q.small():
                    new_air.add(q)
        air |= new_air
        last_air = new_air

    count = 0
    for cube in cubes:
        for p in cube.adjacent():
            if p in air:
                count += 1
    return count


if __name__ == "__main__":
    cubes = parse_cubes(parse_input())
    print(part_1())
    print(part_2())
