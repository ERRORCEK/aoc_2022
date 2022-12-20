def parse_input(filename: str = "input.txt") -> list:
    with open(filename, encoding="utf-8") as _:
        return _.read().splitlines()

def answer(a:list[int]) -> int:
    i_0 = a.index(0)
    return a[(i_0 + 1000) % N] + a[(i_0 + 2000) % N] + a[(i_0 + 3000) % N]

def mix(a:list[int], repeat = 1) -> list[int]:
    b = list(range(N))
    for _ in range(repeat):
        for k in range(N):
            i = b.index(k)
            x = a[i]
            j = (x + i) % (N - 1)

            del a[i]
            del b[i]
            a.insert(j, x)
            b.insert(j, k)
    return a

if __name__ == "__main__":
    data = [int(x) for x in parse_input()]
    N = len(data)
    print(answer(mix(data.copy())))
    print(answer(mix([x * 811589153 for x in data], repeat = 10)))
