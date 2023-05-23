from lexer import Lexer


class ParseTree:
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
            ret += f": {str(self.value)}"  # Add the value if it exists
        ret += "\n"
        for child in self.children:
            ret += child.__str__(level + 1)  # Add the string representation of child nodes recursively
        return ret


class Parser:
    def __init__(self, path):
        # Initialize the Parser with the given path
        lexer = Lexer(path)  # Create a Lexer instance
        self.tokens = lexer.tokenize()  # Tokenize the program using the Lexer
        self.index = 0  # Set the current token index
        self.ast = None  # Initialize the abstract syntax tree (AST)

    def parse(self):
        # Parse the program and build the AST
        self.ast = ParseTree("MATHEMATICAL PROCEDURE")  # Create the root node of the AST
        self.parse_block(self.ast)  # Parse the block and populate the AST

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

    def parse_expression(self, parent_node):
        parse_node = ParseTree("EXPRESSION")
        self.parse_term(parse_node)
        token_type, token_value = self.tokens[self.index]
        # Check if the current token is an addition or subtraction operator
        if token_type in ["ADDITION", "SUBTRACTION"]:
            parse_node.children.append(ParseTree(token_type, token_value))
            self.index += 1
            self.parse_expression(parse_node)  # Recursive call to parse the remaining expression
        parent_node.children.append(parse_node)

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

    def parse_term(self, parent_node):
        self.parse_factor(parent_node)  # Parse the factor
        # Check if the current token is a multiplication or division operator
        if self.tokens[self.index][0] in ["MULTIPLICATION", "DIVISION"]:
            parent_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
            self.index += 1
            self.parse_term(parent_node)  # Recursive call to parse the remaining term

    def parse_factor(self, parent_node):
        # Get the type and value of the current token
        token_type, token_value = self.tokens[self.index]
        # Check if the current token is a left parenthesis
        if token_type == "LEFT_PARENTHESIS":
            parent_node.children.append(ParseTree(token_type, token_value))
            self.index += 1
            self.parse_expression(parent_node)  # Parse the expression within the parentheses
            token_type, token_value = self.tokens[self.index]
            # Check if the current token is a right parenthesis
            if token_type == "RIGHT_PARENTHESIS":
                parent_node.children.append(ParseTree(token_type, token_value))
                self.index += 1
            else:
                raise Exception("Expected ')'")
        # Check if the current token is an integer, float, or identifier
        elif token_type in ["INTEGER", "FLOAT", "IDENTIFIER"]:
            parent_node.children.append(ParseTree(token_type, token_value))
            self.index += 1
        # If none of the above conditions are met, raise an exception
        else:
            raise Exception("Expected factor")

    def parse_if_instr(self, parent_node):
        parse_node = ParseTree("IF_STATEMENT")
        # Check if the current token is 'IF'
        if self.tokens[self.index][0] == "IF":
            self.index += 1
            # Check if the next token is a left parenthesis
            if self.tokens[self.index][0] == "LEFT_PARENTHESIS":
                parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
                self.index += 1
                self.parse_comp(parse_node)  # Parse the comparison within the 'if' statement
                if self.tokens[self.index][0] == "RIGHT_PARENTHESIS":
                    parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
                    self.index += 1
                    self.parse_block(parse_node)  # Parse the block within the 'if' statement
                    if self.tokens[self.index][0] == "ELSE":
                        parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
                        self.index += 1
                        self.parse_block(parse_node)
                else:
                    raise Exception("Expected ')'")
            else:
                raise Exception("Expected '('")
        else:
            raise Exception("Expected 'if'")
        parent_node.children.append(parse_node)

    def parse_print_instr(self, parent_node):
        parse_node = ParseTree("PRINT_STATEMENT")
        # Check if the current token is 'PRINT'
        if self.tokens[self.index][0] == "PRINT":
            self.index += 1
            # Check if the next token is '('
            if self.tokens[self.index][0] == "LEFT_PARENTHESIS":
                parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
                self.index += 1
                # Parse the expression within the print statement
                self.parse_expression(parse_node)
                # Check if the next token is ')'
                if self.tokens[self.index][0] == "RIGHT_PARENTHESIS":
                    parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
                    self.index += 1
                else:
                    raise Exception("Expected ')'")  # Raise an exception if ')' is expected but not found
            else:
                raise Exception("Expected '('")  # Raise an exception if '(' is expected but not found
        else:
            raise Exception("Expected 'print'")  # Raise an exception if 'print' is expected but not found
        parent_node.children.append(parse_node)

    def parse_comp(self, parent_node):
        parse_node = ParseTree("COMPARISON")
        self.parse_expression(parse_node)         # Parse the left side of the comparison expression
        # Define the list of valid comparison operators
        comparison_operators = ["EQUAL", "NOT_EQUAL", "LESS_THAN", "LESS_THAN_OR_EQUAL", "GREATER_THAN",
                                "GREATER_THAN_OR_EQUAL"]
        # Check if the current token is a valid comparison operator
        if self.tokens[self.index][0] in comparison_operators:
            parse_node.children.append(ParseTree(self.tokens[self.index][0], self.tokens[self.index][1]))
            self.index += 1
            self.parse_expression(parse_node)  # Parse the right side of the comparison expression
        else:
            raise Exception("Expected a comparison operator")
        parent_node.children.append(parse_node)

    def show_ast(self):
        print(self.ast)
