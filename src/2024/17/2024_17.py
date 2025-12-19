import dataclasses
import math
import re

from src.utils.data import load_data
from src.utils.submission import submit_or_print


@dataclasses.dataclass(frozen=True)
class State:
    position: int
    register_a: int
    register_b: int
    register_c: int


def main(debug: bool) -> None:
    input_data = load_data(debug)
    program, init_registers = parse_input(input_data)
    print(f"Registers: {init_registers}")
    print(f"Program ({len(program)}): {program}")

    # part 1
    output = run_program(program, init_registers)
    result_part1 = ",".join(map(str, output))

    # part 2
    init_value = 1  # max checked: 819,700,000
    while True:
        registers = init_registers.copy()
        registers["A"] = init_value
        output = run_program(program, registers)
        if output is not None:
            print(init_value, output)
            if len(output) == len(program) and program == output:
                break
            elif program[-len(output) :] == output:
                init_value *= 8
            else:
                init_value += 1
        else:
            init_value += 1
    result_part2 = init_value
    print(result_part2)

    submit_or_print(result_part1, result_part2, debug)


def parse_input(input_data):
    s = input_data.split("\n\n")
    registers = {}
    for line in s[0].splitlines():
        m = re.match(r"Register ([A-Z]): (\d+)", line)
        registers[m.group(1)] = int(m.group(2))
    program = list(map(int, s[1].split(":", 1)[1].strip().split(",")))
    return program, registers


def run_program(program, registers, check_output=False):
    position = 0
    output = []
    states = set()
    registers = registers.copy()

    while position < len(program):
        state = State(position, registers["A"], registers["C"], registers["C"])
        if state in states:
            return None
        states.add(state)

        opcode = program[position]
        operand = program[position + 1]

        if opcode == 0:  # adv
            # print(f"A changed to floor(A / 2^{resolve_combo_str(operand)})")
            registers["A"] = division(operand, registers)

        elif opcode == 1:  # bxl
            # print(f"B changed to xor(B, {operand})")
            registers["B"] = registers["B"] ^ operand

        elif opcode == 2:  # bst
            # print(f"B changed to {resolve_combo_str(operand)} % 8")
            registers["B"] = combo_operand(operand, registers) % 8

        elif opcode == 3:  # jnz
            if registers["A"] != 0:
                # print(f"Position changed from {position} to {operand}")
                position = operand - 2

        elif opcode == 4:  # bxc
            # print("B changed to xor(B, C)")
            registers["B"] = registers["B"] ^ registers["C"]

        elif opcode == 5:  # out
            # print(f"Output {resolve_combo_str(operand)} % 8")
            output.append(combo_operand(operand, registers) % 8)
            if check_output:
                last_output_pos = len(output) - 1
                if output[last_output_pos] != program[last_output_pos]:
                    return output
        elif opcode == 6:  # bdv
            # print(f"B changed to floor(A / 2^{resolve_combo_str(operand)})")
            registers["B"] = division(operand, registers)

        elif opcode == 7:  # cdv
            # print(f"C changed to floor(A / 2^{resolve_combo_str(operand)})")
            registers["C"] = division(operand, registers)

        position += 2
    return output


def division(operand, registers):
    numerator = registers["A"]
    denominator = math.pow(2, combo_operand(operand, registers))
    return math.floor(numerator / denominator)


def resolve_combo_str(operand):
    if operand < 4:
        return operand
    elif operand == 4:
        return "A"
    elif operand == 5:
        return "B"
    elif operand == 6:
        return "C"
    else:
        raise Exception("Invalid combo operand 7!")


def combo_operand(operand, registers):
    if operand < 4:
        return operand
    elif operand == 4:
        return registers["A"]
    elif operand == 5:
        return registers["B"]
    elif operand == 6:
        return registers["C"]
    else:
        raise Exception("Invalid combo operand 7!")


if __name__ == "__main__":
    debug_mode = True
    debug_mode = False
    main(debug_mode)
