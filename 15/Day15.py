import itertools
from collections import defaultdict, deque

from Point2D import Point2D as Pt


class Unit:
    def __init__(self, x, y, name):
        self.pos = Pt(x, y)
        self.type = name

        self.health = 200
        self.atk = 3
        self.dead = False

    def move(self, pos):
        self.pos = pos

    def attack(self, attacker):
        self.health -= attacker.atk

        if self.health <= 0:
            self.dead = True

            if self.type == "elf":
                raise ElfDiedException

    def __repr__(self):
        return "{type} @ ({pos}) with {health} HP".format(type=self.type, pos=self.pos,
                                                          health=self.health)

    def __eq__(self, other):
        return self.pos == other.pos and self.dead == other.dead


class ElfDiedException(BaseException):
    __cause__ = "Elf died in combat. This is unacceptable."


def parse_map(lines, elf_power=3):
    area = defaultdict(bool)
    units = []

    for y, line in enumerate(lines):
        for x, letter in enumerate(line):
            area[Pt(x, y)] = letter == "#"

            if letter == "G":
                units.append(Unit(x, y, "goblin"))
            elif letter == "E":
                elf = Unit(x, y, "elf")
                elf.atk = elf_power
                units.append(elf)

    return area, units


def combat(area, units, part2=False):

    enemy_names = {
        "goblin": "elf",
        "elf": "goblin"
    }

    combat_round = 0

    while True:
        #print("Round", combat_round)
        #print_map(area, units)
        #store_map(area, units)

        # Sort units
        units = sorted(units, key=lambda u: (u.pos.y, u.pos.x))

        # Each unit has its turn
        for unit in units:
            if unit.dead:
                continue

            # Find possible targets
            enemies = [u for u in units if u.type == enemy_names[unit.type] and not u.dead]
            occupied = set(u.pos for u in units if not u.dead and u != unit)

            # If no targets found, combat is over.
            if not enemies:
                print("No more enemies found, combat is over.")
                return combat_round

            # Find positions in range of targets
            in_range_positions = []
            for enemy in enemies:
                in_range_positions.extend(pt for pt in enemy.pos.nb4() if not area[pt] and pt not in occupied)

            # If not in range, move
            if unit.pos not in in_range_positions:
                # Pick in-range position that is reachable in fewest steps
                next_pos = find_move(unit.pos, in_range_positions, area, units)

                if next_pos:
                    unit.move(next_pos)

            # Attack
            # Find all enemies in range
            opponents = [enemy for enemy in enemies if enemy.pos in unit.pos.nb4()]

            if opponents:

                # Select adjacent target with fewest hit points (applying reading order if tied)
                target = min(opponents, key=lambda o: (o.health, o.pos.y, o.pos.x))

                try:
                    target.attack(attacker=unit)
                except ElfDiedException as e:
                    if part2:
                        raise e

        combat_round += 1


def find_move(start, targets, area, units):
    occupied = {unit.pos for unit in units if not unit.dead}
    visit_q = deque([(start, 0)])
    # Remember which nodes we have visited
    seen = set()
    # Stores the shortest path to any position as the distance to get there and the previous node to get there
    paths = {start: (0, None)}

    while visit_q:
        pos, distance = visit_q.popleft()
        for neighbour in pos.nb4():
            if area[neighbour] or neighbour in occupied or neighbour in seen:
                continue
            if neighbour not in paths or paths[neighbour] > (distance + 1, pos):
                paths[neighbour] = (distance + 1, pos)
            if not any(neighbour == visit[0] for visit in visit_q):
                visit_q.append((neighbour, distance + 1))
        seen.add(pos)

    # Determine the closest target positions. The sorting is necessary so that we get the results in reading order.
    try:
        min_dist, closest_pos = min((distance, pos) for pos, (distance, prev) in sorted(paths.items(), key=lambda i: (i[0].y, i[0].x)) if pos in targets)
    except ValueError:
        return

    # Go backwards through the path to the closest target position to find the next step
    while paths[closest_pos][0] > 1:
        closest_pos = paths[closest_pos][1]

    return closest_pos


def print_map(area, units):
    max_x = max(pos.x for pos in area.keys())
    max_y = max(pos.y for pos in area.keys())

    symbols = {
        True: "#",
        False: " ",
        "E": "E",
        "G": "G"
    }

    draw_area = area.copy()
    draw_area.update({unit.pos: unit.type.upper()[0] for unit in units if not unit.dead})

    for line in range(max_y + 1):
        print("".join(symbols[draw_area.get(Pt(x, line), " ")] for x in range(max_x + 1)))


if __name__ == '__main__':
    with open("input.txt") as file:
        lines = [line.strip() for line in file.readlines()]

    area, units = parse_map(lines)

    rounds = combat(area, units)
    print_map(area, units)

    total_hp_remaining = sum(unit.health for unit in units if not unit.dead)

    print("Total remaining HP:", total_hp_remaining)
    print("Total rounds:", rounds)
    print("Result:", total_hp_remaining * rounds)

    # ------- Part 2 -------
    for elf_power in itertools.count(4):
        print("Testing elf power:", elf_power)
        try:
            area, units = parse_map(lines, elf_power)
            rounds = combat(area, units, part2=True)
        except ElfDiedException:
            continue
        else:  # Runs once the try block completes without error
            total_hp_remaining = sum(unit.health for unit in units if not unit.dead)

            print("Total remaining HP:", total_hp_remaining)
            print("Total rounds:", rounds)
            print("Elf attack power needed:", elf_power)
            print("Result:", total_hp_remaining * rounds)
            break
