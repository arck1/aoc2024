import time
from collections.abc import Iterator
from pathlib import Path
from pprint import pprint


def read_input(file: Path):
    m = []
    moves = []

    is_map = True

    for line in file.read_text().splitlines():
        if not line:
            is_map = False
            continue

        if is_map:
            m.append(list(line.strip()))
        else:
            moves.extend(list(line.strip()))

    return m, moves


def _get_position(m: list[list[str]]) -> tuple[int, int]:
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == '@':
                return i, j

    raise ValueError('start not found')


def _get_gps_sum(m: list[list[str]], ch: str = 'O') -> int:
    result = 0

    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == ch:
                result += 100 * i + j

    return result


def _get_dir(c: str) -> tuple[int, int]:
    match c:
        case '^':
            return -1, 0
        case '>':
            return 0, 1
        case 'v':
            return 1, 0
        case '<':
            return 0, -1
        case _:
            raise ValueError('invalid direction')


def solve1(file: Path):
    m, ds = read_input(file)

    x, y = _get_position(m)

    for d in ds:
        dx, dy = _get_dir(d)

        a, b = x + dx, y + dy

        boxes = 0
        has_free = False

        while True:
            match m[a][b]:
                case 'O':
                    boxes += 1
                case '#':
                    break
                case '.':
                    has_free = True
                    break
            a, b = a + dx, b + dy

        if has_free:
            if boxes > 0:
                m[a][b], m[x + dx][y + dy] = m[x + dx][y + dy], m[a][b]

            m[x][y], m[x + dx][y + dy] = m[x + dx][y + dy], m[x][y]
            x, y = x + dx, y + dy

    pprint(m)
    print(_get_gps_sum(m))


def _modify_line(l: list[str]) -> Iterator[str]:
    for c in l:
        match c:
            case '#':
                yield '#'
                yield '#'
            case 'O':
                yield '['
                yield ']'
            case '.':
                yield '.'
                yield '.'
            case '@':
                yield '@'
                yield '.'


def _can_move(m: list[list[str]], x: int, y: int, dx: int, dy: int) -> bool:
    a, b = x + dx, y + dy
    result = False

    if m[a][b] == '#':
        result = False
    elif m[a][b] == '.':
        result = True
    elif dx == 0:
        result = _can_move(m, a, b, dx, dy)
    elif m[a][b] == '[':
        result = _can_move(m, a, b, dx, dy) and _can_move(m, a, b + 1, dx, dy)
    elif m[a][b] == ']':
        result = _can_move(m, a, b, dx, dy) and _can_move(m, a, b - 1, dx, dy)

    return result


def _move(m: list[list[str]], x: int, y: int, dx: int, dy: int) -> tuple[int, int]:
    a, b = x + dx, y + dy

    if m[a][b] == '.':
        pass
    elif dx == 0:
        _move(m, a, b, dx, dy)
    elif m[a][b] == '[':
        _move(m, a, b, dx, dy)
        _move(m, a, b + 1, dx, dy)
    elif m[a][b] == ']':
        _move(m, a, b, dx, dy)
        _move(m, a, b - 1, dx, dy)

    m[a][b], m[x][y] = m[x][y], m[a][b]

    return a, b


def solve2(file: Path):
    m, ds = read_input(file)

    m = [list(_modify_line(l)) for l in m]

    x, y = _get_position(m)

    for d in ds:
        dx, dy = _get_dir(d)

        can_move = _can_move(m, x, y, dx, dy)

        if can_move:
            x, y = _move(m, x, y, dx, dy)

    # pprint(m)
    print(_get_gps_sum(m, ch='['))


if __name__ == '__main__':
    start = time.monotonic()
    solve1(Path('test.txt'))
    solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
