
def parse_nodes(numbers: list):
    child_count, metadata_count = numbers[:2]
    numbers = numbers[2:]

    metadata_total = 0
    values = []

    for n in range(child_count):
        total, value, numbers = parse_nodes(numbers)
        metadata_total += total
        values.append(value)

    metadata_total += sum(numbers[:metadata_count])

    if child_count == 0:
        return metadata_total, sum(numbers[:metadata_count]), numbers[metadata_count:]
    else:
        return (metadata_total,
                sum(values[k - 1] for k in numbers[:metadata_count] if 0 < k <= len(values)),
                numbers[metadata_count:])


if __name__ == '__main__':
    with open("input.txt") as file:
        numbers = list(map(int, file.read().split()))

    metadata, value, _ = parse_nodes(numbers)
    print(metadata)
    print(value)

