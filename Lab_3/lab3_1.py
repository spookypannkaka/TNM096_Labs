import random
import copy

class Clause:
    def __init__(self, arg, empty=False):
        self.p = set() # Positive literals
        self.n = set() # Negative literals
        if not empty:
            self.__parse(arg)    


def resolve(A, B):
    pass

def solve(kb):
    pass