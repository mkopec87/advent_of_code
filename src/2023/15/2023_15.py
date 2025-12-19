import dataclasses
import re

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclasses.dataclass
class Lens:
    label: str
    focal: int


@dataclasses.dataclass
class Box:
    nr: int
    lenses: list

    def remove(self, label: str) -> None:
        for lens in self.lenses:
            if lens.label == label:
                self.lenses.remove(lens)
                break

    def add(self, lens: Lens) -> None:
        for i, l in enumerate(self.lenses):
            if l.label == lens.label:
                self.lenses.remove(l)
                self.lenses.insert(i, lens)
                break
        else:
            self.lenses.append(lens)

    def power(self) -> int:
        total = 0
        for slot_nr, lens in enumerate(self.lenses, start=1):
            total += (self.nr + 1) * slot_nr * lens.focal
        return total


def main(debug: bool) -> None:
    input_data = load_data(debug)

    steps = input_data.strip().split(",")

    # part 1
    total = 0
    for step in steps:
        total += hash(step)
    result_part1 = total

    # part 2
    boxes = {i: Box(i, []) for i in range(256)}
    for step in steps:
        match = re.match("([a-z]+)(.)(.*)", step)
        label_str = match.group(1)
        op_str = match.group(2)
        focal_str = match.group(3)

        box_nr = hash(label_str)
        box = boxes[box_nr]

        if op_str == "-":
            box.remove(label_str)
        elif op_str == "=":
            box.add(Lens(label_str, int(focal_str)))

    total = 0
    for box in boxes.values():
        total += box.power()
    result_part2 = total

    submit_or_print(result_part1, result_part2, debug)


def hash(string: str) -> int:
    cur = 0
    for ch in string:
        cur += ord(ch)
        cur *= 17
        cur %= 256
    return cur


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
