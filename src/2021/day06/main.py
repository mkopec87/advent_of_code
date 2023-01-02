from collections import Counter


def print_counter(c: Counter):
    print("Counter:")
    for n in sorted(c.keys()):
        print(f"\t{n}:{c[n]}")


def main():
    with open("input.txt") as f:
        line = f.readline()
        numbers = [int(nr) for nr in line.split(",")]
    print(f"{len(numbers)} numbers read")

    counter = Counter()
    counter.update(numbers)
    print_counter(counter)

    days = 256

    while days > 0:
        days -= 1

        next_counter = Counter()
        for k, v in counter.items():
            if k == 0:
                next_counter.update({6: v, 8: v})
            else:
                next_counter.update({k - 1: v})

        counter = next_counter
        print_counter(next_counter)

    result = sum([v for k, v in counter.items()])
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
