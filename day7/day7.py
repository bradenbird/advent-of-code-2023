from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class Hand:
    cards: str
    bid: int


def parse_input(data: str) -> list[Hand]:
    return []



def solution(data: str, part_two: bool) -> int:
    return 0


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
        help="To produce output for the part2 version of this problem",
    )

    args = parser.parse_args()

    data = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

    if args.filename:
        with open(args.filename) as f:
            data = f.read()

    output = solution(data, args.part_two)

    print(f"Solution: {output}")


if __name__ == "__main__":
    main()
