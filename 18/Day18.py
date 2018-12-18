from collections import Counter

from Point2D import Point2D as Pt


def parse_area(lines):
    area = {}

    for y, line in enumerate(lines):
        for x, acre in enumerate(line):
            area[Pt(x, y)] = acre

    return area


def print_area(area):
    max_x = max(pos.x for pos in area.keys()) + 1
    max_y = max(pos.y for pos in area.keys())

    draw_area = area.copy()

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if Pt(x, y) in draw_area:
                print(draw_area[Pt(x, y)], end="")
            else:
                print(" ", end="")
        print()
    print()


def change_area(area):
    new_area = {}

    for pos in area:  # type: Pt
        current_state = area[pos]
        neighbour_counts = Counter(area[nb] for nb in pos.nb8() if nb in area)

        if current_state == ".":
            if neighbour_counts["|"] >= 3:
                new_area[pos] = "|"
            else:
                new_area[pos] = "."
        elif current_state == "|":
            if neighbour_counts["#"] >= 3:
                new_area[pos] = "#"
            else:
                new_area[pos] = "|"
        elif current_state == "#":
            if neighbour_counts["#"] >= 1 and neighbour_counts["|"] >= 1:
                new_area[pos] = "#"
            else:
                new_area[pos] = "."

    return new_area


if __name__ == '__main__':
    with open("input.txt") as file:
        lines = [line.strip() for line in file.readlines()]

    area = parse_area(lines)

    seen = []
    for i in range(1, 1000000000+1):
        area = change_area(area)

        # Part 1:
        if i == 10:
            print_area(area)
            counts = Counter(area[pos] for pos in area)
            print("(Part 1) Total resource value after 10 minutes:", counts["|"] * counts["#"])

        # Part 2
        if area in seen:
            minute = seen.index(area) + 1
            print("Repeated area at minute", i)
            print("First seen at minute", minute)
            print("Period: {} minutes".format(i - minute))
            repeat_begin = minute  # = 410
            period = i - minute  # = 84

            # Calculate final result mod
            final_mod = 1000000000 % period  # = 76

            # Look up the result in the stored values
            final_index = repeat_begin
            while final_index % period != final_mod:
                final_index += 1
            final_area = seen[final_index-1]
            counts = Counter(final_area[pos] for pos in final_area)
            print("(Part 2) Total resource value after lots of minutes:", counts["|"] * counts["#"])

            break
        seen.append(area)
