from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)
    banks = parse_data(input_data)

    result_part1 = solve(banks)
    result_part2 = solve(banks, digits=12)

    submit_or_print(result_part1, result_part2, debug)


def parse_data(input_data: str):
    return [list(map(int, bank)) for bank in input_data.splitlines()]


def solve(banks: list[list[int]], digits: int = 2) -> int:
    result = 0
    for bank in banks:
        batteries = []
        start = 0
        end = len(bank) - digits
        for _ in range(digits):
            max_digit, max_digit_position = find_max_digit(bank, start, end)
            start = max_digit_position + 1
            end = end + 1
            batteries.append(max_digit)
        result += int("".join(map(str, batteries)))

    return result


def find_max_digit(bank: list[int], start: int, end: int) -> tuple[int, int]:
    max_digit = -1
    max_digit_position = None
    for i in range(end, start - 1, -1):
        digit = bank[i]
        if digit >= max_digit:
            max_digit = digit
            max_digit_position = i
    return max_digit, max_digit_position


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
