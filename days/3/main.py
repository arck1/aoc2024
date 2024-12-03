import re
from pathlib import Path


def solve1(file: Path):
    s = file.read_text()

    regex = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')

    matches = regex.findall(s)
    result = 0
    for a, b in matches:
        result += int(a) * int(b)

    print(result)


def solve2(file: Path):
    s = file.read_text()

    regex = re.compile(r'(mul\((\d{1,3}),(\d{1,3})\))|(do\(\))|(don\'t\(\))')

    matches = regex.findall(s)
    flag = True
    result = 0
    for v in matches:
        if v[3] == 'do()':
            flag = True
        elif v[4] == "don't()":
            flag = False
        else:
            a, b = v[1], v[2]
            if flag:
                result += int(a) * int(b)

    print(result)


if __name__ == '__main__':
    solve1(Path('test.txt'))
    solve1(Path('input.txt'))

    solve2(Path('test2.txt'))
    solve2(Path('input.txt'))
