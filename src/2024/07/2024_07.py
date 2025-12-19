import dataclasses
import operator
from itertools import product

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclasses.dataclass
class Equation:
    target: int
    values: list[int]

    def possible(self, operators):
        for combination in product(operators, repeat=len(self.values) - 1):
            current = self.values[0]
            for i, op in enumerate(combination, start=1):
                current = op(current, self.values[i])
                if current > self.target:
                    break
            if current == self.target:
                return True
        return False


def main(debug: bool) -> None:
    input_data = load_data(debug)

    equations = parse_input(input_data)

    # part 1
    operators = [operator.add, operator.mul]
    result_part1 = sum([e.target for e in equations if e.possible(operators)])

    # part 2
    def concat(a, b):
        return int(str(a) + str(b))

    operators = [operator.add, operator.mul, concat]
    result_part2 = sum([e.target for e in equations if e.possible(operators)])

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> list[Equation]:
    equations = []
    for line in input_data.splitlines():
        s = line.split(":")
        target = int(s[0])
        values = [int(v) for v in s[1].strip().split(" ")]
        equations.append(Equation(target=target, values=values))
    return equations


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
