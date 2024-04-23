from resolve import resolve, negate_literal

def resolution_solver(clauses):
    # Initialize a set to store all derived resolvents
    derived_clauses = set(frozenset(clause) for clause in clauses)

    # Keep track of previously derived clauses to avoid duplicates
    previous_clauses = set()

    while True:
        new_clauses = set()
        
        # Iterate over each pair of clauses or previously derived resolvents
        for clause1 in derived_clauses:
            for clause2 in derived_clauses:
                # Avoid resolving a clause with itself
                if clause1 != clause2:
                    resolvent = resolve(clause1, clause2)
                    if resolvent is not None and frozenset(resolvent) not in previous_clauses:
                        new_clauses.add(frozenset(resolvent))
        
        # If no new clauses were derived, stop the loop
        if not new_clauses:
            break
        
        # Update the set of derived clauses and add new ones
        previous_clauses.update(derived_clauses)
        derived_clauses.update(new_clauses)

    return derived_clauses

if __name__ == "__main__":
    # A: A is guilty.
    # B: B is guilty.
    # C: C is guilty.
    # D: The crime was committed with a truck.
    
    clauses = [
    {'A', 'B', 'C'},          # Nobody else could have been involved other than A, B, and C
    {'-C', 'A'},              # C never commits a crime without A's participation
    {'-D', 'A', 'C'},         # If the crime was committed with a truck, then either A or C is guilty
    {'-B'}                    # B does not know how to drive
]


    # Apply resolution solver
    derived_clauses = resolution_solver(clauses)

    # Print the derived clauses
    print("Derived Clauses:")
    for clause in derived_clauses:
        print(clause)
