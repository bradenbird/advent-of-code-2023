from argparse import ArgumentParser
from dataclasses import dataclass


@dataclass
class PartNumber:
    row: int
    start_col: int
    end_col: int
    value: int


@dataclass
class Grid:
    rows: list[str]
    height: int
    width: int


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
            print(f"digit at {index}, num_start={num_start}")
            if num_start is None:
                num_start = index
        else:
            print(f"no digit at {index}")
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


def solution(data: str, part_two: bool) -> int:
    total = 0
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
