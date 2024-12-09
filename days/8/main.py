import itertools
from collections import defaultdict
from pathlib import Path


def read_input(file: Path):
    m = []
    a = defaultdict(list)

    for i, line in enumerate(file.read_text().splitlines()):
        m.append(list(line))

        for j in range(len(line)):
            if line[j] != '.':
                a[line[j]].append((i, j))

    return m, a


def _get_points(x1: int, y1: int, x2: int, y2: int, m: list[list[str]]) -> list[tuple[int, int]]:
    dx = x2 - x1
    dy = y2 - y1

    x, y = x1 + 2 * dx, y1 + 2 * dy

    if 0 <= x < len(m) and 0 <= y < len(m[0]):
        yield x, y

    x, y = x1 - dx, y1 - dy

    if 0 <= x < len(m) and 0 <= y < len(m[0]):
        yield x, y


def solve1(file: Path):
    m, a = read_input(file)
    rez = {}

    for c, points in a.items():
        for (x1, y1), (x2, y2) in itertools.combinations(points, 2):
            for x, y in _get_points(x1, y1, x2, y2, m):
                rez[(x, y)] = c

    print(len(rez))


def _get_points2(x1: int, y1: int, x2: int, y2: int, m: list[list[str]]) -> list[tuple[int, int]]:
    dx = x2 - x1
    dy = y2 - y1

    yield x1, y1
    yield x2, y2
    x, y = x2 + dx, y2 + dy

    while 0 <= x < len(m) and 0 <= y < len(m[0]):
        yield x, y
        x, y = x + dx, y + dy

    x, y = x1 - dx, y1 - dy

    while 0 <= x < len(m) and 0 <= y < len(m[0]):
        yield x, y
        x, y = x - dx, y - dy


def solve2(file: Path):
    m, a = read_input(file)
    rez = {}

    for c, points in a.items():
        for (x1, y1), (x2, y2) in itertools.combinations(points, 2):
            for x, y in _get_points2(x1, y1, x2, y2, m):
                rez[(x, y)] = c

    print(len(rez))


if __name__ == '__main__':
    # solve1(Path('test.txt'))
    # solve1(Path('input.txt'))

    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
