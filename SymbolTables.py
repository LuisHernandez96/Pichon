import pprint

FUNC = "func"
ENV = "env"
MOV = "mov"
RETURN_TYPE = "returnType"
VARS = "vars"

SYMBOL_TABLE = dict()

def SYMBOL_INIT(debug):
    SYMBOL_TABLE[FUNC] = dict()
    SYMBOL_TABLE[ENV] = dict()
    SYMBOL_TABLE[MOV] = dict()

    if(debug):
        pprint.pprint(SYMBOL_TABLE)

def ADD_FUNC(id, returnType, vars, debug):
    if FUNC in SYMBOL_TABLE:
        if id not in SYMBOL_TABLE[FUNC]:
            SYMBOL_TABLE[FUNC][id] = dict()
            SYMBOL_TABLE[FUNC][id][RETURN_TYPE] = returnType
            SYMBOL_TABLE[FUNC][id][VARS] = vars
            if(debug):
                pprint.pprint(SYMBOL_TABLE)
        else:
            print("ERROR, A FUNCTION WITH THE SAME ID ALREADY EXIST")
    else:
        print("ERROR, S_T[FUNC] DOESNT EXIST")
