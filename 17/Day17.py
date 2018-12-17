from collections import deque, defaultdict, Counter
import re
import copy

from Point2D import Point2D as Pt


def parse_scan(lines):
    scan = defaultdict(lambda: " ")

    for line in lines:
        numbers = list(map(int, re.findall(r'-?\d+', line)))
        if line[0] == "x":
            x = numbers[0]
            for y in range(numbers[1], numbers[2]+1):
                scan[Pt(x, y)] = "#"
        elif line[0] == "y":
            y = numbers[0]
            for x in range(numbers[1], numbers[2]+1):
                scan[Pt(x, y)] = "#"

    return scan


def print_scan(scan):
    min_x = min(pos.x for pos in scan.keys()) - 1
    max_x = max(pos.x for pos in scan.keys()) + 1
    max_y = max(pos.y for pos in scan.keys())

    draw_area = scan.copy()

    for y in range(max_y + 1):
        for x in range(min_x, max_x + 1):
            if Pt(x, y) in draw_area:
                print(draw_area[Pt(x, y)], end="")
            else:
                print(" ", end="")
        print()
    print()


def simulate_water_flow(scan):
    min_x = min(pos.x for pos in scan.keys()) - 1
    max_x = max(pos.x for pos in scan.keys()) + 1
    min_y = min(pos.y for pos in scan.keys())
    max_y = max(pos.y for pos in scan.keys())

    # DO THIS AFTER FINDING MIN/MAX VALUES!
    scan[Pt(500, 0)] = "+"

    sources = deque([Pt(500, 0)])

    while sources:
        pos = sources.popleft()

        # If water is settled here, move on
        if scan[pos] == "~":
            continue

        # Follow the source downwards
        pos = pos.below()
        while pos.y <= max_y:
            # If we find air, keep dropping
            if scan[pos] == " ":
                scan[pos] = "|"
                pos = pos.below()
            # If we find clay or settled water, spread sideways
            elif scan[pos] == "#" or scan[pos] == "~":
                # Move back up one layer
                pos = pos.above()
                # Spread to the right
                right, r_overflows = flow_sideways(copy.copy(pos), Pt(1, 0), scan, sources)
                # Spread to the left
                left, l_overflows = flow_sideways(copy.copy(pos), Pt(-1, 0), scan, sources)

                for spread_x in range(left.x, right.x + 1):
                    scan[Pt(spread_x, pos.y)] = "|" if (r_overflows or l_overflows) else "~"

            # If we hit another falling stream, merge with it
            elif scan[pos] == "|":
                break

    counts = Counter(scan[Pt(x, y)] for x in range(min_x-1, max_x+1) for y in range(min_y, max_y+1))

    print(counts["~"] + counts["|"])
    print(counts["~"])


def flow_sideways(pos: Pt, direction: Pt, scan: dict, sources: deque):
    while True:
        current_cell = scan[pos]

        # If we hit a wall, move back one step and return "not overflowing"
        if current_cell == "#":
            pos -= direction
            return pos, False

        # If the cell below us is empty, we have overflow and a new source is created
        cell_below = scan[pos.below()]
        if cell_below == " ":
            sources.append(pos)
            return pos, True

        # If the current tile and the one below it are flowing, we have overflow but no
        # new source is created.
        if current_cell == "|" and cell_below == "|":
            return pos, True

        pos += direction


if __name__ == '__main__':
    with open("input.txt") as file:
        lines = [line.strip() for line in file.readlines()]

    scan = parse_scan(lines)

    simulate_water_flow(scan.copy())
