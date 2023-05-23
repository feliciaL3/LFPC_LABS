
tokens = {
    # types
    "INTEGER": u"[0-9]+",
    "FLOAT": r"[0-9]+ \. [0-9]+",
    "DECIMAL": r"[0-9]+(\.[0-9]+)?",  # Updated regular expression for decimal data type
    "STRING": u"\"[^\"]*\"",
    "BOOLEAN": u"true|false",

    # instructions
    "PRINT": u"print", "IF": u"if", "ELSE": u"else", "DELETE": u"del",

    "STARTING_BLOCK": r"\{", "ENDING_BLOCK": r"\}", "NEWLINE": u"\n|\r|\r\n", "WHITESPACE": u"[ ]+",

    # Math Operators
    "ADDITION": r"\+", "SUBTRACTION": u"-", "ASSIGNMENT": u"=",
    "MULTIPLICATION": r"\*", "DIVISION": u"/", "MODULUS": r"\%",

    "RIGHT_PARENTHESIS": r"\)", "LEFT_PARENTHESIS": r"\(",

    # comparison
    "LESS_THAN_OR_EQUAL_TO": u"<=", "EQUAL_TO": u"==", "NOT_EQUAL_TO": u"<>|><|!=",
    "GREATER_THAN": u">", "LESS_THAN": u"<", "GREATER_THAN_OR_EQUAL_TO": u">=",

    # logic
    "OR": r"\|\|", "AND": u"&&",  "NOT": u"!",

    "IDENTIFIER": u"[a-zA-Z_][a-zA-Z0-9_]*",

    # invalid
    "INVALID": u".+"
}
