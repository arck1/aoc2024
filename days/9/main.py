from collections import deque
from pathlib import Path
from typing import NamedTuple


class Block(NamedTuple):
    is_data: bool
    size: int
    values: deque


def read_input(file: Path):
    line = file.read_text().strip()

    is_data = True
    file_id = 0
    blocks = []

    for c in line:
        v = int(c)

        blocks.append(
            Block(
                is_data=is_data,
                size=v,
                values=deque([file_id for _ in range(v)]) if is_data else deque(),
            )
        )

        if is_data:
            file_id += 1
            is_data = False
        else:
            is_data = True

    return blocks


def _calc_hash(blocks: list[Block]) -> int:
    result = 0

    i = 0

    for block in blocks:
        for v in block.values:
            result += i * v
            i += 1

        if d := block.size - len(block.values):
            i += d


    return result


def solve1(file: Path):
    blocks = read_input(file)

    # pprint(blocks)
    left = 0
    right = len(blocks) - 1

    while left < right:
        if blocks[left].is_data:
            left += 1
            continue
        if not blocks[right].is_data:
            right -= 1
            continue

        free = blocks[left].size - len(blocks[left].values)

        if free < 1:
            left += 1
            continue

        while free > 0 and len(blocks[right].values) > 0:
            free -= 1
            blocks[left].values.append(blocks[right].values.pop())

        if free == 0:
            left += 1
        if len(blocks[right].values) < 1:
            right -= 1

    # pprint(blocks)

    result = _calc_hash(blocks)
    print(result)


def solve2(file: Path):
    blocks = read_input(file)

    # pprint(blocks)
    right = len(blocks) - 1

    while right > 0:
        if not blocks[right].is_data:
            right -= 1
            continue

        move_size = len(blocks[right].values)

        free_block = 0
        found = None

        while free_block < right:
            if blocks[free_block].is_data:
                free_block += 1
                continue

            free = blocks[free_block].size - len(blocks[free_block].values) - move_size

            if free >= 0:
                found = free_block
                break

            free_block += 1

        if not found:
            right -= 1
            continue

        blocks[found].values.extend(blocks[right].values)
        blocks[right].values.clear()

        right -= 1

    # pprint(blocks)

    result = _calc_hash(blocks)
    print(result)


if __name__ == '__main__':
    solve1(Path('test.txt'))
    solve1(Path('input.txt'))

    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
