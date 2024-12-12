import time
from collections import deque
from pathlib import Path


def read_input(file: Path):
    m = []
    for line in file.read_text().splitlines():
        m.append([c for c in line])

    return m



def solve1(file: Path):
    m = read_input(file)

    result = 0

    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == '.':
                continue

            c = m[i][j]
            q = deque()
            q.appendleft((i, j))

            area = 0
            per = 0

            current = set()

            while len(q) > 0:
                (x, y) = q.pop()
                if (x, y) in current:
                    continue

                current.add((x, y))

                m[x][y] = '.'
                area += 1

                if x - 1 < 0:
                    per += 1
                elif m[x - 1][y] == c:
                    q.appendleft((x - 1, y))
                elif (x - 1, y) not in current:
                    per += 1

                if x + 1 >= len(m[i]):
                    per += 1
                elif m[x + 1][y] == c:
                    q.appendleft((x + 1, y))
                elif (x + 1, y) not in current:
                    per += 1

                if y - 1 < 0:
                    per += 1
                elif m[x][y - 1] == c:
                    q.appendleft((x, y - 1))
                elif (x, y - 1) not in current:
                    per += 1

                if y + 1 >= len(m[i]):
                    per += 1
                elif m[x][y + 1] == c:
                    q.appendleft((x, y + 1))
                elif (x, y + 1) not in current:
                    per += 1

            result += area * per

    print(result)


def solve2(file: Path):
    m = read_input(file)

    result = 0

    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == '.':
                continue

            c = m[i][j]
            q = deque()
            q.appendleft((i, j))

            area = 0
            per = 0

            current = set()
            borders = set()

            while len(q) > 0:
                (x, y) = q.pop()
                if (x, y) in current:
                    continue

                current.add((x, y))

                m[x][y] = '.'
                area += 1

                if x - 1 < 0:
                    per += 1
                    borders.add((x, y))
                elif m[x - 1][y] == c:
                    q.appendleft((x - 1, y))
                elif (x - 1, y) not in current:
                    per += 1
                    borders.add((x, y))

                if x + 1 >= len(m[i]):
                    per += 1
                    borders.add((x, y))
                elif m[x + 1][y] == c:
                    q.appendleft((x + 1, y))
                elif (x + 1, y) not in current:
                    per += 1
                    borders.add((x, y))

                if y - 1 < 0:
                    per += 1
                    borders.add((x, y))
                elif m[x][y - 1] == c:
                    q.appendleft((x, y - 1))
                elif (x, y - 1) not in current:
                    per += 1
                    borders.add((x, y))

                if y + 1 >= len(m[i]):
                    per += 1
                    borders.add((x, y))
                elif m[x][y + 1] == c:
                    q.appendleft((x, y + 1))
                elif (x, y + 1) not in current:
                    per += 1
                    borders.add((x, y))

            border = list(borders)
            border.sort()

            for x, y in border:
                if (x, y + 1) in borders:
                    if (x - 1, y) not in current and (x - 1, y + 1) not in current:
                        per -= 1
                    if (x + 1, y) not in current and (x + 1, y + 1) not in current:
                        per -= 1

                if (x + 1, y) in borders:
                    if (x, y + 1) not in current and (x + 1, y + 1) not in current:
                        per -= 1
                    if (x, y - 1) not in current and (x + 1, y - 1) not in current:
                        per -= 1

            result += area * per

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
