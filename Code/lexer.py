import token as tokens
import re


class Lexer:
    tokens_regex = re.compile("|".join(f"(?P<{name}>{regex})" for name, regex in tokens.tokens.items()))

    def __init__(self, file_name):
        # Initialize the Lexer with the content of the file
        with open(file_name, "r") as file:
            self.content = file.read()

    def tokenize(self):
        # Find all matches of tokens in the content using the tokens_regex pattern
        matches = self.tokens_regex.finditer(self.content)
        tokens = []
        for match in matches:
            token_name = match.lastgroup  # Get the name of the matched token
            token_value = match.group(token_name)  # Get the value of the matched token
            if token_name in ["WHITESPACE", "NEWLINE"]:
                continue  # Skip whitespace and newline tokens
            if token_name == "INVALID":
                raise Exception(f"Invalid token '{token_value}'")  # Raise an exception for invalid tokens
            tokens.append((token_name, token_value))  # Add the token (name, value) pair to the list of tokens
        return tokens
