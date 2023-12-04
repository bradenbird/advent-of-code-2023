from argparse import ArgumentParser
from dataclasses import dataclass


class PartNumber:
    def __init__(self, row, start_col, end_col, value):
        self.row: int = row
        self.start_col: int = start_col
        self.end_col: int = end_col
        self.value: int = value

    def is_gear_connected(self, row, col) -> bool:
        """
        If the specified gear location is connected to this part
        """
        # if it is within the +/- 1 boundary of our number, it is connected
        return (
            self.row - 1 <= row <= self.row + 1
            and self.start_col - 1 <= col <= self.end_col + 1
        )

    def __eq__(self, other) -> bool:
        return (
            self.row == other.row
            and self.start_col == other.start_col
            and self.end_col == other.end_col
            and self.value == other.value
        )

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self):
        return (
            hash(self.row)
            + hash(self.start_col)
            + hash(self.end_col)
            + hash(self.value)
        )


@dataclass
class Grid:
    rows: list[str]
    height: int
    width: int


@dataclass
class FindGearResult:
    found: bool
    gears: list[tuple[int, int]]


def is_symbol(char: str) -> bool:
    return not (char.isdigit() or char == ".")


def test_is_symbol():
    assert is_symbol(".") is False, "'.' is wrongly classified as a symbol"
    for num in [str(x) for x in range(10)]:
        assert is_symbol(num) is False, f"'{num}' is wrongly classified as a symbol"
    assert is_symbol("$") is True, "'$' is wrongly classified as NOT a symbol"
    assert is_symbol("#") is True, "'$' is wrongly classified as NOT a symbol"
    assert is_symbol("@") is True, "'$' is wrongly classified as NOT a symbol"
    assert is_symbol("*") is True, "'$' is wrongly classified as NOT a symbol"
    assert is_symbol("+") is True, "'$' is wrongly classified as NOT a symbol"


def within_grid(grid: Grid, row: int, col: int):
    return 0 <= row < grid.height and 0 <= col < grid.width


def test_within_grid():
    grid = Grid(rows=[], height=10, width=10)
    assert within_grid(grid, 0, 0) is True, "Failed within_grid check"
    assert within_grid(grid, 1, 1) is True, "Failed within_grid check"
    assert within_grid(grid, 9, 0) is True, "Failed within_grid check"
    assert within_grid(grid, 0, 9) is True, "Failed within_grid check"
    assert within_grid(grid, 9, 9) is True, "Failed within_grid check"

    assert within_grid(grid, -1, 0) is False, "Failed within_grid check"
    assert within_grid(grid, 0, -1) is False, "Failed within_grid check"
    assert within_grid(grid, -1, -1) is False, "Failed within_grid check"
    assert within_grid(grid, 9, 10) is False, "Failed within_grid check"
    assert within_grid(grid, 10, 9) is False, "Failed within_grid check"
    assert within_grid(grid, 10, 10) is False, "Failed within_grid check"


def get_part_numbers(line: str, row_num: int) -> list[PartNumber]:
    part_nums = []
    index = 0
    num_start = None
    length = len(line)
    while index < length:
        char = line[index]
        if char.isdigit():
            if num_start is None:
                num_start = index
        else:
            if num_start is not None:
                part_nums.append(
                    PartNumber(
                        row_num,
                        num_start,
                        index - 1,
                        int(line[num_start:index]),
                    )
                )
                num_start = None
        index += 1

    if num_start is not None:
        # At the end of the string, and therefore this part number that was in-progress
        part_nums.append(
            PartNumber(
                row_num,
                num_start,
                index - 1,
                int(line[num_start:index]),
            )
        )
    return part_nums


def test_get_part_numbers():
    res = get_part_numbers("", 1)
    assert len(res) == 0

    res = get_part_numbers("1.2", 1)
    assert len(res) == 2
    assert res[0].start_col == 0
    assert res[0].end_col == 0
    assert res[0].value == 1
    assert res[1].start_col == 2
    assert res[1].end_col == 2
    assert res[1].value == 2

    res = get_part_numbers("123", 1)
    assert len(res) == 1
    # Check the row part once, just to make sure it is being used. Can skip for future checks below
    assert res[0].row == 1
    assert res[0].start_col == 0
    assert res[0].end_col == 2
    assert res[0].value == 123

    res = get_part_numbers("123.456", 1)
    assert len(res) == 2
    assert res[0].start_col == 0
    assert res[0].end_col == 2
    assert res[0].value == 123
    assert res[1].start_col == 4
    assert res[1].end_col == 6
    assert res[1].value == 456

    res = get_part_numbers(".123.456.", 1)
    assert len(res) == 2
    assert res[0].start_col == 1
    assert res[0].end_col == 3
    assert res[0].value == 123
    assert res[1].start_col == 5
    assert res[1].end_col == 7
    assert res[1].value == 456

    res = get_part_numbers("$123@456*", 1)
    assert len(res) == 2
    assert res[0].start_col == 1
    assert res[0].end_col == 3
    assert res[0].value == 123
    assert res[1].start_col == 5
    assert res[1].end_col == 7
    assert res[1].value == 456


def get_check_locations(part_number: PartNumber) -> list[tuple[int, int]]:
    locations = []
    # left and right of number added first
    locations.append((part_number.row, part_number.start_col - 1))
    locations.append((part_number.row, part_number.end_col + 1))
    # Then add the 'rows' above and below the number (4 X's in the example above)
    for col in range(part_number.start_col - 1, part_number.end_col + 2):
        locations.append((part_number.row - 1, col))
        locations.append((part_number.row + 1, col))
    return locations


def valid_part_number(grid: Grid, part_number: PartNumber):
    """
    Need to check the spots marked with X for a symbol around the number `12`:
    ```
    XXXX.
    X12X.
    XXXX.
    ```
    """

    locations = get_check_locations(part_number)

    # Once we have the list, iterate through it until we find a symbol
    for row, col in locations:
        if not within_grid(grid, row, col):
            continue
        if is_symbol(grid.rows[row][col]):
            # Can exit early here as we found an adjacent symbol
            return True
    # No symbol found
    return False


def test_valid_part_number():
    # Test diagonal symbols
    grid = Grid(["1.2", ".*.", "3.4"], height=3, width=3)
    part1 = PartNumber(0, 0, 0, 1)
    part2 = PartNumber(0, 2, 2, 2)
    part3 = PartNumber(2, 0, 0, 3)
    part4 = PartNumber(2, 2, 2, 4)
    assert valid_part_number(grid, part1) is True
    assert valid_part_number(grid, part2) is True
    assert valid_part_number(grid, part3) is True
    assert valid_part_number(grid, part4) is True

    # Test direct-neighbor numbers
    grid = Grid([".1.", "2*3", ".4."], height=3, width=3)
    part1 = PartNumber(0, 1, 1, 1)
    part2 = PartNumber(1, 0, 0, 2)
    part3 = PartNumber(1, 2, 2, 3)
    part4 = PartNumber(2, 1, 1, 4)
    assert valid_part_number(grid, part1) is True
    assert valid_part_number(grid, part2) is True
    assert valid_part_number(grid, part3) is True
    assert valid_part_number(grid, part4) is True

    # Test no-neighbors
    grid = Grid([".....", ".123.", "....."], height=3, width=5)
    part1 = PartNumber(1, 1, 4, 123)
    assert valid_part_number(grid, part1) is False


def only_valid_part_numbers(
    grid: Grid, part_numbers: list[PartNumber]
) -> list[PartNumber]:
    return [x for x in part_numbers if valid_part_number(grid, x)]


def find_gears_for_part(grid: Grid, part_number: PartNumber) -> FindGearResult:
    locations = get_check_locations(part_number)
    gears = []
    # Once we have the list, iterate through it until we find a symbol
    for row, col in locations:
        if not within_grid(grid, row, col):
            continue
        if grid.rows[row][col] == "*":
            gears.append((row, col))
    return FindGearResult(len(gears) != 0, gears)


def possible_gears(grid: Grid, part_list: list[PartNumber]) -> set[tuple[int, int]]:
    maybe_gears = set()
    for part_number in part_list:
        res = find_gears_for_part(grid, part_number)
        if res.found:
            for gear in res.gears:
                maybe_gears.add(gear)
    return maybe_gears


def test_possible_gears():
    grid = Grid([".1.", ".*.", "..2"], 3, 3)
    part_list = [PartNumber(0, 1, 1, 1), PartNumber(2, 2, 2, 2)]
    gears = possible_gears(grid, part_list)
    assert len(gears) == 1
    assert (1, 1) in gears

    grid = Grid(["*1*", ".*.", "..2"], 3, 3)
    gears = possible_gears(grid, part_list)
    assert len(gears) == 3
    assert (1, 1) in gears
    assert (0, 0) in gears
    assert (0, 2) in gears


def solution(data: str, part_two: bool) -> int:
    possible_part_nums = []
    grid = Grid(data.split("\n"), 0, 0)
    grid.height = len(grid.rows)
    grid.width = len(grid.rows[0])

    for i in range(grid.height):
        possible_part_nums.extend(get_part_numbers(grid.rows[i], i))
    valid_part_nums = only_valid_part_numbers(grid, possible_part_nums)

    total = 0
    if part_two:
        # todo: probably should move to its own function so it could be tested
        part_nums_set = set(valid_part_nums)
        gears = possible_gears(grid, valid_part_nums)
        for gear_row, gear_col in gears:
            matching_parts: list[PartNumber] = []
            for part in part_nums_set:
                if part.is_gear_connected(gear_row, gear_col):
                    matching_parts.append(part)
            if len(matching_parts) == 2:
                total += matching_parts[0].value * matching_parts[1].value
    else:
        for part in valid_part_nums:
            total += part.value
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

    data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

    if args.filename:
        with open(args.filename) as f:
            data = f.read()

    output = solution(data, args.part_two)

    print(f"Solution: {output}")


if __name__ == "__main__":
    main()
