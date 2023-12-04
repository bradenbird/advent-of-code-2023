from argparse import ArgumentParser
from dataclasses import dataclass
import re


@dataclass
class ScratchCard:
    winning_nums: set[int]
    card_nums: list[int]
    card_id: int


# compile all patterns only once
LINE_PATTERN = re.compile(r"^Card[ ]+(\d+):(.*)$")


def parse_line(line: str) -> ScratchCard:
    # First, parse
    match = LINE_PATTERN.match(line)
    if match is None:
        print(f"Error, shouldn't happen, line: '{line}'")
        return ScratchCard({}, [], -1)
    card_num, remainder = match.group(1, 2)
    card_num = int(card_num)
    winning, actual = remainder.split("|")
    winning_nums = {int(x) for x in winning.split(" ") if x != ""}
    actual_nums = [int(x) for x in actual.split(" ") if x != ""]
    return ScratchCard(winning_nums, actual_nums, card_num)


def test_parse_line():
    res = parse_line("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    assert res.card_id == 1
    assert res.card_nums == [83, 86, 6, 31, 17, 9, 48, 53]
    assert res.winning_nums == {41, 48, 83, 86, 17}

    res = parse_line("Card  1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53")
    assert res.card_id == 1
    assert res.card_nums == [83, 86, 6, 31, 17, 9, 48, 53]
    assert res.winning_nums == {41, 48, 83, 86, 17}


def get_card_value(line: str) -> int:
    card = parse_line(line)
    matching_nums = 0
    for num in card.card_nums:
        if num in card.winning_nums:
            matching_nums += 1
    if matching_nums <= 1:
        return matching_nums
    return 2 ** (matching_nums - 1)


def test_get_card_value():
    assert get_card_value("Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53") == 8
    assert get_card_value("Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19") == 2
    assert get_card_value("Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1") == 2
    assert get_card_value("Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83") == 1
    assert get_card_value("Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36") == 0
    assert get_card_value("Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11") == 0


def solution(data: str, part_two: bool) -> int:
    total = 0
    for line in data.split("\n"):
        total += get_card_value(line)
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
        "--part-two",
        default=False,
        action="store_true",
        help="Run the program according to part 2 requirements",
    )

    args = parser.parse_args()

    data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    if args.filename:
        with open(args.filename) as f:
            data = f.read()

    output = solution(data, args.part_two)

    print(f"Solution: {output}")


if __name__ == "__main__":
    main()
