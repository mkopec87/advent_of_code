from numpy import product

INPUT_TXT = "input.txt"


# INPUT_TXT = "input-small.txt"


def parse_binary(binary):
    print("\t parsing binary: ", binary)
    version_number = int(binary[:3], 2)
    binary = binary[3:]
    packet_type = int(binary[:3], 2)
    binary = binary[3:]

    print("\t version:", version_number)
    print("\t type:", packet_type)

    if packet_type == 4:
        number_str = ""
        while int(binary[0], 2) == 1:
            number_str += binary[1:5]
            binary = binary[5:]
        number_str += binary[1:5]
        binary = binary[5:]
        value = int(number_str, 2)
        print("\t literal:", value)

    else:
        length_type = int(binary[0], 2)
        binary = binary[1:]
        print("\t length type:", length_type)

        values = []

        if length_type == 0:
            total_length = int(binary[:15], 2)
            binary = binary[15:]
            print("\t total_length:", total_length)

            to_parse = binary[:total_length]
            while to_parse:
                to_parse, value = parse_binary(to_parse)
                values.append(value)
            binary = binary[total_length:]

        elif length_type == 1:
            total_packets = int(binary[:11], 2)
            binary = binary[11:]
            print("\t total_packets:", total_packets)

            for _ in range(total_packets):
                binary, value = parse_binary(binary)
                values.append(value)

        if packet_type == 0:
            value = sum(values)
        elif packet_type == 1:
            value = product(values)
        elif packet_type == 2:
            value = min(values)
        elif packet_type == 3:
            value = max(values)
        elif packet_type == 5:
            assert len(values) == 2
            value = 1 if values[0] > values[1] else 0
        elif packet_type == 6:
            assert len(values) == 2
            value = 1 if values[0] < values[1] else 0
        elif packet_type == 7:
            assert len(values) == 2
            value = 1 if values[0] == values[1] else 0

    return binary, value


def parse_hex(line):
    print(line)
    binary = bin(int(line, 16))[2:].zfill(len(line) * 4)
    print("\t", binary)
    return parse_binary(binary)


def main():
    with open(INPUT_TXT) as f:
        lines = [line.strip() for line in f.readlines()]
    print(f"{len(lines)} lines read")

    for line in lines:
        print(parse_hex(line))

    result_part1 = 0
    result_part2 = 0

    print()
    print("##########")
    print(f"Result part 1: {result_part1}")
    print(f"Result part 2: {result_part2}")


if __name__ == "__main__":
    main()
