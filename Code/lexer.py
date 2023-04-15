from token import Token
import re


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def lexer(self):
        tokens = []
        # While the current position is within the text length
        while self.pos < len(self.text):
            current_char = self.text[self.pos]

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
                # If the current character is a letter
            if re.match('^[a-zA-Z]+$', current_char):
                i = self.pos
                st = ""
                # While the next character is a letter, add it to st
                while re.match('^[a-zA-Z]+$', self.text[i]):
                    st += self.text[i]
                    i += 1
                self.pos = i
                # If st is in Token dictionary, append a Token with type from dictionary and value of st
                if st in Token.dictionary:
                    tokens.append(Token(f'{Token.dictionary[st]}', st))
                    # Else, append a Token with type 'IDENTIFIER' and value of st
                else:
                    tokens.append(Token('IDENTIFIER', st))
            elif self.text[self.pos:self.pos + 2] in '&&':
                tokens.append(Token('AND', '&&'))
                self.advance()
            elif current_char in ':':
                tokens.append(Token('COLON', ':'))
                self.advance()
            elif current_char in ',':
                tokens.append(Token('COMMA', ','))
                self.advance()
            elif current_char in '_':
                tokens.append(Token('WORD-SEPARATOR', '_'))
                self.advance()
            elif current_char in '.':
                tokens.append(Token('POINT', '.'))
                self.advance()
            elif current_char in '+':
                tokens.append(Token('PLUS', '+'))
                self.advance()
            elif current_char in '-':
                tokens.append(Token('MINUS', '-'))
                self.advance()
            elif current_char in '*':
                tokens.append(Token('MULTIPLY', '*'))
                self.advance()
            elif current_char in '/':
                tokens.append(Token('DIVIDE', '/'))
                self.advance()
            elif current_char in '=':
                tokens.append(Token('EQUAL', '='))
                self.advance()
            elif current_char in '()':
                tokens.append(Token('PARENTHESIS', self.text[self.pos]))
                self.advance()
            elif current_char in '[]':
                tokens.append(Token('BRACKET', self.text[self.pos]))
                self.advance()
            elif current_char in '$':
                tokens.append(Token('MONEY', '$'))
                self.advance()
            # handle comments
            elif current_char in '#':
                comment = ''
                # loop through the text until a newline character is encountered
                while self.text[self.pos] != '\012':
                    # add each character to the comment string
                    comment += self.text[self.pos]
                    self.pos += 1  # advance past the newline character
                self.pos += 1
                tokens.append(Token('COMMENT', comment))

            else:
                pass
            self.omit_whitespace()  # skip whitespace characters

        return tokens

    def advance(self):
        self.pos += 1

    def omit_whitespace(self):
        for char in self.text[self.pos:]:
            if not char.isspace():
                break
            self.advance()
