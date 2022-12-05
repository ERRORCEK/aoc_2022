from dataclasses import dataclass


def parse_input(filename: str = "input") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()


@dataclass(frozen=True)
class SectionRange:
    # both inclusive
    lo: int
    hi: int

    def contains(self, other):
        return self.lo <= other.lo and self.hi >= other.hi

    def any_overlap(self, other):
        return (
            self.lo <= other.lo <= self.hi or
            self.lo <= other.hi <= self.hi or
            other.lo <= self.lo <= other.hi or
            other.lo <= self.hi <= other.hi
        )


def parse_section_range(s):
    lo, hi = s.split("-")
    return SectionRange(int(lo), int(hi))


pairs = []

for line in parse_input():
    elf1, elf2 = line.split(",")
    pairs.append((parse_section_range(elf1), parse_section_range(elf2)))

count = 0
for first, second in pairs:
    if first.contains(second):
        count += 1
    elif second.contains(first):
        count += 1

print(count)

count = 0
for first, second in pairs:
    if first.any_overlap(second):
        count += 1

print(count)
