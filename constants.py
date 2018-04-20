INT = "INT"
FLOAT = "FLOAT"
COORD = "COORD"
BOOLEAN = "BOOLEAN"
INT_LIST = "INT_LIST"
FLOAT_LIST = "FLOAT_LIST"
BOOLEAN_LIST = "BOOLEAN_LIST"
COORD_LIST = "COORD_LIST"
VOID = "VOID"
OBJECT = "OBJECT"
SEMANTIC_ERROR = 99

DATA_TYPES = {
    INT : 0,
    FLOAT : 1,
    COORD : 2,
    BOOLEAN : 3,
    INT_LIST : 4,
    FLOAT_LIST : 5,
    BOOLEAN_LIST : 6,
    COORD_LIST : 7,
    VOID : 8,
    OBJECT : 9
}

OPERATORS = {
    # Arithmetic
    "+" : 0,
    "-" : 1,
    "/" : 2,
    "*" : 3,
    "=" : 4,

    # Relational
    "==" : 5,
    "<" : 6,
    ">" : 7,
    "<=" : 8,
    ">=" : 9,
    "!=" : 10,
    "||" : 11,
    "&&" : 12,

    # Unary
    "!" : 13,
    "~" : 14,
}