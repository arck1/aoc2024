import re
import time
from pathlib import Path


def read_input(file: Path):
    regs = {}
    lines = list(filter(bool, file.read_text().splitlines()))

    for line in lines[:3]:
        match = re.match(r'Register (?P<reg>[ABC]): (?P<val>\d+)', line.strip())

        if not match:
            raise ValueError(line)

        regs[match['reg']] = int(match['val'])

    program = lines[3].rsplit()[1]

    values = list(map(int, program.split(',')))

    return regs, values


def _get_combo(val: int, regs: dict[str, int]) -> int:
    if 0 <= val <= 3:
        return val
    match val:
        case 4:
            return regs['A']
        case 5:
            return regs['B']
        case 6:
            return regs['C']
        case _:
            raise ValueError(val)


def _perform(
    op_code: int, val: int, regs: dict[str, int], pointer: int, output: list[int], debug: bool = False
) -> tuple[int, dict[str, int]]:
    match op_code:
        case 0:  # adv
            if debug:
                print('adv', val, regs)
            regs['A'] = regs['A'] // (2 ** _get_combo(val, regs))
        case 1:  # bxl
            if debug:
                print('bxl', val, regs)
            regs['B'] = regs['B'] ^ val
        case 2:  # bst
            if debug:
                print('bst', val, regs)
            regs['B'] = _get_combo(val, regs) % 8
        case 3:  # jnz
            if debug:
                print('jnz', val, regs)
            if regs['A'] != 0:
                pointer = val
        case 4:  # bxc
            if debug:
                print('bxc', val, regs)
            regs['B'] = regs['B'] ^ regs['C']
        case 5:  # out
            if debug:
                print('out', val, regs)
            output.append(_get_combo(val, regs) % 8)
        case 6:  # bdv
            if debug:
                print('bdv', val, regs)
            regs['B'] = regs['A'] // (2 ** _get_combo(val, regs))
        case 7:  # cdv
            if debug:
                print('cdv', val, regs)
            regs['C'] = regs['A'] // (2 ** _get_combo(val, regs))
        case _:
            raise ValueError(op_code, val)

    return pointer, regs


def compute(regs: dict[str, int], values: list[int], debug: bool = False) -> list[int]:
    pointer = 0
    output = []

    while 0 <= pointer < len(values):
        op_code = values[pointer]
        val = values[pointer + 1]

        new_pointer, regs = _perform(op_code, val, regs, pointer, output, debug=debug)

        if new_pointer != pointer:
            pointer = new_pointer
        else:
            pointer += 2

    return output


def solve1(file: Path):
    regs, values = read_input(file)

    print(regs, values)

    output = compute(regs, values)

    print(','.join(map(str, output)))


def find_a(a: int, j: int, values: list[int], ds: list[int]) -> int | None:
    if j < 0:
        return a

    for i in range(8):
        initial = a + i * ds[j]
        regs = {'A': initial, 'B': 0, 'C': 0}
        output = compute(regs, values)

        if len(output) == len(values) and output[j] == values[j]:
            f = find_a(initial, j - 1, values, ds)
            if f:
                return f
    return None


def solve2(file: Path):
    regs, values = read_input(file)

    print(regs, values)

    ds = [1]
    for i in range(1, len(values)):
        ds.append(ds[i - 1] * 8)

    result = find_a(0, len(values) - 1, values, ds)

    print(result)


if __name__ == '__main__':
    start = time.monotonic()
    solve1(Path('test.txt'))
    solve1(Path('test1.txt'))
    solve1(Path('input.txt'))
    print('Part1', time.monotonic() - start)
    start = time.monotonic()
    solve2(Path('test.txt'))
    solve2(Path('test1.txt'))
    solve2(Path('input.txt'))
    print('Part2', time.monotonic() - start)
