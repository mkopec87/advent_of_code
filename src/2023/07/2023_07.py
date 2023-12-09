import dataclasses
import enum
from collections import Counter
from functools import cmp_to_key, partial
from typing import Callable, List

from src.utils.data import load_data
from src.utils.submission import submit_or_print

CARD_ORDER = ["A", "K", "Q", "T", *[str(i) for i in range(9, 1, -1)], "J"]


def card_rank(card: str) -> int:
    return CARD_ORDER.index(card)


class Type(enum.IntEnum):
    FIVE = 1
    FOUR = 2
    FULL = 3
    THREE = 4
    TWO = 5
    ONE = 6
    HIGH = 7


@dataclasses.dataclass
class Hand:
    cards: List[str]
    bid: int

    def hand_type_part1(self) -> Type:
        return self._hand_type(self.cards)

    def hand_type_part2(self) -> Type:
        non_joker_counts = Counter(filter(lambda c: c != "J", self.cards))
        if not non_joker_counts:
            return Type.FIVE
        ordered = non_joker_counts.most_common()
        most_common = ordered[0]
        cards = [(most_common[0] if c == "J" else c) for c in self.cards]
        return self._hand_type(cards)

    @staticmethod
    def _hand_type(cards: List[str]) -> Type:
        counts = Counter(cards)
        most_common = counts.most_common()[0]
        if most_common[1] == 5:
            return Type.FIVE
        if most_common[1] == 4:
            return Type.FOUR
        second_most_common = counts.most_common()[1]
        if most_common[1] == 3:
            if second_most_common[1] == 2:
                return Type.FULL
            return Type.THREE
        if most_common[1] == 2:
            if second_most_common[1] == 2:
                return Type.TWO
            return Type.ONE
        return Type.HIGH

    @staticmethod
    def compare(first: "Hand", second: "Hand", hand_type_function) -> bool:
        first_type = hand_type_function(first)
        second_type = hand_type_function(second)
        if first_type == second_type:
            for c1, c2 in zip(first.cards, second.cards):
                c1_rank = card_rank(c1)
                c2_rank = card_rank(c2)
                if c1_rank == c2_rank:
                    continue
                return c1_rank > c2_rank
        return first_type > second_type


def main(debug: bool) -> None:
    input_data = load_data(debug)
    hands = parse_input(input_data)

    result_part1 = solve(
        hands, partial(Hand.compare, hand_type_function=Hand.hand_type_part1)
    )
    result_part2 = solve(
        hands, partial(Hand.compare, hand_type_function=Hand.hand_type_part2)
    )

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> List[Hand]:
    hands = []
    for line in input_data.splitlines():
        cards = [c for c in line[:5]]
        bid = int(line.split(" ")[1])
        hands.append(Hand(cards, bid))
    return hands


def solve(hands: List[Hand], compare_function: Callable[[Hand, Hand], bool]) -> int:
    total = 0
    for rank, hand in enumerate(
        sorted(hands, key=cmp_to_key(compare_function)), start=1
    ):
        total += rank * hand.bid
    return total


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
