import FiniteAutomaton
from typing import List, Dict


class Grammar:
    def __init__(self, S: str, Vt: List[str], Vn: List[str], P: Dict[str, List[str]]):
        self.S = S
        self.Vt = Vt
        self.Vn = Vn
        self.P = P

    def toChomskyNormalForm(self):
        print("--------------------------")
        self.removeEpsilon()
        print("Step 1. Removing Epsilon: \n" + "Vt: ", self.Vt, "\nVn: ", self.Vn, "\nP: ", self.P)
        print("--------------------------")
        self.removeUnit()
        print("Step 2. Removing Unit Productions: \n" + "Vt: ", self.Vt, "\nVn: ", self.Vn, "\nP: ", self.P)
        print("--------------------------")
        self.removeInaccessible()
        print("Step 3. Removing Inaccessible: \n" + "Vt: ", self.Vt, "\nVn: ", self.Vn, "\nP: ", self.P)
        print("--------------------------")
        self.removeNonProductive()
        print("Step 4. Removing Non-Productive: \n" + "Vt: ", self.Vt, "\nVn: ", self.Vn, "\nP: ", self.P)
        print("--------------------------")
        self.removeRemainingUnits()

        return self.P, self.Vt, self.Vn

    def removeEpsilon(self):
        # Create a set to store variables that produce epsilon
        epsilon = set()
        # Iterate through each variable in the grammar
        for variable, P in self.P.items():
            # If the production for a variable contains epsilon, add it to the set
            if "ε" in P:
                epsilon.add(variable)

        for left, right in self.P.items():
            for i in right:
                # Iterate through each variable that produces epsilon
                for j in epsilon:
                    # If the variable that produces epsilon is in the right-hand side of the production
                    if j in i:
                        # If the variable that produces epsilon is the same as the left-hand side of the production,
                        # skip to the next variable that produces epsilon
                        if left == j:
                            break
                        # Replace the variable that produces epsilon with an empty string in the right-hand side of the production
                        # and add the resulting string to the list of productions for the left-hand side of the production
                        self.P[left] = [x.replace(j, "") for x in self.P[left]]
                        self.P[left].append(i)
                        # If the right-hand side of the production is epsilon, remove it from the list of productions
                    elif i == "ε":
                        self.P[left].remove(i)

        return self.P

    def removeUnit(self):
        # For every variable A in the grammar
        for left, right in self.P.items():
            # For every production rule B -> C for A
            for e in right:
                # If B is a non-terminal and C is a terminal
                if len(e) == 1 and e in self.Vn:
                    # Replace B -> C with B -> productions of C
                    self.P[left].remove(e)
                    self.P[left].extend(self.P[e])
            new_P = self.P[left]
            for prod in new_P:
                if len(prod) == 1 and prod in self.Vn:
                    # Recursively apply the unit productions
                    self.removeUnit()
        # Return the modified productions
        return self.P

    def removeInaccessible(self):
        # Create a set of symbols that can be reached from the starting symbol
        accessible = set()
        for left, right in self.P.items():
            for r in right:
                for w in r:
                    accessible.add(w)
        # Remove all non-accessible symbols from the grammar
        for left, right in self.P.items():
            for a in left:
                if a in accessible:
                    continue
                else:
                    del self.P[a]
                    del self.Vn[self.Vn.index(a)]
                    return self.P
        return self.P

    def removeNonProductive(self):
        productive = set()  # create a set to hold productive variables
        for left, right in self.P.items():  # loop through all productions
            for r in right:
                if r in self.Vt:  # if production contains a terminal symbol, skip it
                    productive.add(left)  # add left side of production to productive set

        for left, right in self.P.items():
            new_right = []
            for lt in left:
                if lt not in productive:  # if variable not in productive set, remove it
                    del self.P[lt]
                    del self.Vn[self.Vn.index(lt)]
                    return self.P

            for r in right:
                if len(r) > 1:  # if production contains more than one symbol
                    for w in r:
                        if w in self.Vn:
                            if w in new_right:  # avoid adding duplicates
                                break
                            elif w not in productive:  # if variable not productive, remove it
                                new_right.append(r.replace(w, ""))
                        elif w in self.Vt and w not in self.P[left]:  # if terminal symbol not in right side of production, add it
                            new_right.append(r.replace(r, w))
                        elif w in self.Vt and w in self.P[
                                left]:  # if terminal symbol already in right side of production
                            if len(r) > 2:  # if production has more than 2 symbols, skip it
                                continue
                            new_right.append(r.replace(w, ""))  # remove terminal symbol
                        else:
                            continue
                else:
                    new_right.append(r)  # production contains only one symbol, add it to new_right

            self.P[left] = new_right  # update production
        return self.P

    def toFiniteAutomaton(self):
        states = set()
        finalStates = {'X'}
        dimension = 0
        transitions = []
        for nonTerminal in self.Vn:
            dimension += len(self.P[nonTerminal])
        for nonTerminal in self.Vn:
            states.add(nonTerminal)
            rightHandSides = self.P[nonTerminal]
            for rightSide in rightHandSides:
                if len(rightSide) > 1:
                    nextState = rightSide[1]
                else:
                    nextState = 'X'
                transitionLabel = rightSide[0]
                transitions.append((nonTerminal, transitionLabel, nextState))
        states.add('X')
        automaton = FiniteAutomaton(states, self.Vt, transitions, self.S, finalStates)
        automaton.setStates(states)
        automaton.setStartState(str(self.S))
        automaton.setAcceptStates(finalStates)
        automaton.setAlphabet(self.Vt)
        return automaton

    def classify_grammar(self):
        for nonTerminal in self.Vn:
            for production in self.P[nonTerminal]:
                if len(production) > 2 or not (
                        production[0] in self.Vt or production[0] in self.Vn) or (
                        len(production) == 2 and production[1] not in self.Vn):
                    return 'Type 2'

        for nonTerminal in self.Vn:
            if nonTerminal != self.S:
                if len(self.P[nonTerminal]) > 1 or not (
                        len(self.P[nonTerminal][0]) == 1 and (
                        self.P[nonTerminal][0][0] in self.Vt or self.P[nonTerminal][0][0] in self.Vn)):
                    return 'Type 3'

        for nonTerminal in self.Vn:
            for production in self.P[nonTerminal]:
                for symbol in production:
                    if symbol not in self.Vt and symbol not in self.S:
                        return 'Type 0'
        return 'Type 1'

    def removeRemainingUnits(self):
        # For every variable A in the grammar
        for left, right in self.P.items():
            new_right = right.copy()
            # For every production rule B -> C for A
            for e in right:
                # If B is a non-terminal and C is a non-terminal
                if len(e) == 1 and e in self.Vn:
                    # Find all productions of C and add them to A's productions
                    if e in self.P:
                        for prod in self.P[e]:
                            if prod not in new_right:
                                new_right.append(prod)
            self.P[left] = new_right
        # Remove any remaining unit productions
        for left, right in self.P.items():
            new_right = right.copy()
            for e in right:
                if len(e) == 1 and e in self.Vn:
                    new_right.remove(e)
            self.P[left] = new_right
        return self.P
