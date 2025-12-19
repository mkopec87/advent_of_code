import math
from functools import reduce

from tqdm import tqdm

from src.utils.data import load_data
from src.utils.submission import submit_or_print


def evolve(number: int, steps: int) -> tuple[list[int], list[int | None]]:
    numbers = [number]
    changes = [None]
    prev_last_digit = number % 10
    for _ in range(steps):
        number = next_secret(number)

        last_digit = int(str(number)[-1])
        change = last_digit - prev_last_digit
        prev_last_digit = last_digit

        changes.append(change)
        numbers.append(number)

    return numbers, changes


def next_secret(number: int) -> int:
    number = mix_and_prune(number * 64, number)
    number = mix_and_prune(math.floor(number / 32), number)
    number = mix_and_prune(number * 2048, number)
    return number


def mix_and_prune(next_number: int, number: int) -> int:
    number = next_number ^ number
    number = number % 16777216
    return number


def main(debug: bool) -> None:
    input_data = load_data(debug)

    # load input
    numbers = list(map(int, input_data.splitlines()))
    steps = 2000
    print(f"{len(numbers)} numbers")
    print(f"{steps} steps")

    # part 1
    result_part1 = sum([evolve(number, steps)[0][-1] for number in numbers])

    # part 2
    seq_to_prices = []
    for number in numbers:
        # collect 4-number change sequence to first price mapping
        secrets, changes = evolve(number, steps)
        seq_to_price = {}
        for i in range(1, len(changes) - 4):
            seq = tuple(changes[i : i + 4])
            if seq not in seq_to_price:
                seq_to_price[seq] = int(str(secrets[i + 3])[-1])

        seq_to_prices.append(seq_to_price)

    # collect all unique 4-number change sequences for all numbers
    seqs = reduce(set.union, [set(d.keys()) for d in seq_to_prices])
    print(f"{len(seqs)} unique 4-number change sequences")

    # find best 4-number change sequence
    best_seq = None
    best_price = -1
    for seq in tqdm(seqs):
        seq_price = sum([sp.get(seq, 0) for sp in seq_to_prices])
        if seq_price > best_price:
            best_seq = seq
            best_price = seq_price
    print(f"Best sequence: {best_seq}")
    print(f"Best price: {best_price}")

    result_part2 = best_price

    submit_or_print(result_part1, result_part2, debug)


if __name__ == "__main__":
    debug_mode = True
    # debug_mode = False
    main(debug_mode)
