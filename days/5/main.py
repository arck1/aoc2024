from collections import defaultdict
from functools import cmp_to_key
from pathlib import Path


def read_input(file: Path):
    graph = defaultdict(set[int])
    pages = []

    is_second = False

    for line in file.read_text().splitlines():
        if line == '':
            is_second = True
            continue

        if is_second:
            pages.append(list(map(int, line.split(','))))
        else:
            x, y = map(int, line.split('|'))

            graph[x].add(y)

    return graph, pages


def is_pages_order_correct(g: dict[int, set], pages: list[int]) -> bool:
    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            if pages[i] in g[pages[j]]:
                return False
    return True


def solve1(file: Path):
    g, pages = read_input(file)

    result = 0
    for page in pages:
        if is_pages_order_correct(g, page):
            mid = len(page) // 2
            result += page[mid]

    print(result)


def solve2(file: Path):
    g, pages = read_input(file)

    def cmp(a, b) -> int:
        if a in g[b]:
            return -1
        if b in g[a]:
            return 1
        return 0

    result = 0
    for page in pages:
        if not is_pages_order_correct(g, page):
            page.sort(key=cmp_to_key(cmp))

            mid = len(page) // 2
            result += page[mid]

    print(result)


if __name__ == '__main__':
    solve1(Path('test.txt'))
    solve1(Path('input.txt'))

    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
