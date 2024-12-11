from collections import Counter

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    stone_counter = parse_input(input_data)

    result_part1 = sum(blink(stone_counter, 25).values())
    result_part2 = sum(blink(stone_counter, 75).values())

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> Counter[int]:
    return Counter([int(n) for n in input_data.split(" ")])


def blink(initial_state: Counter[int], blinks: int) -> Counter[int]:
    current_state = Counter(initial_state)
    for _ in range(blinks):
        next_state = Counter(current_state)

        for number, count in current_state.items():
            next_state[number] -= count
            if number == 0:
                next_state[1] += count
            elif len(str(number)) % 2 == 0:
                s = str(number)
                split_point = len(s) // 2
                first = int(s[:split_point])
                second = int(s[split_point:])
                next_state[first] += count
                next_state[second] += count
            else:
                next_state[2024 * number] += count

        current_state = next_state

    return current_state


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
