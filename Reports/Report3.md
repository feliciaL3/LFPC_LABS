
# Topic: Lexer & Scanner

### Course: Formal Languages & Finite Automata

### Author: Lupascu Felicia, FAF-212, VAR 15
----------------------------------------------

## Overview
<p align="justify">&ensp;&ensp;&ensp; A lexer, short for lexical analyzer,
is a program component or tool that takes a stream of characters
(such as the source code of a computer program) as input,
and outputs a sequence of tokens,
which are the basic units of meaning in a programming language. <p>

<p align="justify">&ensp;&ensp;&ensp; The task of the lexer is to identify and 
group together the characters of the input stream that form
individual tokens, such as keywords, identifiers, operators, and literals. 
It also typically discards white space and comments,
which are not significant to the meaning of the program.<p>

## Objectives

1.Understand what lexical analysis [1] is.

2.Get familiar with the inner workings of a lexer/scanner/tokenizer.

3.Implement a sample lexer and show how it works.

## Implementation description
<p align="justify">&ensp;&ensp;&ensp;To perform this lab, I created 2 classes  Lexer and   Token  . And I worked with these 2 classes through Main. Also in Main Class I included my input code, where I combined a function and some mathematical stuff.  <p>

### Main
````python3
from lexer import Lexer
text = 
'''
16+2+(3-2)*1/1mm
elif self.text_self = $
$.mdl
#the.input\012
if arr[m] = arr[m+2]:
#comment\012
def magic_function(arr):
    n = len(arr)
    for p in range(n):
'''python3
lexer = Lexer(text)
tokens = lexer.lexer()

for token in tokens:
    print(token)
````

### Token
<p align="justify">&ensp;&ensp;&ensp; Token Class is for representing tokens. This class has a dictionary attribute that maps certain keywords to their corresponding token types. The token types are represented as strings. <p>

````python3
class Token:
    # A dictionary that maps language elements to their corresponding token types.
    dictionary = {
        "%": "MODULO", "_": "WORD-SEPARATOR", "$": "MONEY", ".": "POINT", "&&": "AND", "=": "ASSIGN",
        "assign": "=", "arr": "ARRAY", "def": "FUNCTION", "equal": "==", "elif": "ELIF", "else": "ELSE",
        "False": "BOOLEAN", "float": "FLOAT", "for": "FOR", "if": "IF", "in": "IN", "len": "LEN",
        "not": "NOT", "not_equal": "!=", "or": "OR", "return": "RETURN", "True": "BOOLEAN", "while": "WHILE"
    }
````

 <p align="justify">&ensp;&ensp;&ensp;  The __init__ method is the constructor of the Token class, and it takes two parameters, type and value. type is a string representing the token type, and value is a string representing the actual value of the token. The method initializes a Token object with the given type and value.<p>
<p align="justify">&ensp;&ensp;&ensp;  The __str__ method is used to return a string representation of the Token object. It includes the token type and value in a formatted string that is color-coded using escape sequences. This formatted string is returned as the output of the method. <p>
 
 ### Lexer
<p align="justify">&ensp;&ensp;&ensp; This code defines a lexer class that can convert a given input text into a list of tokens. A token is a lexical unit that represents a specific kind of symbol or sequence of symbols in the input text. <p>

<p align="justify">&ensp;&ensp;&ensp;The lexer works by iterating through the input text character by character and recognizing patterns that match a certain token<p>
    
* <p align="justify">&ensp;&ensp;&ensp; For example, if a sequence of characters matches a regular expression for a number, the lexer will create a "NUMBER" token with the value of that number. <p>
    
````python3
            # If the current character is a digit
            if re.match('^[0-9]+$', current_char):
                i = self.pos
                st = ""
                # While the next character is a digit, add it to st
                while re.match('^[0-9]+$', self.text[i]):
                    st += self.text[i]
                    i += 1
                self.pos = i
                # Append a Token with type 'NUMBER' and integer value of st
                tokens.append(Token('NUMBER', int(st)))
````
    
    
````python3
              # If the current character is a letter
              if re.match('^[a-zA-Z]+$', current_char):
                i = self.pos
                st = ""
                # While the next character is a letter, add it to st
                while re.match('^[a-zA-Z]+$', self.text[i]):
                    st += self.text[i]
                    i += 1
                self.pos = i
                # If st is in Token dictionary,
                # append a Token with type from dictionary and value of st
                if st in Token.dictionary:
                    tokens.append(Token(f'{Token.dictionary[st]}', st))
                    # Else, append a Token with type 'IDENTIFIER' and value of st
                else:
                    tokens.append(Token('IDENTIFIER', st))
````
    

* <p align="justify">&ensp;&ensp;&ensp; The lexer also handles various types of symbols, such as operators (+, -, *, /), parentheses, brackets, and commas. Each symbol is mapped to a specific token type. For example, the "+" symbol is mapped to a "PLUS" token, while the "(" symbol is mapped to a "PARENTHESIS" token. <p>
    
    
````python3

            elif self.text[self.pos:self.pos+2] in '&&':
                tokens.append(Token('AND', '&&'))
                self.advance()
            elif current_char in '_':
                tokens.append(Token('WORD-SEPARATOR', '_'))
                self.advance()
            elif current_char in '.':
                tokens.append(Token('POINT', '.'))
                self.advance()
            elif current_char in '()':
                tokens.append(Token('PARENTHESIS', self.text[self.pos]))
                self.advance()
            elif current_char in '[]':
                tokens.append(Token('BRACKET', self.text[self.pos]))
                self.advance()
````

    
* <p align="justify">&ensp;&ensp;&ensp; In addition, the lexer also handles comments. Any text that follows a "#" character up to the next newline character is considered a comment and is ignored by the lexer. <p>
 
    
````python3
            # handle comments
            elif self.text[self.pos] in '#':
                comment = ''
                # loop through the text until a newline character is encountered
                while self.text[self.pos] != '\012':
                    # add each character to the comment string
                    comment += self.text[self.pos]
                    self.pos += 1  # advance past the newline character
                self.pos += 1
                tokens.append(Token('COMMENT', comment))
````
<p align="justify">&ensp;&ensp;&ensp; Also, there is a a method ``omit_whitespace``. The method works by iterating through the characters in the text starting from the current position (self.pos) and checking whether each character is a whitespace character using the isspace() method. If the character is a whitespace character, the method advances the position of the instance (using the advance() method), effectively skipping over the whitespace character. If the character is not a whitespace character, the loop breaks and the method stops advancing the position. <p>
    
````python3
    def omit_whitespace(self):
        for char in self.text[self.pos:]:
            if not char.isspace():
                break
            self.advance()
````
    


    
<p align="justify">&ensp;&ensp;&ensp; The resulting list of tokens is returned by the lexer() method of the Lexer class. The list contains instances of the Token class, which has two attributes: type (a string that represents the type of the token) and value (the actual value of the token). 
The Token class is defined in another module, which is imported at the beginning of the code. <p>


                                  
## Results 

<p align="justify">&ensp;&ensp;&ensp; The output of the program represents the tokens produced by the lexer when analyzing a given text input. Each token is printed as a separate line with its type and value.There are just parts from the whole output. <p>
            
<img width="198" alt="image" src="https://user-images.githubusercontent.com/113386223/228245372-2ac77c77-15c8-4f75-a03f-99fe9363b399.png">

````python3
TOKEN:  POINT  .
TOKEN:  IDENTIFIER  mdl
TOKEN:  COMMENT  #the.input
TOKEN:  COMMENT  #comment
TOKEN:  FUNCTION  def
TOKEN:  IDENTIFIER  magic
TOKEN:  WORD-SEPARATOR  _
TOKEN:  IDENTIFIER  function
TOKEN:  PARENTHESIS  (
TOKEN:  ARRAY  arr
TOKEN:  PARENTHESIS  )
TOKEN:  COLON  :
TOKEN:  IDENTIFIER  n
TOKEN:  EQUAL  =
TOKEN:  LEN  len
TOKEN:  PARENTHESIS  (
TOKEN:  ARRAY  arr
TOKEN:  PARENTHESIS  )
TOKEN:  FOR  for
````

## Conclusions and Results
<p align="justify">&ensp;&ensp;&ensp; The implemented lexer class successfully tokenizes input text, which can be used in a compiler or interpreter. 
The lexer works by iterating through the input text and returning a list of tokens based on the language elements present in the text. The tokens are represented by a Token class,
which contains a type and value for each token. <p>

<p align="justify">&ensp;&ensp;&ensp; The lexer is able to handle various language elements, such as numbers, identifiers, operators, and special characters.
It can also handle comments and skip over whitespace characters. <p>

<p align="justify">&ensp;&ensp;&ensp; The tokenization process can be improved by adding more language elements to the Token dictionary and implementing a more efficient method for handling the different elements. Overall, the lexer provides a solid foundation for building a compiler or interpreter. <p>


## References

-   "Lexical Analysis with Flex" [online book]: http://westes.github.io/flex/manual/
-   "Writing a Lexer in Python" [blog post]: https://ruslanspivak.com/lsbasi-part1/
-   Cojuhari I., Duca L., & Fiodorov I. Formal Languages and Finite Automata Guide for practical lessons. Technical University of Moldova


