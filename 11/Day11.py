import numpy as np


def calc_power(grid_serial: int):
    def power_value(x: int, y: int) -> int:
        power_level = (x+11) * (x+11) * (y+1) + grid_serial * (x+11)
        hundreds_digit = power_level // 100 % 10
        return hundreds_digit - 5

    grid = np.fromfunction(power_value, (300, 300))

    return grid


def find_max_region(grid):
    max_x = max_y = 0
    max_sum = 0

    for x in range(299):
        for y in range(299):
            area_sum = grid[x:x+3, y:y+3].sum()
            if area_sum > max_sum:
                max_sum = area_sum
                max_x = x
                max_y = y

    return max_x+1, max_y+1, max_sum


def find_max_region2(grid):
    max_x = max_y = 0
    max_sum = 0
    max_size = 0

    for size in range(1, 300 + 1):
        for x in range(300 - size):
            for y in range(300 - size):
                area_sum = grid[x:x+size, y:y+size].sum()
                if area_sum > max_sum:
                    max_sum = area_sum
                    max_size = size
                    max_x = x
                    max_y = y

    return max_x+1, max_y+1, max_size, max_sum


# Cleaned
def find_max_region2(grid):
    max_x = max_y = 0
    max_sum = 0
    max_size = 0

    for size in range(1, 300 + 1):
        areas = sum(grid[x:x-size, y:y-size] for x in range(size) for y in range(size))
        maximum = int(areas.max())
        loc = np.where(areas == maximum)
        print(size, maximum, loc[0][0]+1, loc[1][0]+1)

    return max_x+1, max_y+1, max_size, max_sum


if __name__ == '__main__':
    GRID_SERIAL_NUMBER = 7400

    grid = calc_power(GRID_SERIAL_NUMBER)

#    x, y, max_sum = find_max_region(grid)
#    print("Part 1: {},{}".format(x, y))

#    x, y, size, max_sum = find_max_region2(grid)
#    print("Part 2: {},{},{}".format(x, y, size))

    find_max_region2(grid)

