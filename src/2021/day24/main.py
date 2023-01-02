from tqdm import tqdm

INPUT_TXT = "input.txt"
# INPUT_TXT = "input-small.txt"


def valid(input, lines):
    input = [int(d) for d in str(input)]
    input_index = 0

    values = {x: 0 for x in "wxyz"}

    for line in lines:
        spl = line.split(" ")
        command = spl[0]
        target = spl[1]

        if command == "inp":
            values[target] = input[input_index]
            input_index += 1
        elif command == "add":
            values[target] = values[target] + other(spl, values)
        elif command == "mul":
            values[target] = values[target] * other(spl, values)
        elif command == "div":
            values[target] = values[target] // other(spl, values)
        elif command == "mod":
            values[target] = values[target] % other(spl, values)
        elif command == "eql":
            values[target] = 1 if values[target] == other(spl, values) else 0
        elif command == "neql":
            values[target] = 1 if values[target] != other(spl, values) else 0
        elif command == "set":
            values[target] = other(spl, values)
        else:
            raise Exception("Unknown command ", command)
    print(input, values["z"])
    return values["z"] == 0


def solve_part1(lines):
    for number in tqdm(range(int("9" * 14), 1, -1)):
        if "0" in str(number):
            continue
        if valid(number, lines):
            print(number)
            break


def other(spl, values):
    other = spl[2]
    return values[other] if other in values else int(other)


def main():
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    result_part1 = solve_part1(lines)
    result_part2 = 0

    # TODO:
    # - drop DIV x 1
    # - drop ADD x 0
    # - merge eql, eql into nql
    # - merge mul x 0, add x y -> set x y

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
