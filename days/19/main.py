import queue
import time
from dataclasses import dataclass, field
from pathlib import Path
from pprint import pprint


def read_input(file: Path):
    lines = list(filter(bool, file.read_text().splitlines()))

    patterns = list(map(str.strip, lines[0].split(',')))

    designs = list(map(str.strip, lines[1:]))
    return patterns, designs


@dataclass(slots=True, kw_only=True)
class Node:
    v: str | None = None
    count: int = 0
    is_end: bool = False
    next: dict[str, 'Node'] = field(default_factory=dict)


def is_possible(s: str, i: int, root: Node) -> bool:
    if i >= len(s):
        return True

    node = root

    while i < len(s):
        next_node = node.next.get(s[i])

        if next_node is None:
            return False

        if next_node.is_end and is_possible(s, i + 1, root):
            return True

        i += 1
        node = next_node

    return False


def _build_bor(patterns: list[str]) -> Node:
    root = Node(next={})

    for p in patterns:
        node = root

        for c in p:
            next_node = node.next.get(c)

            if next_node is None:
                next_node = Node(v=c)
                node.next[c] = next_node

            node = next_node

        node.is_end = True
    return root


def count_variants(s: str, root: Node) -> int:
    q = queue.PriorityQueue(maxsize=0)
    q.put_nowait(0)

    dp: list[int] = [0 for _ in range(len(s) + 1)]
    dp[0] = 1

    viewed = set()

    while not q.empty():
        p = q.get_nowait()

        if p >= len(s) or p in viewed:
            continue
        viewed.add(p)
        node = root

        i = p
        while i < len(s):
            next_node = node.next.get(s[i])

            if next_node is None:
                break

            if next_node.is_end:
                dp[i + 1] += dp[p]
                q.put_nowait(i + 1)

            i += 1
            node = next_node

    return dp[len(s)]


def solve1(file: Path):
    patterns, designs = read_input(file)

    print(patterns, designs)

    root = _build_bor(patterns)

    # pprint(root)

    count = 0

    for d in designs:
        res = is_possible(d, 0, root)

        if res:
            count += 1

    print(count)


def solve2(file: Path):
    patterns, designs = read_input(file)

    print(patterns, designs)

    root = _build_bor(patterns)

    # pprint(root)

    count = 0

    for d in designs:
        res = count_variants(d, root)

        if res > 0:
            count += res

    print(count)


if __name__ == '__main__':
    start = time.monotonic()
    solve1(Path('test.txt'))
    solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
