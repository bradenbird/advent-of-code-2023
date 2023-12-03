from argparse import ArgumentParser
from collections import defaultdict
import math
import re

LIMITS = defaultdict(
    int,
    {
        "red": 12,
        "green": 13,
        "blue": 14,
    },
)

# compile all patterns only once
LINE_PATTERN = re.compile(r"^Game (\d+):(.*)$")


def create_block_dict(grab: str) -> dict[str, int]:
    # First, pull out the count and color
    count_colors = [x.strip().split(" ") for x in grab.split(",")]
    # Then make it in a dictionary, so we can handle this easier
    return {color: int(count) for count, color in count_colors}


# Used for part 1, along with the static `LIMITS`
def valid_input(color_counts: dict[str, int]) -> bool:
    for color, count in color_counts.items():
        if count > LIMITS[color]:
            return False
    return True


def parse_line(line: str, part_two: bool) -> int:
    match = LINE_PATTERN.match(line)
    if match is None:
        print("Error, shouldn't happen")
        return 0
    num, remainder = match.group(1, 2)
    num = int(num)
    # Split into each observation of bag contents
    individual_grabs = remainder.split(";")

    # Going to keep logic running to calculate both ways, then just return the result based on `part_two`
    min_counts = defaultdict(int)
    valid = True
    for grab in individual_grabs:
        blocks = create_block_dict(grab)
        valid &= valid_input(blocks)
        # Update the minimum count of each block needed.
        for color, count in blocks.items():
            min_counts[color] = max(min_counts[color], count)

    if part_two:
        return math.prod(min_counts.values())
    else:
        return num if valid else 0


def solution(data: str, part_two: bool) -> int:
    total = 0
    for line in data.split("\n"):
        total += parse_line(line, part_two)
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
        help="To produce output for the part2 version of this problem",
    )

    args = parser.parse_args()

    data = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    if args.filename:
        with open(args.filename) as f:
            data = f.read()

    output = solution(data, args.part_two)

    print(f"Solution: {output}")


if __name__ == "__main__":
    main()
