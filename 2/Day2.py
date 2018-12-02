from collections import Counter
from itertools import combinations


def count_twice(box_id: str):
    letter_counts = Counter(box_id)
    return any([letter_count == 2 for letter_count in letter_counts.values()])


def count_thrice(box_id: str):
    letter_counts = Counter(box_id)
    return any([letter_count == 3 for letter_count in letter_counts.values()])


def find_similar(box_ids: list):
    for pair in combinations(box_ids, 2):
        if sum([l1 != l2 for l1, l2 in zip(*pair)]) == 1:  # if there is exactly 1 differing letter
            return "".join([l1 for l1, l2 in zip(*pair) if l1 == l2])


if __name__ == '__main__':
    with open("input.txt") as file:
        box_ids = file.readlines()

    box_ids = [box_id.strip() for box_id in box_ids]

    twice_count = sum([count_twice(box_id) for box_id in box_ids])
    thrice_count = sum([count_thrice(box_id) for box_id in box_ids])

    print(twice_count * thrice_count)

    print(find_similar(box_ids))

