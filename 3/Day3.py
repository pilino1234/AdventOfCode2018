import re
from collections import namedtuple
from itertools import product

import numpy as np

Claim = namedtuple('Claim', ['id', 'x', 'y', 'width', 'height'])


def parse_claims(raw_claims: list):
    return {Claim(*data) for data in map(lambda s: map(int, re.findall(r'-?\d+', s)), raw_claims)}


def find_overlapping(claims):
    fabric = np.zeros(shape=(1000, 1000), dtype=int)

    for claim in claims:
        fabric[claim.y:claim.y+claim.height, claim.x:claim.x+claim.width] += 1

    return fabric


def find_non_overlapping(claims):
    fabric = np.zeros(shape=(1000, 1000), dtype=int)

    non_overlapping = {int(i) for i in claims.keys()}

    for claim in claims:
        overlaps = set()
        for coord in product([y for y in range(claim.y, claim.y + claim.height)],
                             [x for x in range(claim.x, claim.x + claim.width)]):
            val = fabric[coord]
            if val != 0:
                overlaps.add(val)
                overlaps.add(claim.id)

        if overlaps:
            for i in overlaps:
                try:
                    non_overlapping.remove(i)
                except KeyError:
                    pass
        fabric[claim.y:claim.y + claim.height, claim.x:claim.x + claim.width] = claim.id
    return non_overlapping


def find_non_overlapping2(claims, fabric):
    for claim in claims:
        if np.all(fabric[claim.y:claim.y + claim.height, claim.x:claim.x + claim.width] == 1):
            return claim.id


if __name__ == "__main__":
    with open("input.txt") as file:
        in_data = file.readlines()

    in_data = [data.strip() for data in in_data]

    claims = parse_claims(in_data)

    fabric = find_overlapping(claims)
    print("Overlaps: {}".format((fabric >= 2).sum()))

# First, naive solution. Runtime ~20ms
#    start = time.time()
#    non_overlapping = find_non_overlapping(claims)
#    stop = time.time()
#    print(non_overlapping)
#    print(stop - start)

# Second solution (using np.all). Runtime ~<1ms
    non_overlapping = find_non_overlapping2(claims, fabric)
    print(non_overlapping)
