import time
from collections import defaultdict, deque
from pathlib import Path
from pprint import pprint

from tqdm import tqdm


def read_input(file: Path):
    m = []

    for line in file.read_text().splitlines():
        m.append(list(line))
    return m


def _get_positions(m: list[list[str]]) -> tuple[tuple[int, int], tuple[int, int]]:
    start = None
    end = None
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == 'S':
                start = (i, j)
            if m[i][j] == 'E':
                end = (i, j)

            if start and end:
                break

    return start, end


def _bfs(m: list[list[str]], s: tuple[int, int], e: tuple[int, int]) -> dict[tuple[int, int], int]:
    q = deque()

    q.append(s)
    v = defaultdict(int)

    while len(q) > 0:
        x, y = q.popleft()

        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nx, ny = x + dx, y + dy

            if m[nx][ny] not in ('E', '.'):
                continue

            if 0 <= nx < len(m) and 0 <= ny < len(m[nx]) and (v[(nx, ny)] == 0 or v[(nx, ny)] > v[(x, y)] + 1):
                v[(nx, ny)] = v[(x, y)] + 1
                q.append((nx, ny))
                # m[nx][ny] = '0'

    return v


def _get_path(s: tuple[int, int], e: tuple[int, int], v: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    q = deque()

    q.append(e)
    points = [e]

    while len(q) > 0:
        x, y = q.popleft()

        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nx, ny = x + dx, y + dy

            if v.get((nx, ny), -1000) + 1 == v[(x, y)]:
                points.append((nx, ny))
                q.append((nx, ny))

    points.reverse()
    return points


def solve1(file: Path, min_diff: int = 100):
    m = read_input(file)

    s, e = _get_positions(m)
    print(s, e)
    v = _bfs(m, s, e)

    path = _get_path(s, e, v)
    # pprint(path)
    count = 0
    saves = defaultdict(int)
    for x, y in path:
        a = v[(x, y)]
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            nx, ny = x + dx, y + dy
            nx2, ny2 = x + 2 * dx, y + 2 * dy

            if m[nx][ny] != '#':
                continue

            b = v.get((nx2, ny2), -1000)
            d = b - a - 2
            if b > 0 and d >= min_diff:
                count += 1
                saves[d] += 1

    print(count)
    pprint(saves)


def _dist(a, b) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve2(file: Path, min_diff: int = 100):
    m = read_input(file)
    s, e = _get_positions(m)
    print(s, e)
    v = _bfs(m, s, e)

    path = _get_path(s, e, v)
    # pprint(path)
    count = 0
    saves = defaultdict(int)
    for x, y in tqdm(path):
        a = v[(x, y)]

        q = deque([(x, y)])

        tp = set()

        while len(q) > 0:
            fx, fy = q.popleft()

            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                nx, ny = fx + dx, fy + dy
                dst = _dist((x, y), (nx, ny))
                if 0 <= nx < len(m) and 0 <= ny < len(m[nx]) and dst <= 20 and (nx, ny) not in tp:
                    q.append((nx, ny))
                    tp.add((nx, ny))

        for tx, ty in tp:
            if m[tx][ty] == '#':
                continue

            b = v.get((tx, ty), -1000)
            if b < 0:
                continue
            dst = _dist((x, y), (tx, ty))
            d = b - a - dst
            if b > 0 and d >= min_diff:
                count += 1
                saves[d] += 1

    print(count)
    # pprint(saves)


if __name__ == '__main__':
    start = time.monotonic()
    solve1(Path('test.txt'), min_diff=1)
    solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    solve2(Path('test.txt'), min_diff=50)
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
