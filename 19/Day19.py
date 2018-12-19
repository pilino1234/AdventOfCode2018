
import Day16


def parse_program(input_lines: list):
    pc_target = int(input_lines[0].split()[1])

    program_parts = []
    for line in input_lines[1:]:
        parts = line.split()
        program_parts.append(Day16.Instruction(parts[0], *list(map(int, parts[1:]))))

    return pc_target, program_parts


def addr(state: list, ins: Day16.Instruction):
    state[ins.C] = state[ins.A] + state[ins.B]


def addi(state: list, ins: Day16.Instruction):
    state[ins.C] = state[ins.A] + ins.B


def mulr(state: list, ins: Day16.Instruction):
    state[ins.C] = state[ins.A] * state[ins.B]


def muli(state: list, ins: Day16.Instruction):
    state[ins.C] = state[ins.A] * ins.B


def banr(state: list, ins: Day16.Instruction):
    state[ins.C] = state[ins.A] & state[ins.B]


def bani(state: list, ins: Day16.Instruction):
    state[ins.C] = state[ins.A] & ins.B


def borr(state: list, ins: Day16.Instruction):
    state[ins.C] = state[ins.A] | state[ins.B]


def bori(state: list, ins: Day16.Instruction):
    state[ins.C] = state[ins.A] | ins.B


def setr(state: list, ins: Day16.Instruction):
    state[ins.C] = state[ins.A]


def seti(state: list, ins: Day16.Instruction):
    state[ins.C] = ins.A


def gtir(state: list, ins: Day16.Instruction):
    state[ins.C] = int(ins.A > state[ins.B])


def gtri(state: list, ins: Day16.Instruction):
    state[ins.C] = int(state[ins.A] > ins.B)


def gtrr(state: list, ins: Day16.Instruction):
    state[ins.C] = int(state[ins.A] > state[ins.B])


def eqir(state: list, ins: Day16.Instruction):
    state[ins.C] = int(ins.A == state[ins.B])


def eqri(state: list, ins: Day16.Instruction):
    state[ins.C] = int(state[ins.A] == ins.B)


def eqrr(state: list, ins: Day16.Instruction):
    state[ins.C] = int(state[ins.A] == state[ins.B])


def run_program(instructions, pc_register=None):
    registers = [0] * 6

    dispatch = {
        "addr": addr,
        "addi": addi,
        "mulr": mulr,
        "muli": muli,
        "banr": banr,
        "bani": bani,
        "borr": borr,
        "bori": bori,
        "setr": setr,
        "seti": seti,
        "gtir": gtir,
        "gtri": gtri,
        "gtrr": gtrr,
        "eqir": eqir,
        "eqri": eqri,
        "eqrr": eqrr
    }

    pc = 0

    while 0 <= pc < len(instructions):
        ins = instructions[pc]
        registers[pc_register] = pc

        dispatch[ins.opcode](registers, ins)

        pc = registers[pc_register]
        pc += 1

    return registers


def part2(number: int) -> int:
    factors = []

    for n in range(1, number+1):
        if number % n == 0:  # If we can divide evenly, it's a factor
            factors.append(n)

    return sum(factors)


if __name__ == "__main__":
    with open("input.txt") as file:
        lines = [line.strip() for line in file.readlines()]

    pc_binding, program = parse_program(lines)

    final_registers = run_program(program, pc_binding)
    print("Value in reg0 after running:", final_registers[0])

    # See analysis.txt for how this works
    sum_of_factors = part2(10551306)
    print("Value in reg0 after running part 2:", sum_of_factors)
