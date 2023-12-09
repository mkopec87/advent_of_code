import operator
import re
from functools import reduce

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    # part 1
    lines = input_data.splitlines()
    times = map(int, re.findall(r"\d+", lines[0]))
    distances = map(int, re.findall(r"\d+", lines[1]))
    numbers = []
    for time, record_distance in zip(times, distances):
        ways = 0
        for hold_time in range(1, time + 1):
            distance = hold_time * (time - hold_time)
            if distance > record_distance:
                ways += 1
        numbers.append(ways)
    result_part1 = reduce(operator.mul, numbers)

    # part 2
    lines = input_data.splitlines()
    time = int("".join(re.findall(r"\d", lines[0])))
    record_distance = int("".join(re.findall(r"\d", lines[1])))
    ways = 0
    for hold_time in range(1, time + 1):
        distance = hold_time * (time - hold_time)
        if distance > record_distance:
            ways += 1
    result_part2 = ways

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
