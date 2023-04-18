import unittest
from grammar import Grammar


class UnitTest(unittest.TestCase):
    # Define the grammar to be used for testing
    startingCharacter = 'S'
    nonTerminal = ['S', 'A', 'B', 'C', 'D']
    terminal = ['a', 'b']
    productions = {'S': ['AC', 'bA', 'B', 'aA'],
                   'A': ['ABab', 'aS', 'ε'],
                   'B': ['a', 'bS'],
                   'C': ['abC'],
                   'D': ['AB']
                   }
    grammar = Grammar(startingCharacter, terminal, nonTerminal, productions)

    # Convert the grammar to an automaton
    automaton = grammar.toFiniteAutomaton()

    # Test that the grammar is equivalent to itself
    def test_grammar(self):
        self.assertEqual(self.grammar, self.grammar)

    def test_convertFaToGrammar(self):
        self.assertEqual(self.automaton.convertToRegularGrammar(Grammar),
                         ({'S': ['AC', 'bA', 'B', 'aA'],
                           'A': ['ABab', 'aS', 'ε'],
                           'B': ['a', 'bS'],
                           'C': ['abC'],
                           'D': ['AB']},
                          ['a', 'b'],
                          ['S', 'A', 'B', 'C', 'D']))

    # Test that the grammar can be converted to Chomsky normal form
    def test_to_chomsky_normal_form(self):
        self.assertEqual(self.grammar.toChomskyNormalForm(),
                         ({'S': ['b', 'a', 'A', 'ab', 'S'],
                           'B': ['a', 'bS'],
                           'C': ['abC']},
                          ['a', 'b'],
                          ['S', 'B', 'C']))

    # Test that epsilon productions can be removed from the grammar
    def test_epsilon(self):
        self.assertEqual(self.grammar.removeEpsilon(),
                         {'S': ['C', 'b', 'B', 'a', 'aA', 'C', 'b'],
                          'A': ['ABab', 'aS'],
                          'B': ['a', 'bS'],
                          'C': ['abC'],
                          'D': ['AB']})

    # Test that inaccessible symbols can be removed from the grammar
    def test_remove_inaccessible(self):
        self.assertEqual(self.grammar.removeInaccessible(),
                         {'S': ['b', 'a', 'b', 'aA', 'abC', 'a', 'bS', 'abC'],
                          'A': ['ABab', 'aS'],
                          'B': ['a', 'bS'],
                          'C': ['abC']})

if __name__ == '__main__':
    unittest.main()
