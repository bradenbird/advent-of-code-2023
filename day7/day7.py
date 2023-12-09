from argparse import ArgumentParser
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import total_ordering

@total_ordering
class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

    def __lt__(self, other):
        return self.value < other.value


# Mapping of card values for quick comparisons
CARD_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


@dataclass(init=False, eq=False)
class Hand:
    cards: str
    bid: int
    hand_type: HandType

    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
        # Default to high card, but if it is something better, we will update it in _calculate_hand_type()
        self.hand_type = HandType.HIGH_CARD

        # Calculate what type of hand we have
        self._calculate_hand_type()

    def _calculate_hand_type(self) -> None:
        counts = sorted(
            [(num, card) for card, num in Counter(self.cards).items()], reverse=True
        )

        for num_cards, card in counts:
            if num_cards == 5:
                self.hand_type = HandType.FIVE_OF_A_KIND
                break
            elif num_cards == 4:
                self.hand_type = HandType.FOUR_OF_A_KIND
                break
            elif num_cards == 3:
                self.hand_type = HandType.THREE_OF_A_KIND
            elif num_cards == 2:
                if self.hand_type == HandType.THREE_OF_A_KIND:
                    # Actually a full house
                    self.hand_type = HandType.FULL_HOUSE
                elif self.hand_type == HandType.ONE_PAIR:
                    # Found a second pair
                    self.hand_type = HandType.TWO_PAIR
                else:
                    self.hand_type = HandType.ONE_PAIR
            else:
                # If we only have individual, separate cards left, can't improve our hand type.
                break

    def __lt__(self, other):
        if self.hand_type < other.hand_type:
            return True
        elif self.hand_type > other.hand_type:
            return False
        else:
            # Now need to compare card orders
            for left_c, right_c in zip(self.cards, other.cards):
                if CARD_VALUES[left_c] != CARD_VALUES[right_c]:
                    return CARD_VALUES[left_c] < CARD_VALUES[right_c]
            # If all match, they are equal
            return False

    def __ge__(self, other):
        return not self < other

    def __gt__(self, other):
        if self.hand_type > other.hand_type:
            return True
        elif self.hand_type < other.hand_type:
            return False
        else:
            # Now need to compare card orders
            for left_c, right_c in zip(self.cards, other.cards):
                if CARD_VALUES[left_c] != CARD_VALUES[right_c]:
                    return CARD_VALUES[left_c] > CARD_VALUES[right_c]
            # If all match, they are equal
            return False

    def __le__(self, other):
        return not self > other
    
    def __eq__(self, other):
        if self.hand_type != other.hand_type:
            return False
        else:
            # Now need to compare card orders
            for left_c, right_c in zip(self.cards, other.cards):
                if CARD_VALUES[left_c] != CARD_VALUES[right_c]:
                    return False
            # If all match, they are equal
            return True

    def __ne__(self, other):
        return not self == other


def test_hand_type():
    assert Hand("AAAAA", 10).hand_type == HandType.FIVE_OF_A_KIND
    assert Hand("AAAA2", 10).hand_type == HandType.FOUR_OF_A_KIND
    assert Hand("2AAAA", 10).hand_type == HandType.FOUR_OF_A_KIND
    assert Hand("22AAA", 10).hand_type == HandType.FULL_HOUSE
    assert Hand("23AAA", 10).hand_type == HandType.THREE_OF_A_KIND
    assert Hand("23AA3", 10).hand_type == HandType.TWO_PAIR
    assert Hand("23AA4", 10).hand_type == HandType.ONE_PAIR
    assert Hand("23456", 10).hand_type == HandType.HIGH_CARD

def test_hand_comparators():
    assert Hand("AAAAA", 10) > Hand("AAAA2", 10)
    assert Hand("2AAAA", 10) < Hand("AAAA2", 10)
    assert Hand("2AAAA", 10) != Hand("AAAA2", 10)
    assert Hand("2AAAA", 10) == Hand("2AAAA", 20)


def parse_input(data: str) -> list[Hand]:
    hands = []
    for line in data.split("\n"):
        cards, bid = line.split(" ")
        hands.append(Hand(cards, int(bid)))
    return hands


def solution(data: str, part_two: bool) -> int:
    hands = parse_input(data)
    hands.sort()
    winnings = hands[0].bid
    rank = 1
    for i in range(1, len(hands)):
        if hands[i-1] != hands[i]:
            # New rank for this item, increase before we calculate
            rank += 1
        winnings += rank * hands[i].bid
    return winnings


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
