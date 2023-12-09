from argparse import ArgumentParser
from dataclasses import dataclass
import re

# compile all patterns only once
SEEDS_PATTERN = re.compile(r"^seeds: (.*)$")
OTHER_MAPS_PATTERN = re.compile(r"^[a-z\-]+ map:\n(.*)$", re.DOTALL)


@dataclass
class MappedRange:
    dest_start: int
    source_start: int
    range: int


def get_starting_values(line: str) -> list[int]:
    match = SEEDS_PATTERN.match(line)
    if match is None:
        print("Error: regex didn't match for seeds")
        return []
    return [int(x) for x in match.group(1).split(" ")]


def test_get_starting_values():
    assert get_starting_values("seeds: 1 2 3") == [1, 2, 3]
    assert get_starting_values("seeds: 1 2 3 12 23") == [1, 2, 3, 12, 23]
    assert get_starting_values("seeds: 1") == [1]


def parse_mapping(data: str) -> list[MappedRange]:
    output = []
    match = OTHER_MAPS_PATTERN.match(data)
    if match is None:
        print("Error: regex didn't match for map")
        return output
    for line in match.group(1).split("\n"):
        dest_start, source_start, duration = line.split(" ")
        output.append(MappedRange(int(dest_start), int(source_start), int(duration)))
    return output


def test_parse_mappings():
    assert parse_mapping(
        """water-to-light map:
1 5 2"""
    ) == [MappedRange(1, 5, 2)]
    assert parse_mapping(
        """light-to-temperature map:
1 5 2
81 45 19"""
    ) == [MappedRange(1, 5, 2), MappedRange(81, 45, 19)]


def apply_mapping(input_values: list[int], mappings: list[MappedRange]) -> list[int]:
    output = []
    for value in input_values:
        new_value = value
        for mapped_range in mappings:
            if (
                mapped_range.source_start
                <= value
                < mapped_range.source_start + mapped_range.range
            ):
                new_value = mapped_range.dest_start + (
                    value - mapped_range.source_start
                )
                break
        output.append(new_value)

    return output


def test_apply_mapping():
    assert apply_mapping([1], [MappedRange(5, 0, 3)]) == [6]
    assert apply_mapping([6], [MappedRange(0, 6, 3)]) == [0]
    assert apply_mapping([1, 2, 3], [MappedRange(5, 0, 4)]) == [6, 7, 8]
    assert apply_mapping([6], [MappedRange(70, 1, 3), MappedRange(100, 5, 10)]) == [101]
    assert apply_mapping(
        [79, 14, 55, 13], [MappedRange(50, 98, 2), MappedRange(52, 50, 48)]
    ) == [81, 14, 57, 13]
    assert apply_mapping(
        [81, 14, 57, 13], [MappedRange(0, 15, 37), MappedRange(37, 52, 2), MappedRange(39, 0, 15)]
    ) == [81, 53, 57, 52]

def solution(data: str, part_two: bool) -> int:
    data_split = data.split("\n\n")
    values = get_starting_values(data_split[0])
    for i in range(1, len(data_split)):
        mappings = parse_mapping(data_split[i])
        values = apply_mapping(values, mappings)

    return min(values)


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

    data = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

    if args.filename:
        with open(args.filename) as f:
            data = f.read()

    output = solution(data, args.part_two)

    print(f"Solution: {output}")


if __name__ == "__main__":
    main()
