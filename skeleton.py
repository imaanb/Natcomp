import typing
import numpy as np


# – An implementation of a 1-dimensional, binary-state cellular automaton (in Python) which operates on arrays of size 60
class CellularAutomata:
    """Skeleton CA, you should implement this."""

    def __init__(self, rule_number: int):
        """Intialize the cellular automaton with a given rule number"""
        self.rule_number = rule_number 
        

    def generate_rule_table(self): #added by Imaan 
        "Convert rule number into binary rule table of lenght 8"
        table = '{0:08b}'.format(self.rule_number)
        return(table)

    

    def __call__(self, c0: typing.List[int], t: int) -> typing.List[int]:
        """Evaluate for T timesteps. Return Ct for a given C0."""
        hist = [c0.copy()]
        print()

        for i in range(t): 
            state_curr = history[-1]  #how many times are we regenating a binary string? 
            next_state = np.zeros(len(state_curr)) #intializing next string 
            for j in range(len(state_curr)):       #defining the neighbourhood ---> wat about edge cases? 
                neighbours = [state_curr[j-1], state_curr[j], state_curr[j+1]]



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



instance1 = CellularAutomata(30)

print(CellularAutomata.generate_rule_table(instance1))


