import sys
import numpy as np
import matplotlib.pyplot as plt
from skeleton import CellularAutomata


N_REPEATS = 10
N_STEPS = 100

rule_number = int(sys.argv[1])

def generate_runs(rule_number, n_steps):
    ca = CellularAutomata(rule_number)
    state = np.random.randint(2, size=60)
    states = [state]
    for _ in range(n_steps - 1):
        state = ca(state, 1)
        states.append(state)
    return states


def count_nonzero(states):
    return [np.count_nonzero(state) / np.count_nonzero(states[0]) for state in states]

# the longest string of equal symbols
def longest_consecutive_string(states):
    result = []
    
    for state in states:
        max_consecutive = 0
        current_consecutive = 0
        
        for last_digit, digit in zip(state, state[1:]):
            if last_digit == digit:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0

        result.append(max_consecutive)
    
    return result


def num_changed(states):
    results = [0]
    for prev_state, state in zip(states, states[1:]):
        n_changed = sum(1 if prev_state[i] != state[i] else 0 for i in range(len(prev_state)))
        results.append(n_changed)
    return results


# compute the age of the state that has not been updated for the longest time
def longest_surviving_cell_age(states):
    ages = [0] * len(states[0])
    results = [0]
    for prev_state, state in zip(states, states[1:]):
        for i, (prev_cell, cell) in enumerate(zip(prev_state, state)):
            if prev_cell == cell:
                ages[i] += 1
            else:
                ages[i] = 0
        results.append(max(ages))
        assert max(ages) >= 0
    return results


if __name__ == "__main__":
    # python experiment.py 26

    num_living = []
    lcs = []
    nc = []
    a = []
    for i in range(N_REPEATS):
        states = generate_runs(rule_number, N_STEPS)
        num_living.append(count_nonzero(states))
        lcs.append(longest_consecutive_string(states))
        nc.append(num_changed(states))
        a.append(longest_surviving_cell_age(states))

        for state in states:
            print(''.join(['*' if cell == 1 else ' ' for cell in state]))

    plt.clf()
    plt.plot(np.mean(num_living, axis=0))
    plt.fill_between(range(N_STEPS), np.mean(num_living, axis=0) - np.std(num_living, axis=0), np.mean(num_living, axis=0) + np.std(num_living, axis=0), alpha=0.2)
    plt.savefig(f'num_living-{rule_number}.png')

    plt.clf()
    plt.plot(np.mean(lcs, axis=0))
    plt.fill_between(range(N_STEPS), np.mean(lcs, axis=0) - np.std(lcs, axis=0), np.mean(lcs, axis=0) + np.std(lcs, axis=0), alpha=0.2)
    plt.savefig(f'longest_continuous_string-{rule_number}.png')

    plt.clf()
    plt.plot(np.mean(nc, axis=0))
    plt.fill_between(range(N_STEPS), np.mean(nc, axis=0) - np.std(nc, axis=0), np.mean(nc, axis=0) + np.std(nc, axis=0), alpha=0.2)
    plt.savefig(f'num_changed-{rule_number}.png')

    plt.clf()
    plt.plot(np.mean(a, axis=0))
    plt.fill_between(range(N_STEPS), np.mean(a, axis=0) - np.std(a, axis=0), np.mean(a, axis=0) + np.std(a, axis=0), alpha=0.2)
    plt.savefig(f'age-{rule_number}.png')
