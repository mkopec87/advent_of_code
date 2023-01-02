def fuel(numbers, target, costs):
    f = 0
    for n in numbers:
        steps = abs(target - n)
        f += costs[steps]
    return f


def main():
    with open("input.txt") as f:
        line = f.readline()
        numbers = [int(nr) for nr in line.split(",")]
    print(f"{len(numbers)} numbers read")

    costs = {}
    max_dist = abs(min(numbers) - max(numbers))
    cost = 0
    total_cost = 0
    for t in range(0, max_dist + 1):
        costs[t] = total_cost
        cost += 1
        total_cost += cost
    print(costs)

    min_fuel = costs[max_dist] * len(numbers)
    for t in range(min(numbers), max(numbers) + 1):
        f = fuel(numbers, t, costs)
        min_fuel = min(min_fuel, f)
        print(t, f)

    result = min_fuel
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
