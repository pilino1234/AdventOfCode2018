
def calculate_resulting_frequency(freqs):
    return sum(freqs)


def find_repeated_frequency(frequency_changes):
    found_freqs = {0}
    frequency = 0

    while True:
        for freq in frequency_changes:

            frequency += int(freq)

            if frequency in found_freqs:
                return frequency

            found_freqs.add(frequency)


if __name__ == '__main__':
    with open("input.txt") as file:
        input_frequencies = file.readlines()

    frequencies = [int(f.strip()) for f in input_frequencies]
    # frequencies = ["+1", "-2", "+3", "+1"]
    # frequencies = ["+1", "-1"]

    print(calculate_resulting_frequency(frequencies))
    print(find_repeated_frequency(frequencies))
