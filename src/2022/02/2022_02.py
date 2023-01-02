from enum import IntEnum

from src.utils.data import load_data
from src.utils.submission import submit_or_print


class Outcome(IntEnum):
    LOSE = -1
    DRAW = 0
    WIN = 1

    def negate(self):
        return Outcome(-self.value)


class Shape(IntEnum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    def beats(self, other: "Shape") -> Outcome:
        if self == other:
            return Outcome.DRAW
        if (self.value - other.value) % len(Shape) == 1:
            return Outcome.WIN
        return Outcome.LOSE

    def counter_shape(self, outcome: Outcome) -> "Shape":
        return Shape((self.value + outcome.value) % len(Shape))


LETTER_TO_SHAPE = {
    "X": Shape.ROCK,
    "Y": Shape.PAPER,
    "Z": Shape.SCISSORS,
    "A": Shape.ROCK,
    "B": Shape.PAPER,
    "C": Shape.SCISSORS,
}

LETTER_TO_OUTCOME = {
    "X": Outcome.LOSE,
    "Y": Outcome.DRAW,
    "Z": Outcome.WIN,
}

OUTCOME_TO_SCORE = {Outcome.WIN: 6, Outcome.DRAW: 3, Outcome.LOSE: 0}

SHAPE_TO_SCORE = {Shape.ROCK: 1, Shape.PAPER: 2, Shape.SCISSORS: 3}


def main(debug: bool) -> None:
    input_data = load_data(debug)
    lines = input_data.splitlines()

    result_part1 = 0
    for line in lines:
        spl = line.split(" ")
        opponent_shape = LETTER_TO_SHAPE[spl[0]]
        my_shape = LETTER_TO_SHAPE[spl[1]]
        outcome = my_shape.beats(opponent_shape)
        score = OUTCOME_TO_SCORE[outcome] + SHAPE_TO_SCORE[my_shape]
        result_part1 += score

    result_part2 = 0
    for line in lines:
        spl = line.split(" ")
        opponent_shape = LETTER_TO_SHAPE[spl[0]]
        outcome = LETTER_TO_OUTCOME[spl[1]]
        my_shape = opponent_shape.counter_shape(outcome)
        score = OUTCOME_TO_SCORE[outcome] + SHAPE_TO_SCORE[my_shape]
        result_part2 += score

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
