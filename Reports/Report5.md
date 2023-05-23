# Topic: Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata

### Author: Lupascu Felicia, FAF-212, VAR 15
----------------------------------------------

## Overview
<p align="justify">&ensp;&ensp;&ensp;An Abstract Syntax Tree (AST) and a parser are vital components within the field of computer science, particularly in the realm of programming languages and compilers. They have pivotal roles in analyzing and interpreting code. <p>

<p align="justify">&ensp;&ensp;&ensp;In simple terms, a parser is a software module that takes source code as input and verifies its syntactic accuracy based on predetermined grammar or language rules. It breaks down the code into a structured format called a parse tree, which illustrates the hierarchical relationship among code elements. Although the parse tree contains all the grammatical details of the code, it may include redundant information.<p>

<p align="justify">&ensp;&ensp;&ensp; To overcome this, an AST is derived from the parse tree. The AST captures the core semantic meaning of the code while eliminating unnecessary details. It serves as a more concise representation that emphasizes the program's structure and logic. The AST takes the form of a tree-like structure, where each node corresponds to a specific construct like a function declaration, an if statement, or an expression. <p>

## Objectives:
* Get familiar with parsing, what it is and how it can be programmed [1].

* Get familiar with the concept of AST [2].

* In addition to what has been done in the 3rd lab work do the following:

* In case you didn't have a type that denotes the possible types of tokens you need to:

* Have a type TokenType (like an enum) that can be used in the lexical analysis to categorize the tokens.

Please use regular expressions to identify the type of the token.

Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.

Implement a simple parser program that could extract the syntactic information from the input text.ures/diagrams.



# Implementation description


<p align="justify">&ensp;&ensp;&ensp; To implement this laboratory work I selected Python language.  <p>

### Main Class

``` python 4
def main():
    parser = Parser("text.txt")
    parser.parse()
    parser.show_ast()
if __name__ == '__main__':
    main()
```

 Inside the ``` main() ``` function, it creates an instance of the Parser class, passing the file name ```"text.txt"``` as a parameter. Then, it calls the ```parse()``` method of the parser object, which parses the content of the file and builds an Abstract Syntax Tree (AST). Finally, it calls the ```show_ast()``` method of the parser object to display the AST. 

### Parser Tree

``` python 4

class parseTree:
    def __init__(self, n_type, value=None, children=None):
        # Initialize a ParseTree node
        self.type = n_type  # Set the type of the node
        self.value = value  # Set the value associated with the node (default: None)
        self.children = children or []  # Set the children nodes of the current node (default: None)
    def __str__(self, level=0):
        # Generate a string representation of the ParseTree
        indent = "\t" * level
        ret = f"{indent}{self.type}"  # Add the type to the string
        if self.value is not None:
            ret += f": [{str(self.value)}]"  # Add the value if it exists
        ret += "\n"
        for child in self.children:
            ret += child.__str__(level + 1)  # Add the string representation of child nodes recursively
        return ret
```

The ParseTree class represents a node in the AST. It has an initializer method ```(__init__)``` that takes a node type ```(n_type)```, an optional value (value), and optional children nodes (children). It initializes these attributes accordingly. The class also has a string representation method```(__str__)``` that generates a string representation of the parseTree and its children recursively.


## Parse Class

The Parser class is responsible for parsing a program and building the AST. It has an initializer method ```(__init__)``` that takes a file path (path) as input. It creates a Lexer instance, tokenizes the program using the Lexer. 

The Parser class also defines several methods for parsing different elements of a program, such as ```parse_block```, ```parse_assignment```, ```parse_expression```, ```parse_statement```, ```parse_term```, ```parse_factor```, ```parse_if_instr```, ```parse_print_instr```, ```parse_comp```. Each of these methods follows specific rules to parse the corresponding program element and populate the AST accordingly. If any parsing error occurs, an exception is raised.

Finally, the Parser class includes a method show_ast that prints the generated AST.

### Parse
```  python
    def parse(self):
        # Parse the program and build the AST
        self.ast = ParseTree("MATHEMATICAL PROCEDURE")  # Create the root node of the AST
        self.parse_block(self.ast)  # Parse the block and populate the AST
```
The method begins by creating the root node of the ```AST``` using the ParseTree class. The root node is given the type "MATHEMATICAL PROCEDURE". The ```ParseTree``` class represents a node in the ```AST``` and allows for the creation of a hierarchical tree structure to represent the program's structure.


### Parse Block
``` python 

    def parse_block(self, parent_node):
        parse_node = ParseTree("BLOCK")
        # Get the token representing the starting block
        starting_block_token = self.tokens[self.index]
        # Check if the current token is a starting block token
        if starting_block_token[0] == "STARTING_BLOCK":
            parse_node.children.append(ParseTree(starting_block_token[0], starting_block_token[1]))
            self.index += 1
            # Parse the statement within the block
            self.parse_statement(parse_node)
            # Get the token representing the ending block
            ending_block_token = self.tokens[self.index]
            # Check if the current token is an ending block token
            if ending_block_token[0] == "ENDING_BLOCK":
                parse_node.children.append(ParseTree(ending_block_token[0], ending_block_token[1]))
                self.index += 1
            else:
                raise Exception("Expected '}'")
        else:
            raise Exception("Expected '{'")
        parent_node.children.append(parse_node)
```

The method is responsible for parsing a block of code and constructing the corresponding nodes in the abstract syntax tree ```(AST)```.The method begins by creating a new ParseTree node with the type ```"BLOCK"```. This node represents the block of code being parsed.Next, it retrieves the current token from the token list based on the current index ```(self.tokens[self.index])```. This token represents the starting block of the code.


### Parse Assignment 
``` python
    def parse_assignment(self, parent_node):
        token_type, token_value = self.tokens[self.index]
        # Check if the current token is an identifier
        if token_type == "IDENTIFIER":
            parent_node.children.append(ParseTree(token_type, token_value))
            self.index += 1
            token_type, token_value = self.tokens[self.index]
            # Check if the next token is the assignment operator '='
            if token_type == "ASSIGNMENT":
                parent_node.children.append(ParseTree(token_type, token_value))
                self.index += 1
                self.parse_expression(parent_node)  # Parse the expression after the assignment operator
            else:
                raise Exception("Expected '=' after identifier")
        else:
            raise Exception("Expected identifier")
```

This code handles the parsing of an assignment statement, including the identifier, assignment operator, and the expression on the right side of the assignment operator. It constructs the corresponding nodes in the ```AST```, ensuring the correct structure and hierarchy of the ```AST``` nodes.


### Parse Statement 

``` python
    def parse_statement(self, parent_node):
        parse_node = ParseTree("STATEMENT")
        # Iterate through the tokens until the end is reached
        while self.index < len(self.tokens):
            token_type = self.tokens[self.index][0]
            # Check the type of the current token
            if token_type == "IDENTIFIER":
                parse_node.children.append(ParseTree("ASSIGNMENT_STATEMENT"))
                self.parse_assignment(parse_node)
            elif token_type == "PRINT":
                self.parse_print_instr(parse_node)
            elif token_type == "IF":
                self.parse_if_instr(parse_node)
            else:
                parent_node.children.append(parse_node)
                break  # Exit the loop when encountering an unrecognized token type
        parent_node.children.append(parse_node)
```

This code defines the parse_statement method within the Parser class. The method is responsible for parsing a statement and constructing the corresponding nodes in the abstract syntax tree ```(AST)```.



## Conclusions and Results
<p align="justify">&ensp;&ensp;&ensp; <p>


    
## References

-   Cojuhari I., Duca L., & Fiodorov I. Formal Languages and Finite Automata Guide for practical lessons. Technical University of Moldova
