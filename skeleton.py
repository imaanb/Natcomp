import typing
import numpy as np


# – An implementation of a 1-dimensional, binary-state cellular automaton (in Python) which operates on arrays of size 60
class CellularAutomata:
    """The cells are defined as follows: 1 = living cell, 0 = dead cell"""

    def __init__(self, rule_number: int):
        """ Intialize the cellular automaton with a given rule number """
        self.rule_number = rule_number
        # Precompute the rule table
        self.rule_table = self.generate_rule_table(rule_number)

    def generate_rule_table(self, rule):
        """Generate the rule table for a given rule number"""
        rule_binary = [int(x) for x in bin(rule)[2:].zfill(8)[::-1]]
        rule_table = {}

        for state in range(8):
            state_binary = format(state, '03b')
            state_tuple = tuple(int(bit) for bit in state_binary)
            rule_table[state_tuple] = rule_binary[state]

        return rule_table

    def apply_rule(self, state):
        """Apply the rule to the state"""

        # The state is extended by wrapping around
        extended_state = [0] + state + [0]
        new_state = []

        for i in range(1, len(extended_state) - 1):
            neighborhood = (extended_state[i - 1], extended_state[i], extended_state[i + 1])
            new_cell_value = self.rule_table[neighborhood]
            new_state.append(new_cell_value)

        return new_state

    def __call__(self, c0: typing.List[int], t: int) -> typing.List[int]:
        """Evaluate for T timesteps. Return Ct for a given C0."""
        state = c0
        state = list(state)
        for _ in range(t):
            state = self.apply_rule(state)
        return state

    @classmethod
    def test(cls, rule_number, c0, ct, t=1):
        ca = cls(rule_number)
        ct_prime = ca(c0, t)
        assert all(trial == expected for trial, expected in zip(ct_prime, ct))


if __name__ == "__main__":
    "If the following statements do not produce an error, your CA works correctly."
    x0 = np.zeros(7, dtype=int)
    x0[x0.size // 2] = 1
    CellularAutomata.test(0, x0, np.zeros(7, dtype=int))
    CellularAutomata.test(30, x0, [0,1,1,0,0,1,0], 2)

    import sys
    rule_number = int(sys.argv[1])
    ca = CellularAutomata(rule_number)
    x0 = np.zeros(60, dtype=int)
    x0[x0.size // 2] = 1
    for t in range(20):
        x0 = ca(x0, 1)
        print(''.join(['*' if cell == 1 else ' ' for cell in x0]))
