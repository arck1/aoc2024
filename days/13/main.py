import re
import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class Point:
    x: int = 0
    y: int = 0


@dataclass(slots=True)
class Machine:
    a: Point = field(default_factory=lambda: Point(0, 0))
    b: Point = field(default_factory=lambda: Point(0, 0))
    end: Point = field(default_factory=lambda: Point(0, 0))


def read_input(file: Path):
    ms = []
    m = Machine()

    for line in file.read_text().splitlines():
        if not line:
            ms.append(m)
            m = Machine()
            continue

        match = re.search(r'Button (?P<btn>[AB]): X\+(?P<dx>\d+), Y\+(?P<dy>\d+)', line)

        if match and (d := match.groupdict()):
            if d['btn'] == 'A':
                m.a = Point(int(d['dx']), int(d['dy']))
            elif d['btn'] == 'B':
                m.b = Point(int(d['dx']), int(d['dy']))
            else:
                raise ValueError(f'Unknown button {d["btn"]}')
        else:
            match = re.search(r'Prize: X=(?P<x>\d+), Y=(?P<y>\d+)', line)

            if match and (d := match.groupdict()):
                m.end = Point(int(d['x']), int(d['y']))
            else:
                raise ValueError(f'Unknown line {line}')

    ms.append(m)
    return ms


def get_price(ax: int, bx: int, x: int, ay: int, by: int, y: int) -> int | None:
    solutions = []

    for k in range(x // ax + 1):
        for f in range(x // bx + 1):
            if k * ax + f * bx == x and k * ay + f * by == y:
                solutions.append((k, f))

    result = None

    for k, f in solutions:
        if result is None or result > k * 3 + f:
            result = k * 3 + f

    return result


def solve1(file: Path):
    ms = read_input(file)
    result = 0

    for m in ms:
        s = get_price(m.a.x, m.b.x, m.end.x, m.a.y, m.b.y, m.end.y)
        if s:
            result += s

    print(result)


def get_price2(m: Machine) -> int | None:
    # главный определитель системы
    d = m.a.x * m.b.y - m.a.y * m.b.x

    if d == 0:
        return None

    # вспомогательные определители / главный определитель
    k = (m.end.x * m.b.y - m.end.y * m.b.x) // d
    f = (m.a.x * m.end.y - m.a.y * m.end.x) // d

    if (m.a.x * k + m.b.x * f) == m.end.x and (m.a.y * k + m.b.y * f) == m.end.y:
        # проверка на то, что решение целочисленное подходит
        return 3 * k + f
    return None


def solve2(file: Path):
    ms = read_input(file)
    result = 0

    for m in ms:
        m.end.x += 10000000000000
        m.end.y += 10000000000000
        s = get_price2(m)
        if s:
            result += s

    print(result)


if __name__ == '__main__':
    start = time.monotonic()
    solve1(Path('test.txt'))
    solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
