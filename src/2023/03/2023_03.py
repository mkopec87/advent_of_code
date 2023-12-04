import dataclasses
import re
from typing import List

import numpy as np

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclasses.dataclass
class Number:
    row: int
    start: int
    end: int
    value: int

    def neighbours(self):
        for x in range(self.row - 1, self.row + 2):
            for y in range(self.start - 1, self.end + 1):
                yield x, y


@dataclasses.dataclass
class Gear:
    row: int
    col: int
    numbers: List[Number]


def main(debug: bool) -> None:
    input_data = load_data(debug)

    lines = input_data.splitlines()
    rows = []
    numbers = []
    gears = []
    for row, line in enumerate(lines, 1):
        rows.append(["."] + [ch for ch in line] + ["."])
        for m in re.finditer(r"[0-9]+", line):
            number = Number(
                row=row, start=m.start() + 1, end=m.end() + 1, value=int(m.group())
            )
            numbers.append(number)
        for m in re.finditer("\\*", line):
            gear = Gear(row=row, col=m.start() + 1, numbers=[])
            gears.append(gear)
    border = ["." for _ in range(len(rows[0]))]
    rows.insert(0, border)
    rows.append(border)
    matrix = np.matrix(rows)

    total = 0
    for number in numbers:
        for x, y in number.neighbours():
            if re.match(r"[^0-9.]", str(matrix[x, y])):
                total += number.value
                break

    result_part1 = total

    for gear in gears:
        for number in numbers:
            if (gear.row, gear.col) in number.neighbours():
                gear.numbers.append(number)

    total = 0
    for gear in gears:
        if len(gear.numbers) == 2:
            total += gear.numbers[0].value * gear.numbers[1].value
    result_part2 = total

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
