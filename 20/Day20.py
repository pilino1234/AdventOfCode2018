import collections

from Point2D import Point2D as Pt


class Room:
    def __init__(self, up=None, down=None, left=None, right=None):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def print(self):
        top = "#" + ("-" if self.up else "#") + "#"
        middle = ("|" if self.left else "#") + "." + ("|" if self.right else "#")
        bottom = "#" + ("-" if self.down else "#") + "#"

        return top, middle, bottom

    def __repr__(self):
        return "Room {},{},{},{}".format(self.up, self.down, self.left, self.right)


def create_base_map(regex):
    area = {}
    pos = Pt(0, 0)  # type: Pt
    area[pos] = Room()

    latest_branches = collections.deque()

    for char in regex:
        current_room = area[pos]
        if char == "N":
            # If we are heading into a new room, create it
            if pos.above() not in area:
                next_room = Room()
            else:
                # Otherwise, get the next room from the map
                next_room = area[pos.above()]

            # Link together rooms
            current_room.up = next_room
            next_room.down = current_room

            # Move pos in the correct direction and store the new room there
            pos = pos.above()
            area[pos] = next_room
        elif char == "S":
            # If we are heading into a new room, create it
            if pos.below() not in area:
                next_room = Room()
            else:
                # Otherwise, get the next room from the map
                next_room = area[pos.below()]

            # Link together rooms
            current_room.down = next_room
            next_room.up = current_room

            # Move pos in the correct direction and store the new room there
            pos = pos.below()
            area[pos] = next_room
        elif char == "E":
            # If we are heading into a new room, create it
            if pos.right() not in area:
                next_room = Room()
            else:
                # Otherwise, get the next room from the map
                next_room = area[pos.right()]

            # Link together rooms
            current_room.right = next_room
            next_room.left = current_room

            # Move pos in the correct direction and store the new room there
            pos = pos.right()
            area[pos] = next_room
        elif char == "W":
            # If we are heading into a new room, create it
            if pos.left() not in area:
                next_room = Room()
            else:
                # Otherwise, get the next room from the map
                next_room = area[pos.left()]

            # Link together rooms
            current_room.left = next_room
            next_room.right = current_room

            # Move pos in the correct direction and store the new room there
            pos = pos.left()
            area[pos] = next_room
        elif char == "(":
            # Begin branch
            latest_branches.append(pos)
        elif char == "|":
            # Pop last pos from stack, then continue with new branch from there
            pos = latest_branches.pop()
            latest_branches.append(pos)
        elif char == ")":
            pos = latest_branches.pop()
        elif char in "^$":
            continue
        else:
            print("other char:", char)

    assert len(latest_branches) == 0

    # print_area_map(area)
    return area


def find_paths(base):
    distances = {}

    seen = set()
    to_visit = collections.deque([(Pt(0, 0), 0)])

    while to_visit:
        pos, current_distance = to_visit.popleft()

        # Add neighbours
        if base[pos].up and pos.above() not in seen:
            to_visit.append((pos.above(), current_distance+1))
        if base[pos].down and pos.below() not in seen:
            to_visit.append((pos.below(), current_distance+1))
        if base[pos].left and pos.left() not in seen:
            to_visit.append((pos.left(), current_distance+1))
        if base[pos].right and pos.right() not in seen:
            to_visit.append((pos.right(), current_distance+1))

        if pos not in distances or current_distance < distances[pos]:
            distances[pos] = current_distance

        seen.add(pos)

    max_distance = max(distances.items(), key=lambda d: distances[d[0]])  # type: tuple
    print("Max distance: {} to {}".format(max_distance[1], max_distance[0]))
    print("Number of rooms that are at least 1k doors away:",
          sum(dist >= 1000 for dist in distances.values()))


def print_area_map(area: dict):
    min_x = min(area.keys(), key=lambda point: point.x).x
    max_x = max(area.keys(), key=lambda point: point.x).x
    min_y = min(area.keys(), key=lambda point: point.y).y
    max_y = max(area.keys(), key=lambda point: point.y).y

    for row in range(min_y, max_y+1):
        top = ""
        middle = ""
        bottom = ""
        for col in range(min_x, max_x+1):
            p = Pt(col, row)
            t, m, b = area[p].print()
            top += t
            middle += m
            bottom += b
        print(top)
        print(middle)
        print(bottom)


if __name__ == '__main__':
    with open("input.txt") as file:
        input_regex = file.read().strip()

    elf_base = create_base_map(input_regex)
    find_paths(elf_base)
