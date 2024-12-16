import time
from collections import defaultdict, deque
from pathlib import Path


def read_input(file: Path):
    m = []

    for line in file.read_text().splitlines():
        m.append(list(line.strip()))

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


def _get_delta_point(d: int) -> tuple[int, int]:
    match d:
        case 0:
            return -1, 0
        case 1:
            return 0, 1
        case 2:
            return 1, 0
        case 3:
            return 0, -1
        case _:
            raise ValueError(d)


def _rotate_cost(d, new_d) -> int:
    if abs(d - new_d) < 3:
        return abs(d - new_d) * 1000
    return 1000


Point = tuple[int, int]


def _get_costs(m: list[list[str]]) -> dict[Point, dict[int, int]]:
    s, e = _get_positions(m)
    costs: dict[Point, dict[int, int]] = defaultdict(lambda: defaultdict(int))

    q = deque()

    q.append(s)
    costs[s] = {
        1: 0,
        2: 1000,
        3: 2000,
        0: 1000,
    }

    while len(q) > 0:
        x, y = q.popleft()

        for i in range(4):
            dd = i % 4
            dx, dy = _get_delta_point(dd)

            a, b = x + dx, y + dy

            rotate_cost = _rotate_cost(i, dd)

            if m[a][b] == '.' or m[a][b] == 'E':
                for j in range(4):
                    dn = (dd + j) % 4
                    post_rotate_cost = _rotate_cost(dd, dn)

                    if (
                        dn not in costs[(a, b)]
                        or costs[(a, b)][dn] > costs[(x, y)][dd] + 1 + rotate_cost + post_rotate_cost
                    ):
                        costs[(a, b)][dn] = costs[(x, y)][dd] + 1 + rotate_cost + post_rotate_cost
                        q.append((a, b))

    return costs


def solve1(file: Path):
    m = read_input(file)

    s, e = _get_positions(m)
    costs: dict[Point, dict[int, int]] = _get_costs(m)
    result = min(costs[e].values())
    print(result)


def solve2(file: Path):
    m = read_input(file)
    s, e = _get_positions(m)
    costs: dict[Point, dict[int, int]] = _get_costs(m)

    points = set()

    q = deque()
    min_cost = min(costs[e].values())

    q.appendleft((e, min_cost))

    while len(q) > 0:
        (x, y), cost = q.pop()

        if (x, y) in points:
            continue

        m[x][y] = 'O'
        points.add((x, y))

        for i in range(4):
            dx, dy = _get_delta_point(i)
            a, b = x - dx, y - dy

            if m[a][b] not in ('.', 'S'):
                continue

            for j in range(4):
                rotate_cost = _rotate_cost(i, j)

                if costs[(a, b)][i] + rotate_cost + 1 == cost:
                    q.appendleft(((a, b), cost - rotate_cost - 1))

    print(len(points))


if __name__ == '__main__':
    start = time.monotonic()
    solve1(Path('test.txt'))
    solve1(Path('test1.txt'))
    solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    solve2(Path('test.txt'))
    solve2(Path('test1.txt'))
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
