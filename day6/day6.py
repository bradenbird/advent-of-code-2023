from argparse import ArgumentParser
from dataclasses import dataclass
import math
import re

# compile all patterns only once
LINE_PATTERN = re.compile(r"^[A-Za-z]+:(.*)$")


@dataclass
class Race:
    time_limit: int
    record_distance: int


def parse_input(data: str, part_two: bool) -> list[Race]:
    times, distances = data.split("\n")
    if part_two:
        times = [
            int(
                "".join(
                    [
                        x
                        for x in LINE_PATTERN.match(times).group(1).split(" ")
                        if x != ""
                    ]
                )
            )
        ]
        distances = [
            int(
                "".join(
                    [
                        x
                        for x in LINE_PATTERN.match(distances).group(1).split(" ")
                        if x != ""
                    ]
                )
            )
        ]
    else:
        times = [
            int(x) for x in LINE_PATTERN.match(times).group(1).split(" ") if x != ""
        ]
        distances = [
            int(x) for x in LINE_PATTERN.match(distances).group(1).split(" ") if x != ""
        ]
    return [Race(x, y) for x, y in zip(times, distances)]


def test_parse_input():
    data = """Time:      7  15   30
Distance:  9  40  200"""
    assert parse_input(data, False) == [Race(7, 9), Race(15, 40), Race(30, 200)]
    assert parse_input(data, True) == [Race(71530, 940200)]


def min_waiting_time(race: Race) -> int:
    time = 1
    while time < race.time_limit:
        distance = time * (race.time_limit - time)
        if distance > race.record_distance:
            return time
        time += 1
    print("Error: unable to beat the record!")
    return 0


def test_min_waiting_time():
    assert min_waiting_time(Race(7, 9)) == 2
    assert min_waiting_time(Race(7, 10)) == 3


def num_ways_to_win(race: Race):
    # Only need minimum waiting time since the the max waiting time decreases at the same rate when you increase the distance,
    # meaning multiplying the min by 2 lets us avoid calculating the same number twice
    return race.time_limit - (2 * min_waiting_time(race)) + 1


def test_num_ways_to_win():
    assert num_ways_to_win(Race(7, 9)) == 4
    assert num_ways_to_win(Race(7, 10)) == 2


def solution(data: str, part_two: bool) -> int:
    ways = []
    races = parse_input(data, part_two)
    for race in races:
        ways.append(num_ways_to_win(race))
    return math.prod(ways)


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
