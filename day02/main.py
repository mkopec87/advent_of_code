from enum import IntEnum


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


def main():

    with open("input.txt") as f:
        lines = [l.strip() for l in f.readlines()]

    print(f"{len(lines)} lines read")

    result = 0
    for line in lines:
        spl = line.split(" ")
        opponent_shape = LETTER_TO_SHAPE[spl[0]]
        my_shape = LETTER_TO_SHAPE[spl[1]]
        outcome = my_shape.beats(opponent_shape)
        # print(my_shape, opponent_shape, outcome)
        score = OUTCOME_TO_SCORE[outcome] + SHAPE_TO_SCORE[my_shape]
        result += score
    print(f"Result: {result}")

    result = 0
    for line in lines:
        spl = line.split(" ")
        opponent_shape = LETTER_TO_SHAPE[spl[0]]
        outcome = LETTER_TO_OUTCOME[spl[1]]
        my_shape = opponent_shape.counter_shape(outcome)
        score = OUTCOME_TO_SCORE[outcome] + SHAPE_TO_SCORE[my_shape]
        result += score
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
