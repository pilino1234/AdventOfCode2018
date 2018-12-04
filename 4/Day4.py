import datetime
import re
from collections import defaultdict


def parse_guards(data: list) -> dict:
    sorted_data = sorted(data, key = lambda s: datetime.datetime(*map(int, re.findall(r'\d+', s[0:18]))))

    guards = defaultdict(list)

    current_guard = None
    for line in sorted_data:
        time = datetime.datetime(*map(int, re.findall(r'\d+', line[0:18])))

        if "#" in line:
            guard_id = re.findall(r'#\d+', line)
            guard_id = int(guard_id[0].strip('#'))
            current_guard = guard_id

        guards[current_guard].append((time, line[18:]))

    return guards


def get_longest_sleeping(guards: dict) -> int:
    sleeptimes = defaultdict(int)

    for guard, events in guards.items():
        asleep_since = None
        for event in events:
            if "falls asleep" in event[1]:
                asleep_since = event[0]
            elif "wakes up" in event[1]:
                sleeptimes[guard] += int((event[0] - asleep_since).total_seconds() / 60)

    return max(sleeptimes, key=sleeptimes.get)


def get_most_common_minute(guards, guard_id):
    events = guards[guard_id]

    minutes = defaultdict(int)

    asleep = None  # type: datetime.datetime
    for event in events:
        if "falls asleep" in event[1] and asleep is None:
            asleep = event[0]
        elif "wakes up" in event[1] and asleep is not None:
            while asleep < event[0]:
                minutes[asleep.hour * 60 + asleep.minute] += 1
                asleep += datetime.timedelta(minutes=1)
            asleep = None

    if minutes:
        minute = max(minutes, key=minutes.get)
        count = minutes[minute]
        return minute, count
    return 0, 0  # Some guards never sleep


def part2(guards):
    guard_minutes = {}

    for guard in guards:
        minute, count = get_most_common_minute(guards, guard)
        guard_minutes[guard] = (minute, count)

    # Find the guard id who is most commonly asleep at some minute
    sleeping_guard = max(guard_minutes, key = lambda key: guard_minutes[key][1])

    # Look up the minute
    most_common_sleeping_minute = guard_minutes[sleeping_guard][0]

    return sleeping_guard, most_common_sleeping_minute


if __name__ == '__main__':
    with open("input.txt") as file:
        read_lines = file.readlines()

    read_lines = [line.strip() for line in read_lines]

    guards = parse_guards(read_lines)

    longest_sleeping = get_longest_sleeping(guards)
    most_common_minute, _ = get_most_common_minute(guards, longest_sleeping)

    print("Longest sleeping guard: {}".format(longest_sleeping))

    print("Asleep most commonly at {}".format(most_common_minute))
    print("Part 1", longest_sleeping * most_common_minute)

    sleeping_guard, most_common_sleeping_minute = part2(guards)

    print("Guard {} most frequently asleep at {}".format(sleeping_guard, most_common_sleeping_minute))
    print("Part 2", sleeping_guard * most_common_sleeping_minute)
