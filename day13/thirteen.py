import json

def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().strip()

RIGHT = 1

def check_pair(a, b) -> int:
    if isinstance(a, int) and isinstance(b, int):
        return (a < b) - (b < a)

    if isinstance(a, int):
        a = [a]
    if isinstance(b, int):
        b = [b]

    for new_a, new_b in zip(a, b):
        result = check_pair(new_a, new_b)
        if result:
            return result

    return (len(a) < len(b)) - (len(b) < len(a))

def part_1() -> int:
    pairs = parse_input().split("\n\n")
    pairs = [[json.loads(y) for y in x.split("\n")] for x in pairs]

    score = 0
    for i, pair in enumerate(pairs):
        if check_pair(*pair) == RIGHT:
            score += i + 1

    return score

def part_2() -> int:
    items = [json.loads(y) for y in parse_input().split("\n") if y]
    items += [[[2]], [[6]]]

    def merge_sort(items):
        n = len(items)
        items_a, items_b = items[:n // 2], items[n // 2:]
        if n > 2:
            items_a = merge_sort(items_a)
            items_b = merge_sort(items_b)
        result = []
        while items_a and items_b:
            head_comp = check_pair(items_a[0], items_b[0])
            if head_comp == RIGHT:
                result.append(items_a[0])
                items_a = items_a[1:]
            else:
                result.append(items_b[0])
                items_b = items_b[1:]

        return result + items_a + items_b

    in_order = merge_sort(items)
    json_strings = [json.dumps(x) for x in in_order]
    return (json_strings.index("[[2]]") + 1) * (json_strings.index("[[6]]") + 1)

if __name__ == "__main__":
    print(part_1())
    print(part_2())
