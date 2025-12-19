import re
from dataclasses import dataclass

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclass
class Position:
    x: int
    y: int

    def __add__(self, direction: "Position"):
        return Position(self.x + direction.x, self.y + direction.y)

    def __mul__(self, d: int):
        return Position(self.x * d, self.y * d)

    def __rmul__(self, d: int):
        return self.__mul__(d)

    def __sub__(self, direction: "Position"):
        return Position(self.x - direction.x, self.y - direction.y)

    def __hash__(self):
        return hash(tuple([self.x, self.y]))

    def __eq__(self, other: "Position"):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return f"[{self.x},{self.y}]"


@dataclass
class Machine:
    button_a: Position
    button_b: Position
    prize_position: Position
    button_a_cost: int = 3
    button_b_cost: int = 1

    def cost(self):
        a1 = self.button_a.x
        a2 = self.button_a.y
        b1 = self.button_b.x
        b2 = self.button_b.y
        c1 = self.prize_position.x
        c2 = self.prize_position.y

        det = a1 * b2 - a2 * b1
        x = int((c1 * b2 - c2 * b1) / det)
        y = int((a1 * c2 - a2 * c1) / det)

        reached_position = self.button_a * x + self.button_b * y

        if reached_position == self.prize_position:
            return self.button_a_cost * x + self.button_b_cost * y
        else:
            return 0


def main(debug: bool) -> None:
    input_data = load_data(debug)

    machines = parse_input(input_data)

    # part 1
    result_part1 = sum([machine.cost() for machine in machines])

    # part 2
    for machine in machines:
        machine.prize_position += Position(10000000000000, 10000000000000)
    result_part2 = sum([machine.cost() for machine in machines])

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> list[Machine]:
    machines = []
    for machine_str in input_data.split("\n\n"):
        spl = machine_str.split("\n")
        positions = []
        for s in spl:
            p = re.findall(r"\d+", s)
            positions.append(Position(int(p[0]), int(p[1])))
        machines.append(
            Machine(
                button_a=positions[0],
                button_b=positions[1],
                prize_position=positions[2],
            )
        )
    return machines


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
