from grammar import Grammar

Blue = '\033[94m'
END = '\033[0m'

if __name__ == '__main__':
    S = 'S'
    Vn = ['S', 'A', 'B', 'C', 'D']
    Vt = ['a', 'b']
    P = {'S': ['AC', 'bA', 'B', 'aA'],
         'A': ['ABab', 'aS', 'epsilon'],
         'B': ['a', 'bS'],
         'C': ['abC'],
         'D': ['AB']}

    grammar = Grammar(S, Vt, Vn, P)
    print(Blue + "\n CFG TO CNF " + END)
    print(f"\nVar. 15 Grammar:  \nTerminal: {grammar.Vt}\nNon-Terminal: {grammar.Vn}\nProductions: {grammar.P}")
    grammar.toChomskyNormalForm()
    print(f"Chomsky Normal Form:\nTerminal: {grammar.Vt}\nNon-Terminal: {grammar.Vn}\nProductions: {grammar.P}")
