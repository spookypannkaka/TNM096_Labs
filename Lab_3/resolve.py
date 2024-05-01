def resolve(clause1, clause2):
    resolvent = clause1.union(clause2)

    for literal1 in clause1:
        negation_literal1 = negate_literal(literal1)
        if negation_literal1 in clause2:
            # Create a new set for the resolvent
            resolvent = resolvent - {literal1, negation_literal1}
            if not resolvent:
                return None  # Contradiction found

    return resolvent

def negate_literal(literal):
    if literal.startswith('-'):
        return literal[1:]
    else:
        return '-' + literal

if __name__ == "__main__":
    # Example clauses in CNF
    clause1 = {'sun', '-money'}
    clause2 = {'sun', 'car'}

    # Resolve the clauses
    resolvent = resolve(clause1, clause2)

    # Print the resolvent
    if resolvent is None:
        print("Contradiction: Empty clause obtained.")
    else:
        print("Resolvent:", resolvent)
