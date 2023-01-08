from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    changes = [
        int(i[1:]) if i[0] == "+" else -int(i[1:]) for i in input_data.splitlines()
    ]
    result_part1 = sum(changes)

    frequencies = set()
    frequency = 0
    i = 0
    while True:
        change = changes[i]
        frequency += change
        if frequency in frequencies:
            break
        frequencies.add(frequency)
        i += 1
        i = i % len(changes)
    result_part2 = frequency

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
