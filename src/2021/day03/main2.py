def find(lines, use_most_common):
    line_length = len(lines[0])

    current_lines = lines.copy()
    for i in range(line_length):
        count_half = len(current_lines) * 1.0 / 2
        count_0 = 0
        for line in current_lines:
            ch = line[i]
            if ch == 0:
                count_0 += 1
        most_common = 0 if count_0 > count_half else 1
        least_common = 0 if count_0 <= count_half else 1

        f = most_common if use_most_common else least_common
        current_lines = list(filter(lambda line: line[i] == f, current_lines))
        print(len(current_lines))
        if len(current_lines) == 1:
            return decode(current_lines[0])


def decode(sequence):
    result = 0
    l = len(sequence)
    for i in range(l):
        val = sequence[l - i - 1]
        multiplier = 2**i
        result = result + val * multiplier
    return result


def main():
    with open("input.txt") as f:
        lines = [[int(c) for c in l.strip()] for l in f.readlines()]

    print(f"{len(lines)} lines read")

    oxygen = find(lines, use_most_common=True)
    co2 = find(lines, use_most_common=False)

    print(f"Oxygen: {oxygen}")
    print(f"co2: {co2}")
    result = oxygen * co2
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
