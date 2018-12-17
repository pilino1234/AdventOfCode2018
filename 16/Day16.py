import re
import copy
from collections import namedtuple, defaultdict


class State:
    def __init__(self, reg0, reg1, reg2, reg3):
        self.reg0 = reg0
        self.reg1 = reg1
        self.reg2 = reg2
        self.reg3 = reg3

    @property
    def values(self):
        return self.reg0, self.reg1, self.reg2, self.reg3

    def __getitem__(self, item):
        if item == 0:
            return self.reg0
        elif item == 1:
            return self.reg1
        elif item == 2:
            return self.reg2
        elif item == 3:
            return self.reg3

    def __setitem__(self, key, value):
        if key == 0:
            self.reg0 = value
        elif key == 1:
            self.reg1 = value
        elif key == 2:
            self.reg2 = value
        elif key == 3:
            self.reg3 = value

    def __repr__(self):
        return "".join("[{}]: {} ".format(*(idx, self[idx])) for idx in range(4))

    def __eq__(self, other):
        return self.reg0 == other.reg0 and self.reg1 == other.reg1 \
               and self.reg2 == other.reg2 and self.reg3 == other.reg3


Instruction = namedtuple('Instruction', ['opcode', 'A', 'B', 'C'])
Sample = namedtuple('Sample', ['before', 'instruction', 'after'])


def parse_samples(lines):
    samples = []

    for idx in range(0, len(lines), 4):
        before = lines[idx]
        ins = lines[idx+1]
        after = lines[idx+2]

        before_state = State(*list(map(int, re.findall(r'-?\d+', before))))
        ins = Instruction(*list(map(int, re.findall(r'-?\d+', ins))))
        after_state = State(*list(map(int, re.findall(r'-?\d+', after))))

        samples.append(Sample(before_state, ins, after_state))
    return samples


def parse_program(lines):
    return [Instruction(*list(map(int, re.findall(r'-?\d+', line)))) for line in lines]


def addr(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = state[ins.A] + state[ins.B]
    return output


def addi(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = state[ins.A] + ins.B
    return output


def mulr(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = state[ins.A] * state[ins.B]
    return output


def muli(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = state[ins.A] * ins.B
    return output


def banr(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = state[ins.A] & state[ins.B]
    return output


def bani(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = state[ins.A] & ins.B
    return output


def borr(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = state[ins.A] | state[ins.B]
    return output


def bori(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = state[ins.A] | ins.B
    return output


def setr(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = state[ins.A]
    return output


def seti(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = ins.A
    return output


def gtir(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = int(ins.A > state[ins.B])
    return output


def gtri(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = int(state[ins.A] > ins.B)
    return output


def gtrr(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = int(state[ins.A] > state[ins.B])
    return output


def eqir(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = int(ins.A == state[ins.B])
    return output


def eqri(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = int(state[ins.A] == ins.B)
    return output


def eqrr(state: State, ins: Instruction):
    output = copy.copy(state)
    output[ins.C] = int(state[ins.A] == state[ins.B])
    return output


def reconstruct_from_samples(samples):
    ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

    sample_matches = defaultdict(list)
    mappings = defaultdict(set)

    for idx, sample in enumerate(samples):
        for op in ops:
            output = op(sample.before, sample.instruction)
            if output == sample.after:
                sample_matches[idx].append(op)
                mappings[sample.instruction.opcode].add(op)

    print("Samples matching >= 3 operations:", sum(len(matches) >= 3 for matches in sample_matches.values()))

    while not all(len(matches) == 1 for matches in mappings.values()):
        for opcode, matches in mappings.items():
            # If we only have 1 mapping, we have resolved this opcode/instruction pair
            if len(matches) == 1:
                # Remove the instructions from all other opcode matchings
                to_remove = next(iter(matches))
                for op_ in mappings:
                    if op_ == opcode:
                        continue
                    if to_remove in mappings[op_]:
                        mappings[op_].remove(to_remove)

    return {opcode: next(iter(matches)) for opcode, matches in mappings.items()}


def execute_program(mappings, program):
    state = State(0, 0, 0, 0)

    for instruction in program:  # type: Instruction
        func = mappings[instruction.opcode]
        state = func(state, instruction)

    return state


if __name__ == '__main__':
    with open('input_pt1.txt') as file:
        lines = [line.strip() for line in file.readlines()]

    samples = parse_samples(lines)
    print("Found {} samples".format(len(samples)))

    instruction_set = reconstruct_from_samples(samples)

    with open("input_pt2.txt") as file:
        lines = [line.strip() for line in file.readlines()]
    program = parse_program(lines)

    final_state = execute_program(instruction_set, program)
    print("Register 0 value:", final_state.reg0)
