# Color for text output
DARKCYAN = '\033[36m'
Blue = '\033[94m'
BOLD = '\033[1m'
END = '\033[0m'


class Token:
    # A dictionary that maps language elements to their corresponding token types.
    dictionary = {
        "%": "MODULO", "_": "WORD-SEPARATOR", "$": "MONEY", ".": "POINT", "&&": "AND", "=": "ASSIGN",
        "assign": "=", "arr": "ARRAY", "def": "FUNCTION", "equal": "==", "elif": "ELIF", "else": "ELSE",
        "False": "BOOLEAN", "float": "FLOAT", "for": "FOR", "if": "IF", "in": "IN", "len": "LEN", "range": "RANGE",
        "not": "NOT", "not_equal": "!=", "or": "OR", "return": "RETURN", "True": "BOOLEAN", "while": "WHILE"
    }

    # The __init__ method initializes a Token object with a type and value.
    def __init__(self, type, value):
        self.type = type
        self.value = value

    # It returns a string representation of the object, including the token type and value, with color-coded output.
    def __str__(self):
        return f'{BOLD}{DARKCYAN}TOKEN: {END} {self.type} {Blue} {self.value}{END}'
