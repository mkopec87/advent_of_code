INPUT_TXT = "input.txt"
# INPUT_TXT = "input-small.txt"
import re


def main():
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    numbers = list(map(int, re.findall("-?[0-9]+", lines[0])))
    print(numbers)

    target_x = (numbers[0], numbers[1])
    target_y = (numbers[2], numbers[3])

    def shoot(velocity):
        max_y = 0
        position = [0, 0]
        while True:
            if (
                target_x[0] <= position[0] <= target_x[1]
                and target_y[0] <= position[1] <= target_y[1]
            ):
                return max_y
            elif position[0] >= target_x[1] or position[1] < target_y[0]:
                return -1
            else:
                position[0] += velocity[0]
                position[1] += velocity[1]
                max_y = max(max_y, position[1])
                if velocity[0] > 0:
                    velocity[0] -= 1
                elif velocity[0] < 0:
                    velocity[0] += 1
                velocity[1] -= 1

    max_y = 0
    velocities = set()
    for x in range(1, target_x[1] + 1):
        for y in range(target_y[0], 1000):
            i = shoot([x, y])
            max_y = max(max_y, i)
            if i != -1:
                velocities.add(f"{x},{y}")

    result_part1 = max_y
    result_part2 = len(velocities)

    with open("v.txt", "w") as out:
        for v in sorted(velocities):
            out.write(v + "\n")

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
