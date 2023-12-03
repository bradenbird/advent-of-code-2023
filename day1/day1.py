from argparse import ArgumentParser

DIGIT_STRS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "zero": 0,
}


def get_left_number(line: str, digit_only: bool):
    length = len(line)
    start_index = 0
    while start_index < length:
        if line[start_index].isdigit():
            return int(line[start_index])
        if not digit_only:
            for s, num in DIGIT_STRS.items():
                if line[start_index:].startswith(s):
                    return num
        start_index += 1
    # No matches, return 0
    return 0


def get_right_number(line: str, digit_only: bool):
    end_index = len(line) - 1
    while end_index >= 0:
        if line[end_index].isdigit():
            return int(line[end_index])
        if not digit_only:
            for s, num in DIGIT_STRS.items():
                if line[: end_index + 1].endswith(s):
                    return num
        end_index -= 1
    # No matches, return 0
    return 0


def number_from_line(line: str, digit_only: bool) -> int:
    return get_left_number(line, digit_only) * 10 + get_right_number(line, digit_only)


def solution(data: str, digit_only: bool) -> int:
    total = 0
    for line in data.split("\n"):
        total += number_from_line(line, digit_only)
    return total


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--filename",
        default=None,
        help="Filename containing input data. If not provided, uses the example from the problem",
    )

    parser.add_argument(
        "--digit-only",
        default=False,
        action="store_true",
        help="Use the part-1 line parsing on the input",
    )

    args = parser.parse_args()

    # Part 1 example data, can use instead if running part 1
    #     data = '''1abc2
    # pqr3stu8vwx
    # a1b2c3d4e5f
    # treb7uchet'''

    data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

    if args.filename:
        with open(args.filename) as f:
            data = f.read()

    output = solution(data, args.digit_only)

    print(f"Solution: {output}")


if __name__ == "__main__":
    main()
