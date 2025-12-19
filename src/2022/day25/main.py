from dataclasses import dataclass
from functools import lru_cache


def main():
    path = "input.txt"

    numbers_snafu = read_input(path)
    numbers_decimal = [decrypt(n) for n in numbers_snafu]
    result_part1 = encrypt(sum(numbers_decimal))

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")


def read_input(path: str) -> list[str]:
    with open(path) as f:
        return [line.strip() for line in f.readlines()]


def decrypt(number_str: str) -> int:
    ch2val = {"-": -1, "=": -2}
    total = 0
    multiplier = 1
    for ch in reversed(number_str):
        if ch in ch2val:
            val = ch2val[ch]
        else:
            val = int(ch)
        total += multiplier * val
        multiplier *= 5
    return total


@dataclass
class Interval:
    min: int
    max: int

    def __contains__(self, item):
        return self.min <= item <= self.max


@lru_cache
def interval_for_power(base: int):
    min_for_base = sum(-2 * (5**i) for i in range(base + 1))
    max_for_base = sum(2 * (5**i) for i in range(base + 1))
    return Interval(min_for_base, max_for_base)


def encrypt(number: int) -> str:
    base = minimal_power(number)
    if base == 0:
        result = encrypt_digit(number)
        assert decrypt(result) == number
        return result

    for option in range(-2, 3, 1):
        value_for_option = option * (5**base)
        less_digits_interval = interval_for_power(base - 1)
        min_for_option = value_for_option + less_digits_interval.min
        max_for_option = value_for_option + less_digits_interval.max
        interval_for_option = Interval(min_for_option, max_for_option)
        if number in interval_for_option:
            new_total = number - value_for_option
            result = encrypt_digit(option) + encrypt(new_total).rjust(base, "0")
            assert decrypt(result) == number
            return result

    raise Exception(f"Encryption of number {number} not found!")


def minimal_power(number: int) -> int:
    power = 0
    while True:
        interval = interval_for_power(power)
        if number in interval:
            break
        power += 1
    return power


def encrypt_digit(number: int) -> str:
    if 0 <= number <= 2:
        return str(number)
    elif number == -1:
        return "-"
    elif number == -2:
        return "="
    else:
        raise Exception(f"Single-digit encoding of the number {number} not supported!")


if __name__ == "__main__":
    main()
