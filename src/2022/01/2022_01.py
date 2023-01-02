from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    elves = []
    for block in input_data.split("\n\n"):
        calories = sum([int(line) for line in block.splitlines()])
        elves.append(calories)

    result_part1 = max(elves)
    result_part2 = sum(sorted(elves)[-3:])

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
