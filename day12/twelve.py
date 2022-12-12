from dataclasses import dataclass

def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

grid = parse_input()
rows = len(grid)
cols = len(grid[0])

@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def neighbours(self):
        if self.y != rows - 1:
            yield Point(self.y + 1, self.x)
        if self.y != 0:
            yield Point(self.y - 1, self.x)
        if self.x != cols - 1:
            yield Point(self.y, self.x + 1)
        if self.x != 0:
            yield Point(self.y, self.x - 1)

    def valid_neighbours(self):
        for neighbour in self.neighbours():
            self_value = grid[self.y][self.x]
            other_value = grid[neighbour.y][neighbour.x]
            if self_value >= other_value:
                yield neighbour
            elif chr(ord(self_value) + 1) == other_value:
                yield neighbour

for y in range(rows):
    for x in range(cols):
        if grid[y][x] == "S":
            grid[y] = grid[y][:x] + "a" + grid[y][x + 1:]
            start = Point(y, x)
        elif grid[y][x] == "E":
            grid[y] = grid[y][:x] + "z" + grid[y][x + 1:]
            end = Point(y, x)

def dijkstra(_start, _end):

    distance = {_start: 0}
    visited = set()
    to_visit = {_start}

    while to_visit:
        next_to_visit = set()

        for node in to_visit:
            for neighbour in node.valid_neighbours():
                if neighbour not in visited:
                    visited.add(neighbour)
                    next_to_visit.add(neighbour)
                    distance[neighbour] = distance[node] + 1
        to_visit = next_to_visit

    if _end in distance:
        return distance[_end]
    else:
        return 2**31 - 1

print(dijkstra(start, end))

def part_2():
    curr_min = 2**31 - 1
    for _y in range(rows):
        for _x in range(cols):
            if grid[_y][_x] != "a":
                continue

            p = Point(_y, _x)
            distance = dijkstra(p, end)
            if distance < curr_min:
                curr_min = distance
    print(curr_min)

part_2()
