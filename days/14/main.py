import operator
import re
import time
from dataclasses import dataclass
from functools import reduce
from pathlib import Path
from pprint import pprint


@dataclass(slots=True, kw_only=True)
class Robot:
    x: int
    y: int
    vx: int
    vy: int

def read_input(file: Path):
    m = []
    for line in file.read_text().splitlines():
        match = re.search(r'p=(?P<y>\d+),(?P<x>\d+) v=(?P<vy>[\d\-]+),(?P<vx>[\d\-]+)', line)

        if not match:
            raise ValueError(f'Invalid line: {line}')

        d = match.groupdict()

        m.append(
            Robot(
                x=int(d['x']),
                y=int(d['y']),
                vx=int(d['vx']),
                vy=int(d['vy']),
            )
        )

    return m


def _move_robot(r: Robot, *, count: int = 100, h: int, w: int) -> Robot:
    r.x = (r.x + r.vx * count) % h
    r.y = (r.y + r.vy * count) % w
    return r


def _show_robots(robots: list[Robot], *, w: int, h: int) -> None:
    m = [
        [0 for _ in range(w)]
        for _ in range(h)
    ]

    for r in robots:
        m[r.x][r.y] += 1

    for i in range(h):
        for j in range(w):
            if m[i][j] == 0:
                m[i][j] = '.'
            else:
                m[i][j] = str(m[i][j])
    pprint(m)



def solve1(file: Path, w: int = 101, h: int = 103):
    m = read_input(file)

    # pprint(m)

    qdrants = [0, 0, 0, 0]

    wd = w // 2
    hd = h // 2

    for r in m:
        r = _move_robot(r, count=100, h=h, w=w)

        if r.x < hd:
            if r.y < wd:
                qdrants[0] += 1
            elif r.y > wd:
                qdrants[1] += 1
        elif r.x > hd:
            if r.y < wd:
                qdrants[2] += 1
            elif r.y > wd:
                qdrants[3] += 1

    # _show_robots(m, w=w, h=h)
    result = reduce(operator.mul, qdrants, 1)
    print(qdrants, result)


def _calc_image(robots: list[Robot], threshold: int = 20) -> int:
    avg_x = sum(r.x for r in robots) / len(robots)
    avg_y = sum(r.y for r in robots) / len(robots)

    count = 0

    for r in robots:
        if abs(avg_x - r.x) < threshold and abs(avg_y - r.y) < threshold:
            count += 1

    return count

def solve2(file: Path, w: int = 101, h: int = 103):
    m = read_input(file)

    timer = 0

    while True:
        timer += 1
        for r in m:
            _move_robot(r, count=1, h=h, w=w)

        if (c := _calc_image(m)) > 250:
            print(c, timer)

        if timer > 10000:
            break

if __name__ == '__main__':
    start = time.monotonic()
    solve1(Path('test.txt'), h=7, w=11)
    solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
