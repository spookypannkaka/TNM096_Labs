import random
import copy
#from sympy import subsets

class Clause:
    def __init__(self, arg=None, empty=False):
        self.p = set() # Positive literals
        self.n = set() # Negative literals
        if not empty and arg is not None:
            self.__parse(arg)

    def __parse(self, arg):
        for a in arg:
            if a.startswith('~'):
                self.n.add(a.strip('~'))
            else:
                self.p.add(a)


def resolution(A, B):
    C = Clause()

    # Check if there are opposite literals in the set, if there are then resolve
    if not A.p.intersection(B.n) and not A.n.intersection(B.p):
        return False
    
    # Choose one of the intersections to proceed with
    if A.p.intersection(B.n):
        # Pick random element from intersection
        literal = random.choice(list(A.p.intersection(B.n)))
    
        # Remove element from both clauses
        B.n.remove(literal)
        A.p.remove(literal)
    else: # Do the opposite
        literal = random.choice(list(A.n.intersection(B.p)))

        A.n.remove(literal)
        B.p.remove(literal)

    # Put all the positive and negative elements from A and B into positive and negative parts of C
    C.p = A.p.union(B.p)
    C.n = A.n.union(B.n)

    # Tautology C.p = A, C.n = A
    if C.p.intersection(C.n):
        return False
    
    return C

def solver(KB):
    KB_set = set(KB)
    S = set() # Temporary clauses
    KB_prime = set() # Previous state of kb

    while True:
        S = set()
        KB_prime = set(KB)

        # Derive new clauses by iterating through all pairs of clauses
        for A in KB:
            for B in KB:
                if A != B:  # Ensure A and B are different clauses
                    C = resolution(A, B)
                    if C is not False:
                        S.add(C)

        if not S:
            return KB

        
        KB = incorporate(S, KB)
        if KB_prime == KB:
            break

    return KB

def incorporate_clause(A, KB):
    for B in KB:
        if B.issubset(A):
            return KB
    
    KB_prime = KB.copy()  # Create a copy of KB to iterate over and modify
    for B in KB:
        if A.issubset(B):
            KB_prime.remove(B)
    
    KB_prime.add(A)
    return KB_prime

def incorporate(S, KB):
    KB_set = set(KB)
    for clause in S:
        KB_set = incorporate_clause(clause, KB_set)
    return list(KB_set)


'''KB = {}

A = Clause(["a", "b"])
B = Clause(["~a", "c"])
C = Clause(["~b"])
KB = [A, B, C]

result_kb = solver(KB)

D = Clause(["a"])
E = Clause(["~a"])
KB = [A, B, C, D, E]

result_kb = solver(KB)'''

##

KB = set()

A = Clause()
A.n = set(['sun', 'money'])
A.p = set(['ice'])

B = Clause()
B.n = set(['money'])
B.p = set(['ice','movie'])

C = Clause()
C.n = set(['movie'])
C.p = set(['money'])

D = Clause()
D.n = set(['movie', 'ice'])

E = Clause()
E.p = set(['sun', 'money', 'cry'])

'''A = Clause(["ice", "sun"])
B = Clause(["~money", "ice", "movie"])
C = Clause(["~movie", "money"])
D = Clause(["~movie", "~ice"])
E = Clause(["sun", "money", "cry"])'''

incorporate_clause(A, KB)
incorporate_clause(B, KB)
incorporate_clause(C, KB)
incorporate_clause(D, KB)
incorporate_clause(E, KB)

solver(KB)