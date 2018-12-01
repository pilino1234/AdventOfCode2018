from itertools import cycle


def calculate_resulting_frequency(freqs):
    return sum(freqs)


def find_repeated_frequency(frequency_changes):
    found_freqs = {0}
    frequency = 0

    for freq in cycle(frequency_changes):
        frequency += freq

        if frequency in found_freqs:
            return frequency

        found_freqs.add(frequency)


if __name__ == '__main__':
    with open("input.txt") as file:
        input_frequencies = file.readlines()

    frequencies = [int(f.strip()) for f in input_frequencies]

    print(calculate_resulting_frequency(frequencies))
    print(find_repeated_frequency(frequencies))
