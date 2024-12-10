import time
from pathlib import Path


def read_input(file: Path):
    m = []
    for line in file.read_text().splitlines():
        m.append([int(c) for c in line])

    return m


def _dfs(m, x, y, value: int, total: int) -> set[tuple[int, int]]:
    if x < 0 or y < 0 or x >= len(m) or y >= len(m[x]) or m[x][y] != value:
        return set()

    if value == total:
        return {(x, y)}

    return (
        _dfs(m, x + 1, y, value + 1, total)
        | _dfs(m, x - 1, y, value + 1, total)
        | _dfs(m, x, y + 1, value + 1, total)
        | _dfs(m, x, y - 1, value + 1, total)
    )


def solve1(file: Path):
    m = read_input(file)

    total = 0

    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == 0:
                _points = _dfs(m, i, j, 0, 9)
                total += len(_points)

    print(total)


def _dfs2(m, x, y, value: int, total: int, path: list[tuple[int, int]]) -> set[tuple[tuple[int, int], ...]]:
    if x < 0 or y < 0 or x >= len(m) or y >= len(m[x]) or m[x][y] != value:
        return set()

    path.append((x, y))

    if value == total:
        return {tuple(path)}

    return (
        _dfs2(m, x + 1, y, value + 1, total, path)
        | _dfs2(m, x - 1, y, value + 1, total, path)
        | _dfs2(m, x, y + 1, value + 1, total, path)
        | _dfs2(m, x, y - 1, value + 1, total, path)
    )


def solve2(file: Path):
    m = read_input(file)

    total = 0

    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == 0:
                _points = _dfs2(m, i, j, 0, 9, [])
                total += len(_points)

    print(total)


if __name__ == '__main__':
    start = time.monotonic()
    solve1(Path('test.txt'))
    solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
