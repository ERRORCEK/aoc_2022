def parse_input(filename: str = "input.txt")->list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

def decode(number):
    out = 0
    for digit in number:
        out *= 5
        match digit:
            case '2':
                out += 2
            case '1':
                out += 1
            case '-':
                out -= 1
            case '=':
                out -= 2
    return out

def encode(number):
    out = []
    while number:
        digit = number % 5
        match digit:
            case 0:
                out.append('0')
            case 1:
                out.append('1')
            case 2:
                out.append('2')
            case 3:
                out.append('=')
                number += 2
            case 4:
                out.append('-')
                number += 1
        number //= 5
    return ''.join(reversed(out))

def part_1():
    s = sum(map(decode, parse_input()))
    return encode(s)

if __name__ == "__main__":
    print(part_1())
