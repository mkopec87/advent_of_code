def main():
    with open("input.txt") as f:
        commands = [l.strip() for l in f.readlines()]

    print(f"{len(commands)} commands read")

    horizontal = 0
    depth = 0
    aim = 0

    for command in commands:
        spl = command.split(" ")
        c = spl[0]
        v = int(spl[1])

        if c == "forward":
            horizontal += v
            depth += aim * v
        elif c == "down":
            aim += v
        elif c == "up":
            aim -= v
        else:
            raise Exception(f"Unknown command: {c}")

    result = depth * horizontal
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
