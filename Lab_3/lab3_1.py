import random

class Clause:
    def __init__(self, literals=None, empty=False):
        self.p = set() # Positive literals
        self.n = set() # Negative literals
        if literals and not empty:
            self.__parse(literals)

    def __parse(self, literals):
        # Properly handle literals parsing to avoid empty strings or incorrect entries
        for literal in literals:
            literal = literal.strip()
            if literal.startswith('~'):
                self.n.add(literal.strip('~'))
            elif literal:
                self.p.add(literal)

    def __str__(self):
        # Ensure that the string output doesn't have trailing commas or show empty sets incorrectly
        positive_literals = ', '.join(sorted(self.p)) if self.p else ''
        negative_literals = ', '.join('~' + x for x in sorted(self.n)) if self.n else ''
        if positive_literals and negative_literals:
            return f"{{{positive_literals}, {negative_literals}}}"
        else:
            return f"{{{positive_literals}{negative_literals}}}"


def resolution(A, B):
    print(f"Attempting to resolve between {A} and {B}")
    C = Clause()

    # Check if there are opposite literals in the set, if there are then resolve
    if not A.p.intersection(B.n) and not A.n.intersection(B.p):
        print("No resolution possible")
        return False
    
    new_p = set(A.p)
    new_n = set(A.n)
    
    # Choose one of the intersections to proceed with
    if A.p.intersection(B.n):
        # Pick random element from intersection
        literal = random.choice(list(A.p.intersection(B.n)))
    
        # Remove element from both clauses
        new_p.remove(literal)
        new_n.update(B.n - {literal})
        new_p.update(B.p)
    
    elif A.n.intersection(B.p): # Do the opposite
        literal = random.choice(list(A.n.intersection(B.p)))

        new_n.remove(literal)  # Remove from new negative
        new_p.update(B.p - {literal})  # Union with adjusted positives from B
        new_n.update(B.n)  # Union negatives from B

    # Put all the positive and negative elements from A and B into positive and negative parts of C
    C.p = new_p
    C.n = new_n

    # Tautology C.p = A, C.n = A
    if C.p.intersection(C.n):
        print("Resulting clause is a tautology")
        return False
    
    print(f"Resolved clause: {C}")
    return C

def solver(KB):
    KB_set = set(KB)
    S = set() # Temporary clauses
    KB_prime = set() # Previous state of kb

    KB = incorporate(KB, set())

    while True:
        S = set()
        KB_prime = set(KB)

        # Derive new clauses by iterating through all pairs of clauses
        for A in KB:
            for B in KB:
                C = resolution(A, B)
                if C is not False:
                    S.add(C)

        if not S:
            print("No new clauses derived")
            return KB

        
        KB = incorporate(S, KB)
        if KB_prime == KB:
            print("No change in knowledge base; stopping")
            break

    print("Final knowledge base:")
    for clause in KB:
        print(clause)
    return KB

def incorporate_clause(A, KB):
    for B in KB:
        if B.p <= A.p and B.n <= A.n:
            return KB

    # If no clause subsumes A, prepare to add A to KB
    KB_set = set(KB)  # Create a copy of KB to modify
    for B in list(KB_set):
        # Check if A subsumes B
        if A.p <= B.p and A.n <= B.n:
            # Remove B as it is subsumed by A
            KB_set.remove(B)
    
    # Add A to KB since it wasn't subsumed by any clause in KB
    KB_set.add(A)
    return KB_set

def incorporate(S, KB):
    KB_set = set(KB)
    for clause in S:
        KB_set = incorporate_clause(clause, KB_set)
    return list(KB_set)

KB = {Clause(["~sun", "~money", "ice"]), 
      Clause(["~money", "ice", "movie"]),
      Clause(["~movie", "money"]),
      Clause(["~movie", "~ice"]),
      Clause(["sun", "money", "cry"]),
      Clause(["movie"])
     }

final_kb = solver(KB)

# Output the result
for clause in final_kb:
    print(clause)

# Robbery
robbery_kb = {Clause(["A", "B", "C"]), # Nobody else could have been involved other than A, B and C.
              Clause(["A", "~C"]), # C never commits a crime without A’s participation.
              Clause(["~B", "A", "C"]) # B does not know how to drive. -> B cannot commit a crime without A or C
             }

# Run the solver to process these clauses
final_kb_robbery = solver(robbery_kb)

# Output the result
print("Final Knowledge Base for the Robbery Scenario:")
for clause in final_kb_robbery:
    print(clause)