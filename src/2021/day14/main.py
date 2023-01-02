from collections import Counter

from tqdm import tqdm


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    polymer_str = lines[0]
    print(f"Polymer: {polymer_str}")

    rules = {}
    for line in lines[2:]:
        spl = line.split(" ")
        key = spl[0]
        val1 = key[0] + spl[2]
        val2 = spl[2] + key[1]
        rules[key] = {val1, val2}
    print(rules)

    def make_step(seq_counter):
        new_counter = Counter()
        for k, v in seq_counter.items():
            new_counter.update({key: v for key in rules[k]})
        return new_counter

    polymer = Counter(map("".join, zip(polymer_str, polymer_str[1:])))

    for step in tqdm(range(40)):
        print(polymer)
        polymer = make_step(polymer)

    letters = Counter()
    for k, v in polymer.items():
        for l in k:
            letters.update({l: v})
    letters.update({polymer_str[0]: 1, polymer_str[-1]: 1})

    print(letters)
    ordered = letters.most_common()
    print(ordered)
    result_part1 = (ordered[0][1] - ordered[-1][1]) / 2
    result_part2 = 0

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
