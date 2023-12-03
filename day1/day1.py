from argparse import ArgumentParser

# Could probably play with some more efficient checks than hashing and looking up in a set, but we can start with this
def number_from_line(line) -> int:
    DIGITS = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    length = len(line)
    left_digit = 0
    while left_digit < length:
        if line[left_digit] in DIGITS:
            break
        left_digit += 1

    if left_digit == length:
        return 0

    right_digit = length - 1
    while right_digit >= 0:
        if line[right_digit] in DIGITS:
            break
        right_digit -= 1
    
    if right_digit < 0:
        return 0

    # Should have 2 valid digits now, convert from str to int
    return int(f'{line[left_digit]}{line[right_digit]}')


def solution(data: str) -> int:
    total = 0
    for line in data.split('\n'):
        total += number_from_line(line)
    return total

def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        '--filename',
        default=None,
        help="Filename containing input data. If not provided, uses the example from the problem",
    )

    args = parser.parse_args()

    data = '''1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
'''

    if args.filename:
        with open(args.filename) as f:
            data = f.read()
    
    output = solution(data)
    
    print(f'Solution: {output}')

if __name__ == "__main__":
    main()
