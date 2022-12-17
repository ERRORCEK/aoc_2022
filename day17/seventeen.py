from itertools import cycle

ROCKS = [
        [[1, 1, 1, 1]],
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        [
            [0, 0, 1],
            [0, 0, 1],
            [1, 1, 1],
        ],
        [
            [1],
            [1],
            [1],
            [1],
        ],
        [
            [1, 1],
            [1, 1],
        ]
]

def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

class Rock:
    def __init__(self, shape):
        self.shape = shape
        self.x, self.y = 0, 0

    def place(self, highest_y):
        self.x = 2
        self.y = len(self.shape) + 3 + highest_y

    def cells(self):
        d_x = 0
        d_y = 0
        for line in self.shape:
            for cell in line:
                yield cell, self.x + d_x, self.y + d_y
                d_x += 1

            d_x = 0
            d_y -= 1

    def push(self, jet, room):
        delta = 1 if jet == ">" else -1
        for cell, x, y in self.cells():
            x += delta
            if cell == 1 and (x > 6 or x < 0 or room[y][x]):
                return
        self.x += delta

    def fall(self, room) -> bool:
        for cell, x, y in self.cells():
            y -= 1
            if cell == 1 and (y < 0 or room[y][x]):
                return True
        self.y -= 1
        return False

    def draw_on(self, room):
        for cell, x, y in self.cells():
            if cell == 1:
                room[y][x] = 1

def part_1():
    jet_i = 0
    rocks = cycle(ROCKS)
    room = [[0] * 7 for _ in range(10_000)]
    highest_y = -1

    def next_jet():
        nonlocal jet_i
        result = lines[0][jet_i]
        jet_i += 1
        jet_i %= len(lines[0])
        return result

    def fall():
        nonlocal highest_y
        rock = Rock(next(rocks))
        rock.place(highest_y)
        while True:
            rock.push(next_jet(), room)
            stopped = rock.fall(room)
            if stopped:
                break
        rock.draw_on(room)
        if rock.y > highest_y:
            highest_y = rock.y

    for _ in range(2022):
        fall()
    return highest_y + 1

def part_2():
    jet_i = 0
    rocks = cycle(ROCKS)
    room = [[0] * 7 for _ in range(1_000_000)]
    highest_y = -1

    def next_jet():
        nonlocal jet_i
        result = lines[0][jet_i]
        jet_i += 1
        jet_i %= len(lines[0])
        return result

    def fall():
        nonlocal highest_y
        rock = Rock(next(rocks))
        rock.place(highest_y)
        while True:
            rock.push(next_jet(), room)
            stopped = rock.fall(room)
            if stopped:
                break
        rock.draw_on(room)
        if rock.y > highest_y:
            highest_y = rock.y

    fingerprints = {}
    rocks_fell = 0
    while rocks_fell < 1_000_000_000_000:
        fall()
        rocks_fell += 1
        fp_jet_i = jet_i % len(lines[0])
        fp_rocks = rocks_fell % len(ROCKS)

        hitmap = [0] * 7
        i_y = highest_y
        while i_y > 0:
            row = room[i_y]
            for i, c in enumerate(row):
                hitmap[i] += c
            if all(c >= 1 for c in hitmap):
                break
            i_y -= 1

        if i_y == 0:
            continue

        fp_this = room[i_y:highest_y + 1]
        fp_key = (fp_jet_i, fp_rocks)
        if fp_key in fingerprints:
            fp_old, old_rocks_fell, old_highest_y = fingerprints[fp_key]
            if fp_old == fp_this and fp_key == (1411, 2):
                print(fp_key, fp_old)
                print(old_rocks_fell, old_highest_y)
                print(rocks_fell, highest_y)
                d_rocks = rocks_fell - old_rocks_fell
                d_highest = highest_y - old_highest_y
                print(d_rocks, d_highest)
                can_apply = (1_000_000_000_000 - rocks_fell) // d_rocks
                rocks_fell += can_apply * d_rocks
                delta_highest = can_apply * d_highest
                print(rocks_fell, d_highest)
        else:
            if rocks_fell > 1972:
                fingerprints[fp_key] = fp_this, rocks_fell, highest_y
    return delta_highest + highest_y + 1

if __name__ == '__main__':
    lines = parse_input()
    print(part_1())
    #print(part_2())        # index out of range
