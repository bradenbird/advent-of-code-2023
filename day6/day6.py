from argparse import ArgumentParser
import math


def solution(data: str, part_two: bool) -> int:
    total = []
    return math.prod(total)


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

    data = """Time:      7  15   30
Distance:  9  40  200"""

    if args.filename:
        with open(args.filename) as f:
            data = f.read()

    output = solution(data, args.part_two)

    print(f"Solution: {output}")


if __name__ == "__main__":
    main()
