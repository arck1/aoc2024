from collections import defaultdict
from copy import deepcopy
from pathlib import Path

from tqdm import tqdm


def read_input(file: Path):
    return [list(line) for line in file.read_text().splitlines()]


NEXT_DIRS = {'^': '>', '>': 'v', 'v': '<', '<': '^'}


def _get_pos(m: list[list[str]]) -> tuple[int, int]:
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] in NEXT_DIRS:
                return i, j

    raise ValueError('No position')


def _next_point(direction: str, x: int, y: int) -> tuple[int, int]:
    match direction:
        case '^':
            return x - 1, y
        case '>':
            return x, y + 1
        case 'v':
            return x + 1, y
        case '<':
            return x, y - 1


def _next_direction(direction: str) -> str:
    return NEXT_DIRS[direction]


def solve1(file: Path):
    m = read_input(file)
    # pprint(m)
    count = 0

    x, y = _get_pos(m)

    path, _ = _get_path(m, x, y)

    print(len(path))


def _get_path(m, x, y, with_path=True) -> tuple[list[tuple[int, int]], bool]:
    path = []
    direction = m[x][y]
    m[x][y] = '.'

    is_cycled = False

    seen = defaultdict(set[str])

    while True:
        if m[x][y] == '.':
            m[x][y] = direction
            if with_path:
                path.append((x, y))
        elif m[x][y] == direction:
            is_cycled = True
            break

        new_x, new_y = _next_point(direction, x, y)

        if new_x < 0 or new_x >= len(m) or new_y < 0 or new_y >= len(m[new_x]):
            break

        if m[new_x][new_y] == '#':
            direction = _next_direction(direction)
            m[x][y] = direction

        new_x, new_y = _next_point(direction, x, y)

        if m[new_x][new_y] == '#':
            direction = _next_direction(direction)
            m[x][y] = direction

        if direction in seen[(x, y)]:
            is_cycled = True
            break

        seen[(x, y)].add(direction)

        x, y = _next_point(direction, x, y)

    return path, is_cycled


def solve2(file: Path):
    m = read_input(file)
    # pprint(m)
    count = 0

    start_x, start_y = _get_pos(m)

    origin = deepcopy(m)
    path, _ = _get_path(origin, start_x, start_y)

    for x, y in tqdm(path):
        if (x, y) == (start_x, start_y):
            continue
        _m = deepcopy(m)

        _m[x][y] = '#'
        _, is_cycled = _get_path(_m, start_x, start_y, with_path=False)

        if is_cycled:
            count += 1

    print(count)


if __name__ == '__main__':
    # solve1(Path('test.txt'))
    # solve1(Path('input.txt'))

    # solve2(Path('test.txt'))
    solve2(Path('input.txt'))
