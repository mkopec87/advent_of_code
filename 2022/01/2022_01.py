from aocd import data, submit


def main() -> None:
    elves = []
    for block in data.split("\n\n"):
        calories = sum([int(line) for line in block.splitlines()])
        elves.append(calories)

    result_part1 = max(elves)
    submit(result_part1, part="a")

    result_part2 = sum(sorted(elves)[-3:])
    submit(result_part2, part="b")


if __name__ == "__main__":
    main()
