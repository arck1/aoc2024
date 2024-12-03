from collections import defaultdict
from pathlib import Path


def solve1(file: Path):
    left = []
    right = []

    for line in file.read_text().splitlines():
        a, b = map(int, line.split())
        left.append(a)
        right.append(b)

    left.sort()
    right.sort()

    result = 0

    for i in range(len(left)):
        result += abs(left[i] - right[i])

    print(file.as_posix(), '=', result)


def solve2(file: Path):
    left = []
    right = defaultdict(int)

    for line in file.read_text().splitlines():
        a, b = map(int, line.split())
        left.append(a)
        right[b] += 1

    result = 0

    for x in left:
        result += x * right[x]

    print(file.as_posix(), '=', result)


if __name__ == '__main__':
    solve1(Path('test.txt'))
    solve1(Path('input.txt'))

    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
