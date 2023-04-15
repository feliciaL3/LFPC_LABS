import networkx as nx
import matplotlib.pyplot as plt


class FiniteAutomata:
    # Initialize the class with the required arguments
    def __init__(self, states: set, alphabet: list, transitions: list, first_state, final_state: set):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.first_state = first_state
        self.final_state = final_state

    # Return the transitions as a formatted string
    def get_transitions(self):
        return '\n'.join(str(t) for t in self.transitions) + ':\n'

    # Check if a given word is accepted by the automaton
    def check_word(self, word):
        state = self.first_state[0]
        for i in word:
            # Look for the next state based on the current state and input symbol
            state = next((t.get_next_state() for t in self.transitions if
                          t.get_current_state() == state and
                          t.get_transition_label() == i), None)
            # If the next state cannot be found, return False
            if state is None:
                return False
            # Check if the final state is in the set of accept states
        return str(state) in self.final_state

    # Define the Transitions class, used to represent transitions in the automaton
    class Transitions:
        def __init__(self, current_state, next_state, transition_label):
            self.current_state, self.next_state, self.transition_label = current_state, next_state, transition_label

        def __str__(self):
            return str(self.next_state)

        def get_current_state(self): return self.current_state

        def get_next_state(self): return self.next_state

        def get_transition_label(self): return self.transition_label

    # Define getter and setter methods for the various attributes of the automaton
    def get_states(self):
        return self.states

    def put_states(self, states):
        self.states = states

    def get_alphabet(self):
        return self.alphabet

    def put_alphabet(self, alphabet):
        self.alphabet = alphabet

    def get_first_state(self):
        return self.first_state

    def put_first_state(self, startState):
        self.first_state = startState

    def get_accept_states(self):
        return self.final_state

    def put_accept_states(self, acceptStates):
        self.final_state = acceptStates

    def convert_to_grammar(self, Grammar):
        # Step 1: Create a dictionary to hold the productions for each state
        P = {state: [] for state in self.states}
        # Step 2: Add a new start symbol S
        S = self.first_state + "'"
        P[S] = [self.first_state]
        # Step 3: Add ε-productions for each final state
        for accept_state in self.final_state:
            P[accept_state].append("ε")
        # Step 4: Add productions for each transition
        for q, a, p in self.transitions:
            P[q].append(a + p)
        # Step 5: Create lists of non-terminal and terminal symbols
        Vn = list(self.states) + [S]
        Vt = self.alphabet
        # Step 6: Create the grammar object and return it
        return Grammar(S, Vt, Vn, P)

    def is_deterministic(self):
        # Step 1: Create a dictionary to hold the transitions for each state
        transitions = {}
        # Step 2: Loop through each transition and add it to the dictionary
        for transition in self.transitions:
            if transition[0] in transitions:
                # If the current state already has a transition with the same symbol, it's not deterministic
                if transition[1] in transitions[transition[0]]:
                    return "IT IS NOT DETERMINISTIC"
                # Otherwise, add the transition symbol to the dictionary for this state
                else:
                    transitions[transition[0]].append(transition[1])
                    # If the current state doesn't have any transitions yet, add the transition to the dictionary
            else:
                transitions[transition[0]] = [transition[1]]
                # Step 3: If the function hasn't returned yet, the automaton is deterministic
        return "IT IS DETERMINISTIC"

    def convert_to_dfa(self):
        # Step 1: Initialize the DFA with an empty set of states and the same alphabet as the original automaton
        dfa_states, dfa_alphabet, dfa_transitions, dfa_acceptStates = set(), self.alphabet, [], set()

        # Step 2: Compute the epsilon closure of the initial state and make it the start state of the DFA
        dfa_startState = frozenset(self.epsilon_closure({self.first_state}, self.transitions))

        # Step 3: Initialize a queue with the start state of the DFA and an empty set of processed states
        queue, processed_states = [dfa_startState], set()

        # Step 4: While the queue is not empty, process the next state in the queue
        while queue:
            # Step 5: Get the next state from the queue and add it to the set of processed states
            state_set = queue.pop(0)
            if state_set in processed_states:
                continue
            processed_states.add(state_set)

            # Step 6: Add the current state to the set of states in the DFA
            dfa_states.add(state_set)

            # Step 7:If the current state contains a final state from the original automaton, mark it as an accept state
            for accept_state in self.final_state:
                if accept_state in state_set:
                    dfa_acceptStates.add(state_set)
                    break

            # Step 8: For each symbol in the alphabet, compute the epsilon closure of the set of states that can be
            # reached from the current state using that symbol
            for symbol in dfa_alphabet:
                next_states = self.epsilon_closure(self.move(state_set, symbol, self.transitions), self.transitions)
                if next_states:
                    # Step9:Add transition to DFA and add the next state to the queue if it hasn't been processed yet
                    dfa_transitions.append((state_set, symbol, frozenset(next_states)))
                    if frozenset(next_states) not in processed_states:
                        queue.append(frozenset(next_states))

        # Step 10: Return the DFA as a new FiniteAutomata object
        return FiniteAutomata(states=dfa_states, alphabet=dfa_alphabet, transitions=dfa_transitions,
                               first_state=dfa_startState, final_state=dfa_acceptStates)

    # This function computes the epsilon closure of a given set of states
    # with respect to a given set of transitions in a non-deterministic finite
    # automaton (NFA).

    def epsilon_closure(self, states, transitions):
        # Create a new set containing the initial states
        e_closure = set(states)
        # Create a queue to hold the current states to process
        queue = list(states)
        # Loop through the states in the queue
        while queue:
            # Get the next state to process
            state = queue.pop(0)
            # Find all the next states that can be reached using epsilon transitions
            next_states = [transition[2] for transition in transitions if
                           transition[0] == state and transition[1] == 'ε']
            # Find the new states that haven't been added to the epsilon closure yet
            new_states = set(next_states) - e_closure
            # Add the new states to the epsilon closure
            e_closure |= new_states
            # Add the new states to the queue to be processed
            queue.extend(new_states)
        # Return the final epsilon closure
        return e_closure

    # This function computes the set of states that can be reached from a given set
    # of states using a given symbol and a given set of transitions in an NFA.

    def move(self, states, symbol, transitions):
        # Find all the states that can be reached using the given symbol
        # from any of the given states
        return {transition[2] for state in states for transition in transitions if
                transition[0] == state and transition[1] == symbol}

    # This function draws the graph of the state transitions of the NFA.

    def draw(self):
        # Create a directed graph using the states and transitions of the NFA
        G = nx.DiGraph()
        G.add_nodes_from(self.states)
        G.add_edges_from([(t[0], t[2], {'label': t[1]}) for t in self.transitions])
        # Set the layout of the graph to circular
        pos = nx.circular_layout(G)
        # Set the style parameters for the nodes and edges
        font_family = 'Times New Roman'
        node_color = '#c28488'
        node_size = 2400
        font_size = 22
        node_border_color = 'black'
        node_border_width = 2
        edge_color = '#990610'
        edge_width = 2
        arrow_size = 28
        # Create a new figure and axis for the plot
        fig, ax = plt.subplots(figsize=(12, 12), facecolor='white', linewidth=2)
        # Draw the nodes of the graph
        nx.draw_networkx_nodes(G, pos, node_size=node_size, alpha=0.8, node_color=node_color,
                               edgecolors=node_border_color, linewidths=node_border_width)
        # Draw the labels for the nodes
        nx.draw_networkx_labels(G, pos, font_size=font_size, font_family=font_family, font_weight='bold')
        # Create a dictionary of edge labels and their positions
        edge_labels = {(e[0], e[1]): e[2]['label'] for e in G.edges(data=True)}
        edge_label_pos = nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=30,
                                                      font_family=font_family, font_weight='bold',
                                                      label_pos=0.9,
                                                      bbox=dict(facecolor='white', edgecolor='none', alpha=0.8),
                                                      verticalalignment='center')
        # Set the rotation of the edge labels to horizontal
        for _, t in edge_label_pos.items():
            t.set_rotation('horizontal')
        # Draw the edges of the graph
        nx.draw_networkx_edges(G, pos, edgelist=G.edges(), arrows=True, arrowsize=arrow_size, width=edge_width,
                               edge_color=edge_color)
        # Set the title, axis, and text for the plot
        ax.set_title("Graph of State Transitions ", fontsize=24, fontweight='bold')
        ax.set_axis_off()
        plt.figtext(0.1, 0.1, "Initial State - q0\nFinal State - q3", fontsize=18, fontweight='bold')
        # Remove the spines of the axis
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Show the plot
        plt.show()
