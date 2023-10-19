import sys
import numpy as np
import matplotlib.pyplot as plt
from skeleton import CellularAutomata


N_REPEATS = 100 # number of times to repeat the experiment
N_STEPS = 100 # number of steps to run the CA for in an experiment

def generate_runs(rule_number, n_steps):
    """Generate n_steps of the CA with the given rule number"""
    ca = CellularAutomata(rule_number)
    state = np.random.randint(2, size=60)
    states = [state]
    for _ in range(n_steps - 1):
        state = ca(state, 1)
        states.append(state)
    return states

def count_nonzero(states):
    """Return the fraction of living cells in each state"""
    return [np.count_nonzero(state) / np.count_nonzero(states[0]) for state in states]

def longest_consecutive_string(states):
    """Return the length of the longest consecutive string of 1s or 0s in each state"""
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
    """Return the number of cells that changed from the previous state to the current state"""
    results = [0]
    for prev_state, state in zip(states, states[1:]):
        n_changed = sum(1 if prev_state[i] != state[i] else 0 for i in range(len(prev_state)))
        results.append(n_changed)
    return results

def longest_surviving_cell_age(states):
    """Return the age of the longest surviving cell in each state"""
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

def save_fig(datas, experiment_name):
    """Save a figure with the given datas"""
    plt.figure()
    for rule_number, data in datas.items():
        mean = np.mean(data, axis=0)
        plt.plot(mean, label=rule_number)
    plt.legend()
    plt.title(experiment_name)

    rules_string = "-".join([str(rule_number) for rule_number in datas.keys()])
    figname = f"{experiment_name}-{rules_string}.png"
    plt.savefig(figname)


def main():
    """Run the experiments.

    Example:
    $ python3 experiment.py 30 90 110
    """

    rule_numbers = [int(x) for x in sys.argv[1:]]
    if len(rule_numbers) == 0:
        raise ValueError("Please provide at least one rule number")

    num_living = {rule_number: [] for rule_number in rule_numbers}
    lcs = {rule_number: [] for rule_number in rule_numbers}
    nc = {rule_number: [] for rule_number in rule_numbers}
    a = {rule_number: [] for rule_number in rule_numbers}
    for rule_number in rule_numbers:
        for i in range(N_REPEATS):
            # seed the random number generator with the repeat number
            # this ensures that each rule number has a different yet
            # repeatable random initial state
            np.random.seed(i)
            states = generate_runs(rule_number, N_STEPS)
            num_living[rule_number].append(count_nonzero(states))
            lcs[rule_number].append(longest_consecutive_string(states))
            nc[rule_number].append(num_changed(states))
            a[rule_number].append(longest_surviving_cell_age(states))

    save_fig(num_living, experiment_name='num_living')
    save_fig(lcs, experiment_name='longest_continuous_string')
    save_fig(nc, experiment_name='num_changed')
    save_fig(a, experiment_name='age')


if __name__ == "__main__":
    main()
