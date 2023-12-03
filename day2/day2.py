from argparse import ArgumentParser
from collections import defaultdict
import re

LIMITS = defaultdict(int, {
    'red': 12,
    'green': 13,
    'blue': 14,
})

# compile all patterns only once
LINE_PATTERN = re.compile(r'^Game (\d+):(.*)$')

def valid_input(grab):
    count_colors = [x.strip().split(' ') for x in grab.split(',')]
    for count, color in count_colors:
        if int(count) > LIMITS[color]:
            return False
    return True

def parse_line(line: str) -> int:
    match = LINE_PATTERN.match(line)
    if match is None:
        print('Error, shouldn\'t happen')
        return 0
    num, remainder = match.group(1, 2)
    num = int(num)
    # Each grab from the bag needs to be checked against the maximums of each color
    individual_grabs = remainder.split(';')

    valid = True
    for grab in individual_grabs:
        valid &= valid_input(grab)
    return num if valid else 0
    
def solution(data: str) -> int:
    total = 0
    for line in data.split('\n'):
        total += parse_line(line)
    return total

def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        '--filename',
        default=None,
        help='Filename containing input data. If not provided, uses the example from the problem',
    )

    args = parser.parse_args()

    data = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''

    if args.filename:
        with open(args.filename) as f:
            data = f.read()
    
    output = solution(data)
    
    print(f'Solution: {output}')

if __name__ == "__main__":
    main()
