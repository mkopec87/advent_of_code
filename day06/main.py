from collections import deque


def main():
    with open("input.txt") as f:
        line = [line.strip() for line in f.readlines()][0]
    print(f"line with {len(line)} characters read")

    print(f"Result part 1: {find_message_start(line, 4)}")
    print(f"Result part 2: {find_message_start(line, 14)}")


def find_message_start(line: str, buffer_size: int) -> int:
    buffer_queue = deque()
    for i, char in enumerate(line):
        buffer_queue.append(char)
        if len(buffer_queue) > buffer_size:
            buffer_queue.popleft()
        if len(set(buffer_queue)) == buffer_size:
            return i + 1


if __name__ == "__main__":
    main()
