# Moved part 2 out into a different file since the approach completely changed
from argparse import ArgumentParser
from dataclasses import dataclass
from collections import deque
import re

# compile all patterns only once
SEEDS_PATTERN = re.compile(r"^seeds: (.*)$")
OTHER_MAPS_PATTERN = re.compile(r"^[a-z\-]+ map:\n(.*)$", re.DOTALL)


# This approach needs to speak in Ranges, as calculating by individual numbers is prohibitively expensive memory-wise
@dataclass(init=False)
class Range:
    # Represents a range from [start, end)
    start: int
    length: int
    end: int

    def __init__(self, start: int, length: int):
        self.start = start
        self.length = length
        self.end = start + length

    def __lt__(self, other):
        return self.start < other.start

    def __gt__(self, other):
        return self.start > other.start

    def __le__(self, other):
        return self.start <= other.start

    def __ge__(self, other):
        return self.start >= other.start


def test_range_constructor():
    r = Range(0, 5)
    assert r.start == 0
    assert r.length == 5
    assert r.end == 5
    r = Range(10, 2)
    assert r.start == 10
    assert r.length == 2
    assert r.end == 12


@dataclass
class MappedRange:
    # Holds a range and the offset of the starting point for the output range to be calculated from
    input_range: Range
    offset: int


def ranges_overlap(a: Range, b: Range) -> bool:
    return a.start <= b.start < a.end or b.start <= a.start < b.end


def test_ranges_overlap():
    assert ranges_overlap(Range(0, 5), Range(0, 5))
    assert ranges_overlap(Range(0, 5), Range(4, 5))
    assert ranges_overlap(Range(4, 5), Range(0, 5))
    assert not ranges_overlap(Range(0, 1), Range(1, 1))
    assert not ranges_overlap(Range(1, 1), Range(0, 1))
    assert ranges_overlap(Range(1, 2), Range(0, 5))
    assert ranges_overlap(Range(0, 5), Range(1, 2))


def range_intersect(a: Range, b: Range) -> Range:
    # Assumes they overlap, check with `ranges_overlap(a, b)` first
    new_start = max(a.start, b.start)
    new_end = min(a.end, b.end)
    return Range(new_start, new_end - new_start)


def test_range_intersect():
    assert range_intersect(Range(0, 10), Range(2, 5)) == Range(2, 5)
    assert range_intersect(Range(2, 5), Range(0, 10)) == Range(2, 5)

    assert range_intersect(Range(0, 10), Range(5, 10)) == Range(5, 5)
    assert range_intersect(Range(5, 10), Range(0, 10)) == Range(5, 5)


@dataclass(init=False)
class TransformResult:
    def __init__(
        self,
        unchanged: Range | None = None,
        transformed_range: Range | None = None,
        remainders: list[Range] | None = None,
    ):
        self.unchanged = unchanged
        self.transformed_range = transformed_range
        self.remainders = remainders

    def transformed(self) -> bool:
        return self.unchanged is None


def test_transform_result():
    v = TransformResult(unchanged=Range(0, 1))
    assert not v.transformed()
    assert v.unchanged == Range(0, 1)
    v = TransformResult(
        transformed_range=Range(100, 1), remainders=[Range(0, 1), Range(2, 1)]
    )
    assert v.transformed()
    assert v.transformed_range == Range(100, 1)
    assert v.remainders == [Range(0, 1), Range(2, 1)]


# Taking an input range, and split it into multiple lists (if necessary) to apply the mapping provided
def apply_transform(
    input_range: Range, transform_range: MappedRange
) -> TransformResult:
    if ranges_overlap(input_range, transform_range.input_range):
        remainders = []
        transformed = range_intersect(input_range, transform_range.input_range)
        # transformed is currently the range we are cutting out of the input range to transform.
        # If there is any range lesser or higher, put those in remainders now
        lower_length = transformed.start - input_range.start
        if lower_length > 0:
            remainders.append(Range(input_range.start, lower_length))
        upper_length = input_range.end - transformed.end
        if upper_length > 0:
            remainders.append(Range(transformed.end, upper_length))

        # Now, apply transformation to the range
        transformed = Range(
            transformed.start + transform_range.offset, transformed.length
        )
        return TransformResult(transformed_range=transformed, remainders=remainders)
    else:
        return TransformResult(unchanged=input_range)


def test_apply_transform():
    # No transform applied
    assert apply_transform(
        Range(0, 10), MappedRange(Range(100, 3), 100)
    ) == TransformResult(unchanged=Range(0, 10))
    assert apply_transform(
        Range(0, 10), MappedRange(Range(10, 3), 100)
    ) == TransformResult(unchanged=Range(0, 10))

    # Lower remainder only
    assert apply_transform(
        Range(0, 11), MappedRange(Range(10, 3), 100)
    ) == TransformResult(transformed_range=Range(110, 1), remainders=[Range(0, 10)])

    # Upper remainder only
    assert apply_transform(
        Range(0, 11), MappedRange(Range(0, 1), 100)
    ) == TransformResult(transformed_range=Range(100, 1), remainders=[Range(1, 10)])

    # Both sides remainder
    assert apply_transform(
        Range(0, 11), MappedRange(Range(5, 2), 100)
    ) == TransformResult(
        transformed_range=Range(105, 2), remainders=[Range(0, 5), Range(7, 4)]
    )


def get_starting_ranges(line: str) -> list[Range]:
    match = SEEDS_PATTERN.match(line)
    if match is None:
        print("Error: regex didn't match for seeds")
        return []
    values = [int(x) for x in match.group(1).split(" ")]
    output = []
    for i in range(0, len(values), 2):
        output.append(Range(values[i], values[i + 1]))
    return output


def test_get_starting_ranges():
    assert get_starting_ranges("seeds: 1 2 3 4") == [Range(1, 2), Range(3, 4)]
    assert get_starting_ranges("seeds: 0 100 200 10 150 25") == [
        Range(0, 100),
        Range(200, 10),
        Range(150, 25),
    ]


def parse_mapping(data: str) -> list[MappedRange]:
    output = []
    match = OTHER_MAPS_PATTERN.match(data)
    if match is None:
        print("Error: regex didn't match for map")
        return output
    for line in match.group(1).split("\n"):
        dest_start, source_start, duration = line.split(" ")
        output.append(
            MappedRange(
                Range(int(source_start), int(duration)),
                int(dest_start) - int(source_start),
            )
        )
    return output


def test_parse_mappings():
    assert parse_mapping(
        """water-to-light map:
1 5 2"""
    ) == [MappedRange(Range(5, 2), -4)]
    assert parse_mapping(
        """light-to-temperature map:
1 5 2
81 45 19"""
    ) == [MappedRange(Range(5, 2), -4), MappedRange(Range(45, 19), 36)]


def apply_mapping(
    current_ranges: list[Range], mappings: list[MappedRange]
) -> list[Range]:
    # For each mapping group, process all of `current_ranges` once. If a range has been transformed, put it into `next_ranges`
    next_ranges: list[Range] = []
    unmapped_ranges: list[Range] = []
    for mapping in mappings:
        for range_to_check in current_ranges:
            res: TransformResult = apply_transform(range_to_check, mapping)
            if res.transformed():
                unmapped_ranges.extend(res.remainders)
                next_ranges.append(res.transformed_range)
            else:
                unmapped_ranges.append(res.unchanged)
        current_ranges = unmapped_ranges
        unmapped_ranges = []

    # If we still have values in `current_ranges`, they weren't applied to any mapping.
    # Put into next_ranges as-is
    next_ranges.extend(current_ranges)
    return next_ranges


def test_apply_mapping():
    current_ranges = [Range(79, 14), Range(55, 13)]
    mappings = [MappedRange(Range(98, 2), -48), MappedRange(Range(50, 48), 2)]

    new_ranges = apply_mapping(current_ranges, mappings)
    assert len(new_ranges) == 2
    assert new_ranges == [Range(81, 14), Range(57, 13)]

    current_ranges = new_ranges
    mappings = [
        MappedRange(Range(15, 37), -15),
        MappedRange(Range(52, 2), -15),
        MappedRange(Range(0, 15), 39),
    ]
    new_ranges = apply_mapping(current_ranges, mappings)
    assert len(new_ranges) == 2
    assert new_ranges == [Range(81, 14), Range(57, 13)]

    current_ranges = new_ranges
    mappings = [
        MappedRange(Range(53, 8), -4),
        MappedRange(Range(11, 42), -11),
        MappedRange(Range(0, 7), 42),
        MappedRange(Range(7, 4), 50),
    ]
    new_ranges = apply_mapping(current_ranges, mappings)
    assert len(new_ranges) == 3
    assert new_ranges == [Range(53, 4), Range(81, 14), Range(61, 9)]


def solution(data: str) -> int:
    data_split = data.split("\n\n")
    current_ranges = get_starting_ranges(data_split[0])
    for i in range(1, len(data_split)):
        current_ranges = apply_mapping(current_ranges, parse_mapping(data_split[i]))
        # TODO: maybe need to merge overlapping intervals at this point to reduce future iteration complexities?

    # Now, just get the smallest range's starting value to get the lowest number possible after all mappings were completed
    return min(current_ranges).start


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--filename",
        default=None,
        help="Filename containing input data. If not provided, uses the example from the problem",
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

    output = solution(data)

    print(f"Solution: {output}")


if __name__ == "__main__":
    main()
