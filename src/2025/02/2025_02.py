import math

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def main(debug: bool) -> None:
    input_data = load_data(debug)

    ranges = parse_input(input_data)

    result_part1 = solve_part1(ranges)
    result_part2 = solve_part2(ranges)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data: str) -> set[tuple[int, int]]:
    splits = input_data.split(",")
    ranges = set()
    for s in splits:
        s = s.split("-")
        ranges.add((int(s[0]), int(s[1])))
    return ranges


def solve_part1(ranges: set[tuple[int, int]]) -> int:
    result = 0
    for start, end in ranges:
        for i in range(start, end + 1):
            i_str = str(i)
            if len(i_str) % 2 != 0:
                continue
            half_len = len(i_str) // 2
            if i_str[half_len:] == i_str[:half_len]:
                result += i
    return result


def solve_part2(ranges: set[tuple[int, int]]) -> int:
    result = 0
    for start, end in sorted(ranges):
        for i in range(start, end + 1):
            i_str = str(i)
            valid = False
            for divisor in get_divisors(len(i_str)):
                chunks = set()
                for j in range(0, len(i_str), divisor):
                    chunk = i_str[j : j + divisor]
                    chunks.add(chunk)
                    if len(chunks) > 1:
                        break
                if len(chunks) == 1:
                    valid = True
                    break
            if valid:
                result += i
    return result


def get_divisors(n: int) -> set[int]:
    divisors = set()
    for i in range(1, int(math.sqrt(n)) + 2):
        if n % i == 0:
            divisors.add(i)
            divisors.add(n // i)
    return divisors - {n}


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
