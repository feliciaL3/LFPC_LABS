# Topic: Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata

### Author: Lupascu Felicia, FAF-212
----------------------------------------------

## Theory
<p align="justify"> &ensp;&ensp;&ensp; Regular expression is the language which is used to describe the language and is accepted by finite automata. Regular expressions are the most effective way to represent any language. There are 4 types of grammar according to Chomsky Classification: <p>
    
* Type 0 – Phrase-structure Grammars
* Type 1 – Context-Sensitive
* Type 2 – Context-Free
* Type 3 – Regular


**Definitions and important concepts:**
* Language - a process of communicating information.
* Formal language - a set of strings based on an alphabet generated with the help of a grammar.
* String - a combination of symbols generated with the help of rules.
* Grammar - an entity defined by 4 elements (the set of non-terminal symbols, the set of terminal symbols, the start symbol, and the set of production rules).
* Automaton - an abstract  computational device.
* Finite automaton - a device with a finite amount of memory.



## Objectives:

<p align="justify">1.  Understand what a language is and what it needs to have in order to be considered a formal one. <p>

<p align="justify">2.  Provide the initial setup for the evolving project that you will work on during this semester. I said project because usually at lab works, I encourage/impose students to treat all the labs like stages of development of a whole project. Basically you need to do the following: <p>

      a.  Create a local && remote repository of a VCS hosting service.

      b.  Choose a programming language, and my suggestion would be to choose one that supports all the main paradigms;

      c.  Create a separate folder where you will be keeping the report. 

<p align="justify">3.  According to your variant number (by universal convention it is register ID), get the grammar definition and do the following tasks: <p>

     a.  Implement a type/class for your grammar;

     b.  Add one function that would generate 5 valid strings from the language expressed by your given grammar;

     c.  Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

     d.  For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;


## Implementation description
<p align="justify">&ensp;&ensp;&ensp; To implement this laboratory work I selected Python language. Firstly, I created two classes, one for the grammar, and the second one for the  finite automata. <p>
    
#### GRAMMAR for variant 15 :

```
class Grammar:
    def __init__(self, Vn, Vt, P, S):
        self.Vn = Vn
        self.Vt = Vt
        self.P = P
        self.S = S
``` 
Respectively
```
Vn = ['S', 'A', 'B']
Vt = ['a', 'b', 'c']
P = {'S': ['aS', 'bS', 'cA'],
     'A': ['aB'],
     'B': ['aB', 'bB', 'c']}
```
Constructor for the Finite Automaton:
```
class Finite_Automat:
    def __init__(self, Q, sigma, delta, q0, f):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.f = f
```
**Method Generate String**

<p align="justify"> &ensp;&ensp;&ensp;The  method called "generate_string" that belongs to a class that has some attributes, such as "S" (a starting symbol), "Vn" (a set of non-terminal symbols), and "P" (a dictionary of production rules). The purpose of this method is to generate a random string based on the production rules provided.The method starts by assigning the "S" attribute to a variable called "string" and setting the "index" to 0. Then, it enters a loop that checks each character of the "string" until the end of the string is reached. <p>

<p align="justify">&ensp;&ensp;&ensp;For each character, the method checks whether it is a non-terminal symbol. If it is, it randomly selects a production rule from the list of possible rules (in the "P" dictionary) for that symbol, replaces the non-terminal symbol with the selected rule in the "string", and then moves the "index" back one step so that the method checks the first character of the newly added substring.If the character is a terminal symbol, the method simply increments the "index" to check the next character in the "string". <p>

<p align="justify">&ensp;&ensp;&ensp;After the loop ends, the method returns the final "string" with all the non-terminal symbols replaced by their respective production rules. Therefore, this method implements a simple form of context-free grammar (CFG) that can generate random strings based on the provided set of production rules. <p>
    
```
    def generate_string(self):
        string, index = self.S, 0
        while index < len(string):
            symbol = string[index]

            # Check if the symbol is a non-terminal indicated by Vn
            if symbol in self.Vn:
                # If so, it randomly selects a rule from the list
                post_rule = random.choice(self.P[symbol])
                # Replace the non-terminal symbol  with a rule.
                string = string.replace(symbol, post_rule, 1)
                index -= 1
            # Increments the index to move on to the next character in the string
            index += 1

        return string
```

The function generate_strings generates a list of 5 unique strings by repeatedly calling the generate_string function and checking if the generated string is already in the list.


```
    # Create the function which would generate 5 strings.
    def generate_strings(self):
        # initializes an empty list called str_list and sets the variable str_num to 5
        str_list, str_num = [], 5
        while str_num != 0:
            # generates a random string, assigns result to variable string
            string = self.generate_string()
            # checks if the generated string is already in the str_list
            if string not in str_list:
                print(string)
                # If the generated string isn't in str_list,add it to the list
                str_list.append(string)
                str_num -= 1
        return str_list
 ```

   **Convert Grammar to Finite Automaton**
   
   <p align="justify"> &ensp;&ensp;&ensp;For each non-terminal state in grammar and each production  associated with that non-terminal,
   the code checks if length of the production is 1 (which means it's a production of  form A -> a,
   where A is a non-terminal and a-terminal). If so, the code adds a transition from  non-terminal state
   to the final state 'X' labeled with the terminal symbol a. Otherwise, the code adds a transition from
   non-terminal state to another state (which may be a non-terminal or the final state 'X') labeled with the
   first symbol of production and going to the second symbol of production. <p>
    
    
```
# Convert grammar to finite automaton
    def grammar_to_fa(self):
        sigma = self.Vt

        # Sets up the states of the finite autom., which is just Vn + the final state.
        q, f = [], 'X'
        q = self.Vn
        q.append(f)

        # Constructs the transition function delta
        q0, delta = self.S, {}
        for state, productions in self.P.items():
            for production in productions:
                if len(production) == 1:
                    production += f
                if state in delta:
                    delta[state].append((production[0], production[1]))
                else:
                    delta[state] = [(production[0], production[1])]

        return finite_automat.Finite_Automat(q, sigma, delta, q0, f)
```

**Finite Automaton Method that checks if an input string can be obtained via state transition**

<p align="justify"> &ensp;&ensp;&ensp;This code defines a method named check_string_meth_1 that takes a string as an argument and checks whether the given string belongs to a finite automaton or not. The finite automaton is represented by a set of states, initial state, final state, and transition rules, which are stored in an object referred to by self. <p>

<p align="justify"> &ensp;&ensp;&ensp;The method first initializes two variables, searched_state and re_string. The searched_state is the current state of the automaton, which starts at the initial state. The re_string is a reconstructed string that is generated based on the transition rules followed by the automaton.The method then iterates through the symbols of the input string one by one. For each symbol, it checks the transition rules of the current state to see if there is a transition that matches the symbol. If there is a match, it updates the searched_state to the new state and appends the symbol to the re_string. If there is no matching transition, the automaton cannot continue, and the method returns that the input string doesn't belong to the finite automaton. <p>

<p align="justify"> &ensp;&ensp;&ensp;The method also checks whether the reconstructed string is the same as the original input string and whether the current state of the automaton is a final state. If both conditions are true, it returns the string "POSSIBLE" in yellow color. Otherwise, it returns a message saying that the input string doesn't belong to the finite automaton. <p>

<p align="justify"> &ensp;&ensp;&ensp; Overall, this method simulates the operation of a finite automaton and checks whether a given input string can be accepted by the automaton or not. <p>

```
    def check_string_meth_1(self, string):
        searched_state, re_string = self.q0, ''

            for production in self.delta[searched_state]:
                if production[0] == symbol:
                    searched_state = production[1]

                    re_string += production[0]
                    break

            # If the current state is a final state, the outer loop is also broken
            if searched_state == self.f:
                break

        if re_string == string and searched_state == self.f:
            return Yellow + 'POSSIBLE' + END
        else:
            return ' (doesnt belong to the finite automata) '
```

**Main Class**

<p align="justify">&ensp;&ensp;&ensp; In the Main Class I defined the grammar, I call the functions and there are some Test Cases for checking if  a word belongs to automata. <p>

```
grammar_Var15 = grammar.Grammar(Vn, Vt, P, 'S')
# Convert the grammar to Finite Automaton
fa = grammar_Var15.grammar_to_fa()
print(Green + '\nPossible Words:' + END)
# Generate 5 strings( function described in grammar.py)
test_cases = grammar_Var15.generate_strings()
```

```
# Test cases if a word belongs to automata
test_cases.append('abcaca')
test_cases.append('baababab')
test_cases.append('cababbc')
test_cases.append('aaaaaaa')
test_cases.append('aab')
test_cases.append('cababbcc')
```


## Conclusions and Results


**Case 1 for:**

```
test_cases.append('abcaca')
test_cases.append('baababab')
test_cases.append('cababbc')
test_cases.append('aaaaaaa')
test_cases.append('aab')
test_cases.append('cababbcc')
```
<img width="319" alt="image" src="https://user-images.githubusercontent.com/113386223/219570264-c5728e1a-468a-46cc-ad79-15ebad5e9cee.png">

**Case 2 for:**
```
test_cases.append('baaca')
test_cases.append('cacaca')
test_cases.append('bababac')
test_cases.append('cccc')
test_cases.append('ababs')
test_cases.append('babaa')
```
<img width="303" alt="image" src="https://user-images.githubusercontent.com/113386223/219570688-4a736e34-6369-41d0-86c1-c776de88604b.png">

<p align="justify">&ensp;&ensp;&ensp; In these photos, we can see the results of our program. So, in the first part with light green, there are the generated words that should be CORRECT( Possible), and in the second part with purple is the Testing part. With blue color are marked all the words that should be checked, and if the word is valid the result will be in Yellow Color, and if the word is not valid, the result will have the default color text (doesn't belong to the finite automata). First, the generated words are checked (which should be correct), and then the words indicated in the program by me. <p>
    
------------------------------------------------------------------------------------------------------------------------

<p align="justify"> &ensp;&ensp;&ensp; In this laboratory work, I worked and got a better understanding of regular grammar, finite automata, and how to convert regular grammar to a finite automaton. I implemented the concept of regular grammar and finite automaton. I learned the way they work and their relationship with each other. I learned to convert regular grammar to a finite automaton and check the corresponding strings through it. So, I implemented a grammar for generating valid (possible) words according to our rules. Secondly, I used Finite Automaton implementation, creating a method that converts an object->Finite Automaton.  </p>

    
  <p align="justify">  &ensp;&ensp;&ensp;Grammar and finite automata are fundamental concepts in computer science and the study of formal languages.By understanding grammar and finite automata, beginners can gain a better understanding of the theoretical foundations of computer science, as well as practical applications of these concepts in software engineering and other related fields. </p>


## References

-   Conversion [online source]: https://www.scirp.org/html/5-9301558_27481.htm
-   Construction of Regular Grammar [online source]: https://mycareerwise.com/content/construction-of-regular-grammar-from-finite-automata
-   Regular grammar (Model regular grammars ) [online source]: https://www.geeksforgeeks.org/regular-grammar-model-regular-grammars/
-   Language by Grammar [online source]: https://www.tutorialspoint.com/automata_theory/language_generated_by_grammars.html
-   Cojuhari I., Duca L., & Fiodorov I. Formal Languages and Finite Automata Guide for practical lessons. Technical University of Moldova