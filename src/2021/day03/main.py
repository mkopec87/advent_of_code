def main():
    with open("input.txt") as f:
        lines = [l.strip() for l in f.readlines()]

    print(f"{len(lines)} commands read")

    line_length = len(lines[0])
    count_0_at_pos = {}
    for i in range(line_length):
        count_0_at_pos[i] = 0

    for line in lines:
        for i in range(line_length):
            ch = line[line_length - i - 1]
            if ch == "0":
                count_0_at_pos[i] += 1

    print(count_0_at_pos)

    gamma = 0
    epsilon = 0
    for i in range(line_length):
        most_common = 0 if count_0_at_pos[i] > len(lines) / 2 else 1
        least_common = 0 if most_common == 1 else 1
        multiplier = 2**i
        print(multiplier, most_common, least_common)
        gamma = gamma + most_common * multiplier
        epsilon = epsilon + least_common * multiplier

    result = gamma * epsilon
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
