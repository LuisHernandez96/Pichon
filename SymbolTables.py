
FUNC = "func"
ENV = "env"
MOV = "mov"
RETURN_TYPE = "returnType"
VARS = "vars"

SYMBOL_TABLE = dict()

def SYMBOL_INIT():
    SYMBOL_TABLE[FUNC] = dict()
    SYMBOL_TABLE[ENV] = dict()
    SYMBOL_TABLE[MOV] = dict()

def ADD_FUNC(id, returnType, vars):
    if FUNC in SYMBOL_TABLE:
        SYMBOL_TABLE[FUNC][id] = dict()
        SYMBOL_TABLE[FUNC][id][RETURN_TYPE] = returnType
        SYMBOL_TABLE[FUNC][id][VARS] = vars
    else:
        print("ERROR, S_T[FUNC] DOESNT EXIST")
