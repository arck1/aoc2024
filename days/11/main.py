import time
from collections.abc import Iterable
from pathlib import Path


def read_input(file: Path):
    return list(map(int, file.read_text().split()))


mem: dict[int, int] = {}


def _process_stones(stones: Iterable[int]):
    for stone in stones:
        if stone == 0:
            yield 1
        elif (s := str(stone)) and len(s) % 2 == 0:
            yield int(s[: len(s) // 2])
            yield int(s[len(s) // 2 :])
        else:
            yield stone * 2024


def solve1(file: Path):
    m = read_input(file)

    for i in range(25):
        m = list(_process_stones(m))
        print(i, m)

    print(len(m))


def solve2(file: Path):
    m = read_input(file)

    for i in range(75):
        m = _process_stones(m)
        print(i)

    count = 0

    for _ in m:
        count += 1

        if count % 1000 == 0:
            print(count)
    print(count)


if __name__ == '__main__':
    start = time.monotonic()
    # solve1(Path('test.txt'))
    # solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    # solve2(Path('test.txt'))
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
