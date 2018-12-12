from collections import defaultdict


def parse_rules(lines):
    growth_rules = {}

    for line in lines:  # type: str
        condition, result = line.split(" => ")
        cond = tuple(True if letter == "#" else False for letter in condition)
        growth_rules[cond] = True if result == "#" else False

    return growth_rules


def parse_pots(initial_state):
    pots = defaultdict(bool)

    for pos, pot in enumerate(initial_state):
        if pot == "#":
            pots[pos] = True

    return pots


def simulate_growth(pots, rules, generations=20):
    prev_state = pots.copy()
    next_state = defaultdict(bool)

    print_pots(pots, 0)

    # Part 2
    # pcount = count_pots(pots)

    for i in range(1, generations+1):
        for pos in range(min(prev_state)-1, max(prev_state)+2):
            # print(pos)
            surrounding_state = tuple([True if prev_state[n_pos] else False for n_pos in range(pos-2, pos+3)])
            if surrounding_state in rules:
                next_state[pos] = rules[surrounding_state]

        prev_state = next_state
        next_state = defaultdict(bool)
        print_pots(prev_state, i)

        # Part 2
        # count = count_pots(prev_state)
        # print("{}: {}, delta: {}".format(i, count, count-pcount))
        # pcount = count

    return prev_state


def print_pots(pots, generation):
    pots_copy = pots.copy()
    print("{:2}: ".format(generation), end="")
    for pos in range(min(pots_copy)-1, max(pots_copy)+2):
        if pots_copy[pos]:
            print("#", end="")
        else:
            print(".", end="")
    print()


def count_pots(pots):
    return sum(pos for pos in range(min(pots), max(pots)+1) if pots[pos])


if __name__ == '__main__':
    with open("input.txt") as file:
        lines = [line.strip() for line in file.readlines()]

    pots = parse_pots(initial_state=lines[0][15:])

    rules = parse_rules(lines[2:])

    final_state = simulate_growth(pots, rules)
    print(count_pots(final_state))

    # Part 2 (uncomment lines in simulate_growth() and run with a high number of generations)
    # We see that the sum of the pot numbers increases by 52 every generation after 109,
    # so we do some simple maths from there
    # simulate_growth(pots, rules, 50000000000)
    DELTA = 52
    generations_remaining = 50000000000 - 109
    total = 6587 + generations_remaining * DELTA
    print(total)
