import re
from collections import defaultdict
from operator import itemgetter


def parse_points(lines: list):
    return [list(map(int, re.findall(r'-?\d+', line))) for line in lines]


def simulate(points: list):
    max_y = max(points, key=itemgetter(1))[1]
    min_y = min(points, key=itemgetter(1))[1]

    seconds = 0

    while abs(max_y - min_y) > 10:
        seconds += 1

        # Update positions
        for p in points:
            p[0] += p[2]
            p[1] += p[3]

        max_y = max(points, key = itemgetter(1))[1]
        min_y = min(points, key = itemgetter(1))[1]

    print_points(points)
    return seconds


def print_points(points: list):
    points_map = defaultdict(int)

    max_x = max(points, key=itemgetter(0))[0]
    min_x = min(points, key=itemgetter(0))[0]

    max_y = max(points, key = itemgetter(1))[1]
    min_y = min(points, key = itemgetter(1))[1]

    for p in points:
        points_map[(p[0], p[1])] = 1

    for line in range(min_y, max_y + 1):
        for col in range(min_x, max_x + 1):
            if (col, line) in points_map:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


if __name__ == '__main__':
    with open("input.txt") as file:
        lines = [line.strip() for line in file.readlines()]

    points = parse_points(lines)

    print(simulate(points))
