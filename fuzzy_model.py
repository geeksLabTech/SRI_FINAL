

def convert_DNF_to_CNF(DNF):
    CNF = []
    literals = set()
    for term in DNF:
        if not term == '^' or not term == 'v' or not term == '(' or not term == ')':
            literals.add(term) 
    while len(DNF) > 0:
        index = 0
        clause = ''
        if DNF[index] == 'v':
            CNF.append(convert_clause_to_CNF(clause , literals))
        else :
            clause.append(DNF[index])
    return CNF

def convert_clause_to_CNF(clause , literals):
    CNF = []
    for term in literals:
        if not term in clause:
            CNF.append()
