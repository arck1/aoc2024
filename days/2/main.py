from collections.abc import Iterator
from pathlib import Path


def read_input(file: Path) -> Iterator[list[int]]:
    for line in file.read_text().splitlines():
        values = list(map(int, line.split()))
        yield values


def is_safe_pair(a: int, b: int, dir: bool) -> bool:
    d = abs(a - b)

    if d < 1 or d > 3:
        return False

    if dir and a > b:
        return False
    if not dir and a < b:
        return False

    return True


def is_safe(values: list[int], direction: bool | None = None, ignore: int | None = None) -> bool:
    direction = values[0] < values[1] if direction is None else direction

    for i in range(len(values) - 1):
        if i == ignore:
            continue

        next = values[i + 1]
        if i + 1 == ignore:
            if i + 2 >= len(values):
                break

            next = values[i + 2]

        if not is_safe_pair(values[i], next, direction):
            return False

    return True


def solve1(file: Path):
    result = 0

    for values in read_input(file):
        result += 1 if is_safe(values) else 0

    print(file.as_posix(), result)


def is_safe2(values: list[int]) -> bool:
    result = False
    for ignore in range(len(values)):
        if is_safe(values, direction=True, ignore=ignore) or is_safe(values, direction=False, ignore=ignore):
            return True

    return result


def solve2(file: Path):
    result = 0

    for values in read_input(file):
        result += 1 if is_safe2(values) else 0

    print(file.as_posix(), result)


if __name__ == '__main__':
    solve1(Path('test.txt'))
    # solve1(Path('input.txt'))

    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
