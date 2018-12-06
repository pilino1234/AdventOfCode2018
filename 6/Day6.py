from itertools import product
from collections import defaultdict


def stake_regions(coords):
    grid = {coord: num for num, coord in enumerate(coords)}
    regions = defaultdict(int)
    safe_region_size = 0        # Part 2
    out_of_range = set()

    max_x = max(coord[0] for coord in coords)
    max_y = max(coord[1] for coord in coords)

    for coord in product(range(max_x+1), range(max_y+1)):
        point_distances = sorted([(abs(point[0] - coord[0]) + abs(point[1] - coord[1]), id) for point, id in grid.items()])

        point_distance = sum(d[0] for d in point_distances)
        if point_distance < 10000:
            safe_region_size += 1

        if point_distances[0][0] != point_distances[1][0]:
            id = point_distances[0][1]
            regions[id] += 1

            if coord[0] in (0, max_x) or coord[1] in (0, max_y):
                out_of_range.add(id)

    return max(regions[region] for region in regions if region not in out_of_range), safe_region_size


if __name__ == '__main__':
    with open("input.txt") as file:
        coords = [tuple(map(int, line.strip().split(','))) for line in file.readlines()]

    unsafe_region_size, safe_region_size = stake_regions(coords)

    print("Part 1", unsafe_region_size)
    print("Part 2", safe_region_size)
