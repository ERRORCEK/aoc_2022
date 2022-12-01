
def parse_input(input: str) -> list:
    with open(input) as f:
        data = f.read()
    # split the input by blank lines to get the lists of calories for each elf
    return data.strip().split("\n\n")

def part_1(input: str) -> int:
    # find the list item with maximum sum
    return max([sum([int(x) for x in group.split()]) for group in parse_input(input)])

def part_2(input: str) -> int:
    # calculate the sum of each elfs calories and sort them
    elfs_calories = [sum([int(x) for x in group.split()]) for group in parse_input(input)]
    elfs_calories.sort(reverse=True, key=int)
    # return sum of the 3 max calories elves
    return sum(elfs_calories[0:3])

    

if __name__ == '__main__':
    print(part_2("input"))