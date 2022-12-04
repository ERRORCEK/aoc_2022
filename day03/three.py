from string import ascii_lowercase, ascii_uppercase

def parse_input(filename: str = "input") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()


def get_priority(char_):
    """Returns priority of a character"""
    if char_ in ascii_lowercase:
        return ord(char_) - ord('a') + 1
    if char_ in ascii_uppercase:
        return ord(char_) - ord('A') + 27
    assert False

def part_1(lines: list) -> int:
    result = 0
    for line in lines:
        line_length = len(line)
        c_1, c_2 = line[:line_length // 2], line[line_length // 2:]
        c_1 = set(c_1)
        c_2 = set(c_2)
        char_ = list(c_1 & c_2)[0]
        result += get_priority(char_)
    return result

def part_2(lines: list) -> int:
    result = 0
    i = 0
    while i < len(lines):
        c_1 = set(lines[i])
        c_2 = set(lines[i + 1])
        c_3 = set(lines[i + 2])
        ch_ = list(c_1 & c_2 & c_3)[0]
        result += get_priority(ch_)
        i += 3
    return result


if __name__ == '__main__':
    lines_input = parse_input()
    print(part_1(lines_input))
    print(part_2(lines_input))
