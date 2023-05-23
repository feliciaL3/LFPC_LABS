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



## Implementation description


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





## Conclusions and Results
<p align="justify">&ensp;&ensp;&ensp; <p>


    
## References

-   Cojuhari I., Duca L., & Fiodorov I. Formal Languages and Finite Automata Guide for practical lessons. Technical University of Moldova
