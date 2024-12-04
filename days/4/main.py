from pathlib import Path


def read_input(file: Path) -> list[list[str]]:
    return [list(line) for line in file.read_text().splitlines()]


def get_words(data: list[list[str]], *, i: int, j: int, length: int = 4) -> list[str]:
    words = []

    if j + length <= len(data[i]):
        words.append(''.join(data[i][j : j + length]))

    low = length - 1

    if j - low >= 0:
        words.append(''.join(data[i][j - k] for k in range(length)))

    if i + length <= len(data):
        words.append(''.join(data[i + k][j] for k in range(length)))
    if i - low >= 0:
        words.append(''.join(data[i - k][j] for k in range(length)))

    if i + length <= len(data) and j + length <= len(data[i]):
        words.append(''.join(data[i + k][j + k] for k in range(length)))

    if i + length <= len(data) and j - low >= 0:
        words.append(''.join([data[i + k][j - k] for k in range(length)]))

    if i - low >= 0 and j + length <= len(data[i]):
        words.append(''.join([data[i - k][j + k] for k in range(length)]))

    if i - low >= 0 and j - low >= 0:
        words.append(''.join([data[i - k][j - k] for k in range(length)]))

    return words


def solve1(file: Path):
    data = read_input(file)

    count = 0

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 'X':
                words = get_words(data, i=i, j=j)
                c = words.count('XMAS')
                if c > 0:
                    count += c

    print(count)


def _get_word(data: list[list[str]], start: tuple[int, int], d_row: int, d_col: int, length: int) -> str:
    i, j = start

    word = []
    for _ in range(length):
        if i < 0 or j < 0 or i >= len(data) or j >= len(data[i]):
            return ''

        word.append(data[i][j])

        i += d_row
        j += d_col

    return ''.join(word)


def is_x_mas(data: list[list[str]], *, i: int, j: int, length: int = 3) -> int:
    d1 = _get_word(data, (i - 1, j - 1), 1, 1, length)
    d1r = d1[::-1]
    d2 = _get_word(data, (i + 1, j - 1), -1, 1, length)
    d2r = d2[::-1]

    if not (d1 and d2):
        return 0

    keys = {'MAS', 'SAM'}
    count = 0

    if d1 in keys and d2 in keys and (d1 in (d2, d2r) or d1r in (d2, d2r)):
        count += 1

    return count


def solve2(file: Path):
    data = read_input(file)

    count = 0

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 'A':
                count += is_x_mas(data, i=i, j=j)

    print(count)


if __name__ == '__main__':
    solve1(Path('test.txt'))
    solve1(Path('input.txt'))

    solve2(Path('test.txt'))
    solve2(Path('input.txt'))
