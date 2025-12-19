import dataclasses
import math
import re

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclasses.dataclass
class Card:
    winning_numbers: set[int]
    card_numbers: set[int]

    def match_count(self) -> int:
        return len(self.card_numbers.intersection(self.winning_numbers))


def parse_input(input_data: str) -> list[Card]:
    cards = []
    for line in input_data.splitlines():
        line = line.split(":")[1].strip()
        winning_numbers_str, card_numbers_str = line.split("|", 1)
        winning_numbers = parse_integers(winning_numbers_str)
        card_numbers = parse_integers(card_numbers_str)
        card = Card(winning_numbers=winning_numbers, card_numbers=card_numbers)
        cards.append(card)
    return cards


def parse_integers(text: str) -> set[int]:
    return {int(m) for m in re.findall(r"[0-9]+", text)}


def main(debug: bool) -> None:
    input_data = load_data(debug)

    cards = parse_input(input_data)

    # part 1
    result_part1 = sum(
        [
            int(math.pow(2, card.match_count() - 1))
            for card in cards
            if card.match_count() > 0
        ]
    )

    # part 2
    card_count = len(cards)
    counts = [1 for _ in range(card_count)]
    for i, card in enumerate(cards):
        for j in range(card.match_count()):
            counts[i + j + 1] += counts[i]
    result_part2 = sum(counts)

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
