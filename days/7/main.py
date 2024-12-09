from pathlib import Path
from pprint import pprint


def read_input(file: Path):
    data = []
    for line in file.read_text().splitlines():
        result, nums = line.split(':', maxsplit=1)

        data.append((int(result), list(map(int, nums.split()))))
    return data


def _calc(nums: list[int], pos: int, current: int, result: int) -> bool:
    if pos == len(nums):
        return current == result

    if current > result:
        return False

    return _calc(nums, pos + 1, current + nums[pos], result) or _calc(nums, pos + 1, current * nums[pos], result)


def solve1(file: Path):
    data = read_input(file)
    count = 0
    for total, nums in data:
        is_valid = _calc(nums, 0, 0, total)

        if is_valid:
            count += total
    pprint(count)


def _calc2(nums: list[int], pos: int, current: int, result: int) -> bool:
    if pos >= len(nums):
        return current == result

    if current > result:
        return False
    a = _calc2(nums, pos + 1, current + nums[pos], result)
    b = _calc2(nums, pos + 1, current * nums[pos] if current > 0 else nums[pos], result)
    c = _calc2(nums, pos + 1, int(str(current) + str(nums[pos])) if current > 0 else nums[pos], result)
    return a or b or c


def solve2(file: Path):
    data = read_input(file)
    count = 0
    for total, nums in data:
        is_valid = _calc2(nums, 0, 0, total)

        if is_valid:
            count += total
    pprint(count)


if __name__ == '__main__':
    # solve1(Path('test.txt'))
    # solve1(Path('input.txt'))

    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
