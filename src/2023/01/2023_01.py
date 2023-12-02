import re

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    lines = [l for l in input_data.split("\n") if len(l) > 0]

    # part 1
    numbers = []
    for line in lines:
        digits = [d for d in line if re.match("\\d", d)]
        if digits:
            numbers.append(int(digits[0] + digits[-1]))
    result_part1 = sum(numbers)

    mapping = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
        **{str(d): str(d) for d in range(1, 10)},
    }
    regex = "|".join([f"({k})" for k in mapping.keys()])
    regex_rev = "|".join([f"({rev(k)})" for k in mapping.keys()])

    numbers = []
    for line in lines:
        m = re.search(regex, line)
        first_digit = mapping[m.group(0)]

        rev_line = rev(line)
        m = re.search(regex_rev, rev_line)
        second_digit = mapping[rev(m.group(0))]

        number = int(first_digit + second_digit)
        numbers.append(number)
    result_part2 = sum(numbers)

    submit_or_print(result_part1, result_part2, debug)


def rev(line):
    return "".join(reversed(line))


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
