import time
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

from tqdm import tqdm


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

def _process_stones2(stones: dict[int, int]):
    for stone, v in stones.items():
        if stone == 0:
            yield 1, v
        elif (s := str(stone)) and len(s) % 2 == 0:
            yield int(s[: len(s) // 2]), v
            yield int(s[len(s) // 2 :]), v
        else:
            yield stone * 2024, v


def solve2(file: Path):
    m = read_input(file)

    stones = defaultdict(int)
    for s in m:
        stones[s] += 1

    for i in tqdm(range(75)):
        new_stones = defaultdict(int)

        for s, v in _process_stones2(stones):
            new_stones[s] += v

        stones = new_stones

    result = sum(stones.values())
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
