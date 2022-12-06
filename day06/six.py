from collections import Counter

def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

def solve(input_packet: str, s_length: int) -> int:
    for i in range(s_length, len(input_packet)):
        slider = Counter(input_packet[i-s_length:i])
        if max(slider.values()) == 1:
            return i

if __name__ == "__main__":
    packet = parse_input()[0]
    print(solve(packet, 4))
    print(solve(packet, 14))
