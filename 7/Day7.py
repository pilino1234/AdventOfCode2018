import string
from collections import defaultdict
import copy

def parse_steps(lines):
    steps = defaultdict(list)

    for line in lines:      # type: str
        step1 = line[5]
        step2 = line[-12]
        steps[step2].append(step1)

    return steps


def assemble(steps_in):
    steps = copy.deepcopy(steps_in)
    ready = []
    done = []

    while len(done) < 26:
        for letter in string.ascii_uppercase:
            if len(steps[letter]) == 0 and letter not in ready and letter not in done:
                ready.append(letter)

        ready = sorted(ready)

        next_step = ready[0]
        for step in steps:
            if next_step in steps[step]:
                steps[step].remove(next_step)
        ready.remove(next_step)
        done.append(next_step)

    return done


def assemble_with_workers(steps_in, worker_count):
    steps = copy.deepcopy(steps_in)
    workers = {}
    for i in range(worker_count):
        workers[i] = (None, 0)

    ready = []
    done = []
    step_times = {step: ord(step)-4 for step in string.ascii_uppercase}
    # step_times = {step: time+1 for time, step in enumerate("ABCDEF")}

    second = 0

    currently_working = []

    while len(done) < 26:
        # Finish worker work
        for worker, work in workers.items():
            if work[1] == 0:
                if work[0] is not None:
                    print(worker, "finishing", work[0])
                    # Finish work
                    for step in steps:
                        if work[0] in steps[step]:
                            steps[step].remove(work[0])
                    done.append(work[0])
                    currently_working.remove(work[0])


        # Check if there is new work
        # for letter in "ABCDEF":
        for letter in string.ascii_uppercase:
            if len(steps[letter]) == 0 and letter not in ready \
                    and letter not in done and letter not in currently_working:
                ready.append(letter)
        ready = sorted(ready)

        print("Ready", ready)

        # Assign new work
        for worker, work in workers.items():
            if work[1] == 0:
                # Get next job if there is one
                if ready:
                    print("Worker is done, getting next job")
                    next_step = ready[0]
                    workers[worker] = (next_step, step_times[next_step]-1)
                    ready.remove(next_step)
                    currently_working.append(next_step)
                else:
                    workers[worker] = (None, 0)
            else:
                print("Worker has work {}, finishing in".format(work[0]), work[1]-1)
                workers[worker] = (work[0], work[1]-1)
        second += 1

        for worker in workers:
            print(worker, workers[worker])

        print("------------------------------------------")

    return second-1


if __name__ == "__main__":
    with open("input.txt") as file:
        lines = [line.strip() for line in file.readlines()]

    test = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".split('\n')
    steps = parse_steps(lines)

    step_order = assemble(steps)
    print("".join(step_order))

    worker_step_time = assemble_with_workers(steps, 5)
    print(worker_step_time)
