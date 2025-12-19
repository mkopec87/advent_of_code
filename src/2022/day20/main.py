from dataclasses import dataclass


@dataclass
class Number:
    value: int
    next: "Number" = None
    prev: "Number" = None


def main():
    input_file = "input.txt"

    result_part1 = solve(input_file)
    result_part2 = solve(input_file, decryption_key=811589153, mix_count=10)

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")  # Expected sample: 3, full: 9687
    print(
        f"Result part 2: {result_part2}"
    )  # Expected sample: 1623178306, full: 1338310513297


def solve(
    input_file: str, decryption_key: int | None = 1, mix_count: int | None = 1
) -> int:
    print()

    initial_list = load_numbers(input_file, decryption_key)
    print(f"Loaded {len(initial_list)} numbers from {input_file}")

    print(f"Initial list: {list_to_string(initial_list)}")
    for i in range(mix_count):
        mix_list(initial_list)
        print(f"List after mixing {i + 1}: {list_to_string(initial_list)}")

    return score(initial_list)


def load_numbers(path: str, multiplier: int = 1) -> list[Number]:
    initial_list = []
    with open(path) as f:
        for line in f.readlines():
            value = int(line.strip()) * multiplier
            initial_list.append(Number(value))
    prev = initial_list[-1]
    for i, n in enumerate(initial_list):
        n.prev = prev
        n.next = initial_list[(i + 1) % len(initial_list)]
        prev = n
    return initial_list


def list_to_string(initial_list: list[Number]) -> str:
    values = []
    current = initial_list[0]
    max_values_shown = 3
    for _ in range(min(max_values_shown, len(initial_list))):
        values.append(str(current.value))
        current = current.next
    if len(initial_list) > max_values_shown:
        values.append("...")
    return "[" + ", ".join(values) + "]"


def mix_list(initial_list: list[Number]) -> None:
    for n in initial_list:
        shift = n.value % (len(initial_list) - 1)

        while shift > 0:
            shift -= 1
            current_next = n.next
            current_prev = n.prev
            new_next = n.next.next

            n.next = new_next
            new_next.prev = n
            n.prev = current_next
            current_next.next = n
            current_prev.next = current_next
            current_next.prev = current_prev

        while shift < 0:
            shift += 1

            current_next = n.next
            current_prev = n.prev
            new_prev = n.prev.prev

            new_prev.next = n
            n.prev = new_prev
            current_prev.prev = n
            n.next = current_prev
            current_next.prev = current_prev
            current_prev.next = current_next


def score(initial_list: list[Number]) -> int:
    start_value = 0
    shifts = [1000, 1000, 1000]

    # find start
    n = initial_list[0]
    for _ in range(len(initial_list)):
        if n.value == start_value:
            break
        n = n.next

    # collect values to score
    values = []
    for shift in shifts:
        shift = shift % len(initial_list)
        for _ in range(shift):
            n = n.next
        values.append(n.value)

    print(f"Scored values: {values}")
    return sum(values)


if __name__ == "__main__":
    main()
