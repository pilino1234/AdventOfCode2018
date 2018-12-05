import string


def react(polymer: str):
    length_before = len(polymer)
    length_after = 0
    while length_before > length_after:
        length_before = len(polymer)
        for char in string.ascii_lowercase:
            polymer = polymer.replace('{}{}'.format(char, char.upper()), "")
            polymer = polymer.replace('{}{}'.format(char.upper(), char), "")
        length_after = len(polymer)
    return polymer


def optimize(polymer: str):
    lengths = {}

    for letter in set(polymer.lower()):
        test = polymer.replace(letter, "")
        test = test.replace(letter.upper(), "")
        lengths[letter] = len(react(test))

    shortest = min(lengths, key=lengths.get)
    return lengths[shortest]


if __name__ == '__main__':
    with open("input.txt") as file:
        polymer = file.read().strip()

    test = "dabAcCaCBAcCcaDA"

    print(len(react(polymer)))

    print(optimize(polymer))

