
class Cart:
    def __init__(self, x: int, y: int, direction: int, id: int):
        self.x = x
        self.y = y
        self.direction = direction

        self.dead = False
        self.id = id

        self.next_intersection = -1  # -1 = left, 0 = straight, 1 = right

    def kill(self):
        self.dead = True

    def intersection(self):
        self.direction += self.next_intersection
        self.direction %= 4

        self.next_intersection += 1
        if self.next_intersection > 1:
            self.next_intersection -= 3

    def turn(self, new_segment: str):
        if self.dead:
            return

        if new_segment in "|-":
            return
        elif new_segment == "\\":
            if self.direction == 0 or self.direction == 2:
                self.direction = (self.direction - 1) % 4
            elif self.direction == 1 or self.direction == 3:
                self.direction = (self.direction + 1) % 4
        elif new_segment == "/":
            if self.direction == 0 or self.direction == 2:
                self.direction = (self.direction + 1) % 4
            elif self.direction == 1 or self.direction == 3:
                self.direction = (self.direction - 1) % 4
        elif new_segment == "+":
            self.intersection()

    def move(self):
        if self.dead:
            return

        if self.direction == 0:
            self.y -= 1
        elif self.direction == 2:
            self.y += 1
        elif self.direction == 3:
            self.x -= 1
        elif self.direction == 1:
            self.x += 1

    def __repr__(self):
        return "Cart {id} @ ({x},{y}) facing {dir}".format(id=self.id, x=self.x, y=self.y,
                                                           dir=self.direction)

    def __eq__(self, other):
        return other.x == self.x and other.y == self.y


def find_carts(track):
    carts = []

    replacements = {
        "^": "|",
        "v": "|",
        "<": "-",
        ">": "-"
    }

    directions = {
        "^": 0,
        ">": 1,
        "v": 2,
        "<": 3,
    }

    for row, line in enumerate(track):  # type: (int, str)
        for col, letter in enumerate(line):  # type: (int, str)
            if letter in "^v<>":
                carts.append(Cart(col, row, directions[letter], len(carts)))
                new_line = track[row][:col] + replacements[letter] + track[row][col+1:]
                track[row] = new_line

    return track, carts


def tick(track, carts):
    carts = sorted(carts, key=lambda c: c.y)

    first_collision = True
    crashes = []
    ticks = 0

    while len(crashes) < len(carts)-1:
        for cart in carts:
            if cart.dead:
                continue
            # Move cart
            cart.move()

            # Check if we ran into something
            for other_cart in carts:
                if cart is other_cart:
                    continue
                if other_cart.dead:
                    continue
                if cart == other_cart:
                    print("Collision:", cart, "and", other_cart)
                    cart.kill()
                    other_cart.kill()
                    crashes.append(cart)
                    crashes.append(other_cart)
                    if first_collision:
                        print("First collision ({},{})".format(cart.x, cart.y))
                        first_collision = False
                    break

            # Update cart direction
            track_segment = track[cart.y][cart.x]
            cart.turn(track_segment)

        ticks += 1

        if ticks % 500 == 0:
            print("Remaining carts:", sum(not cart.dead for cart in carts), "at tick", ticks)
        #print("Crashed carts ({}): {}".format(len(crashes), crashes))

    last_cart = [cart for cart in carts if not cart.dead]
    print(last_cart)
    print_track(track, carts)


def print_track(track, carts):
    rev_directions = {
        0: "^",
        1: ">",
        2: "v",
        3: "<"
    }

    track_copy = track[:]
    for cart in carts:
        if not cart.dead:
            # track_copy[cart.y] = track_copy[cart.y][:cart.x] + str(cart.id) + track_copy[cart.y][cart.x+1:]
            track_copy[cart.y] = track_copy[cart.y][:cart.x] + rev_directions[cart.direction] + track_copy[cart.y][cart.x+1:]

    print("".join(track_copy))


if __name__ == '__main__':
    with open("input.txt") as file:
        lines = file.readlines()

    track, carts = find_carts(lines)

    tick(track, carts)


