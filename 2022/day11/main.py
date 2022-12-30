import math
import re


class Monkey:
    def __init__(self, id: int):
        self.id = id
        self.target = {}
        self.items = []
        self.inspections = 0
        self.test_factor = None


def main():
    with open("input.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} read")

    id_to_monkey = parse_monkeys(lines)
    result_part1 = solve(id_to_monkey, 20, lambda x: math.floor(x / 3))
    print(f"Result part 1: {result_part1}")  # 61503

    id_to_monkey = parse_monkeys(lines)
    d = math.prod([monkey.test_factor for monkey in id_to_monkey.values()])
    result_part2 = solve(id_to_monkey, 10_000, lambda x: x % d)
    print(f"Result part 2: {result_part2}")  # 14081365540


def solve(id_to_monkey, rounds, item_op):
    for _ in range(rounds):
        for monkey in id_to_monkey.values():
            for item in monkey.items:
                monkey.inspections += 1
                item = monkey.transform(item)
                item = item_op(item)
                t = monkey.target[monkey.test(item)]
                id_to_monkey[t].items.append(item)
            monkey.items = []
    s = sorted([m.inspections for m in id_to_monkey.values()], reverse=True)
    return math.prod(s[0:2])


def parse_monkeys(lines):
    def parse_var(x, var):
        if var == "old":
            return x
        else:
            return int(var)

    def parse_op(x, y, op):
        if op == "+":
            return x + y
        elif op == "*":
            return x * y

    id_to_monkey = {}
    for line in lines:
        if line.startswith("Monkey"):
            monkey = Monkey(int(re.match(r"Monkey (\d+):", line).group(1)))
            id_to_monkey[monkey.id] = monkey
        elif line.startswith("Operation"):
            m = re.match(r"Operation: new = ([^ ]+) (.) ([^ ]+)", line)
            var1 = m.group(1)
            op = m.group(2)
            var2 = m.group(3)
            monkey.transform = lambda item, var1=var1, var2=var2, op=op: parse_op(
                parse_var(item, var1), parse_var(item, var2), op
            )

        elif line.startswith("Test"):
            test_factor = int(re.match(r"Test: divisible by (\d+)", line).group(1))
            monkey.test_factor = test_factor
            monkey.test = lambda x, f=test_factor: x % f == 0
        elif line.startswith("If"):
            m = re.match(r"If ([a-z]+): throw to monkey (\d+)", line)
            test = m.group(1) == "true"
            target = int(m.group(2))
            monkey.target[test] = target
        elif line.startswith("Starting items"):
            items = [
                int(item.strip()) for item in line.split(":")[1].strip().split(",")
            ]
            monkey.items.extend(items)
    return id_to_monkey


if __name__ == "__main__":
    main()
