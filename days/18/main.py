import copy
import time
from collections import defaultdict, deque
from pathlib import Path

from tqdm import tqdm


def read_input(file: Path):
    m = []

    for line in file.read_text().splitlines():
        x, y = map(int, line.strip().split(','))

        m.append((x, y))

    return m


def solve1(file: Path, w: int = 70, h: int = 70):
    b = read_input(file)
    w += 1
    h += 1

    m = [[0] * w for _ in range(h)]

    for x, y in b[:1024]:
        m[y][x] = -1

    q = deque([(0, 0)])
    e = h - 1, w - 1

    while len(q) > 0:
        x, y = q.pop()

        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nx, ny = x + dx, y + dy

            if (nx, ny) == (0, 0):
                continue

            if 0 <= nx < h and 0 <= ny < w and (m[nx][ny] == 0 or m[nx][ny] > m[x][y] + 1):
                m[nx][ny] = m[x][y] + 1
                q.appendleft((nx, ny))

    print(m[h - 1][w - 1])


def bfs(mp: list[list[int]], w: int, h: int) -> dict[tuple[int, int], int]:
    q = deque([(0, 0)])

    costs = defaultdict(int)

    while len(q) > 0:
        x, y = q.pop()

        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nx, ny = x + dx, y + dy

            if (nx, ny) == (0, 0):
                continue

            if (
                0 <= nx < h
                and 0 <= ny < w
                and mp[x][y] >= 0
                and (costs[(nx, ny)] == 0 or costs[(nx, ny)] > costs[(x, y)] + 1)
            ):
                costs[(nx, ny)] = costs[(x, y)] + 1
                q.appendleft((nx, ny))
    return costs


def get_path(costs: dict[tuple[int, int], int], w: int, h: int) -> set[tuple[int, int]]:
    points = set()

    q = deque([(h - 1, w - 1)])
    points.add((h - 1, w - 1))

    while len(q) > 0:
        x, y = q.pop()

        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nx, ny = x + dx, y + dy

            if 0 <= nx < h and 0 <= ny < w and costs[(nx, ny)] == costs[(x, y)] - 1:
                q.appendleft((nx, ny))
                points.add((nx, ny))

    return points


def solve2(file: Path, w: int = 70, h: int = 70, first_n: int = 1024):
    b = read_input(file)

    w += 1
    h += 1

    m = [[0] * w for _ in range(h)]

    for x, y in b[:first_n]:
        m[y][x] = -1

    paths = bfs(m, w, h)

    for x, y in tqdm(b[first_n:]):
        m[y][x] = -2

        if (y, x) in paths:
            paths = bfs(m, w, h)
            if paths[(h - 1, w - 1)] == 0:
                print(x, y)
                return


if __name__ == '__main__':
    start = time.monotonic()
    # solve1(Path('test.txt'), w=6, h=6)
    # solve1(Path('test1.txt'))
    # solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    # solve2(Path('test.txt'), w=6, h=6, first_n=12)
    # solve2(Path('test1.txt'))
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
