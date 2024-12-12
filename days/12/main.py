import time
from pathlib import Path


def read_input(file: Path):
    m = []
    for line in file.read_text().splitlines():
        m.append([int(c) for c in line])

    return m


def solve1(file: Path):
    m = read_input(file)



def solve2(file: Path):
    m = read_input(file)



if __name__ == '__main__':
    start = time.monotonic()
    solve1(Path('test.txt'))
    solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
