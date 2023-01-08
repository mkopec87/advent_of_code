import math

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)
    masses = [int(line) for line in input_data.splitlines()]

    def fuel(mass: int) -> int:
        return math.floor(mass / 3) - 2

    result_part1 = sum([fuel(mass) for mass in masses])

    def fuel2(mass: int) -> int:
        total = 0
        required = fuel(mass)
        while required > 0:
            total += required
            required = fuel(required)
        return total

    result_part2 = sum([fuel2(mass) for mass in masses])

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
