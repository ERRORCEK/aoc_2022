from itertools import chain

def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

grid = parse_input()
rows = len(grid)
cols = len(grid[0])
visibility = [[0] * cols for _ in range(rows)]

def tree(y, x) -> int:
    """Returns the value of the tree at the given coordinates."""
    return int(grid[y][x])

def visible(y, x) -> int:
    """Returns 1 if the tree at the given coordinates is visible, 0 otherwise."""
    at_value = tree(y, x)
    up_vis = all(tree(y_2, x) < at_value for y_2 in range(0, y))
    down_vis = all(tree(y_2, x) < at_value for y_2 in range(y + 1, rows))
    left_vis = all(tree(y, x_2) < at_value for x_2 in range(0, x))
    right_vis = all(tree(y, x_2) < at_value for x_2 in range(x + 1, cols))
    vis = up_vis or down_vis or left_vis or right_vis
    visibility[y][x] = vis
    return vis

def part_1() -> int:
    """Calculate how many trees are visible from outside of the grid."""
    for y in range(rows):
        for x in range(cols):
            visible(y,x)
    return sum(chain.from_iterable(visibility))

def scenic_score_1d(at_value: int, _it) -> int:
    """Calculate the score of a single direction."""
    score = 0
    for y, x in _it:
        score += 1
        val = tree(y, x)
        if val >= at_value:
            break
    return score

def scenic_score(y, x) -> int:
    """Calculate the score of a tree at the given coordinates."""
    at_value = tree(y, x)
    up_score = scenic_score_1d(at_value, ((y_2, x) for y_2 in reversed(range(0, y))))
    down_score = scenic_score_1d(at_value, ((y_2, x) for y_2 in range(y + 1, rows)))
    left_score = scenic_score_1d(at_value, ((y, x_2) for x_2 in reversed(range(0, x))))
    right_score = scenic_score_1d(at_value, ((y, x_2) for x_2 in range(x + 1, cols)))
    return up_score * down_score * left_score * right_score

def part_2() -> int:
    """Calculate the maximum scenic score achievable."""
    curr_max = 0
    for y in range(rows):
        for x in range(cols):
            score = scenic_score(y, x)
            if score > curr_max:
                curr_max = score
    return curr_max

if __name__ == "__main__":
    print(part_1())
    print(part_2())
