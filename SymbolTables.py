import pprint
import sys

FUNC = "FUNCTIONS"
ENV = "ENVIRONMENT"
MOV = "MOVEMENT"
RETURN_TYPE = "returnType"
VARS = "vars"
DATA_TYPE = "data_type"
VALUE = "value"
SIZE = "size"
LIST = "list"

SYMBOL_TABLE = dict()

def SYMBOL_INIT(debug):
    SYMBOL_TABLE[FUNC] = dict()
    SYMBOL_TABLE[ENV] = dict()
    SYMBOL_TABLE[MOV] = dict()

    if(debug):
        pprint.pprint(SYMBOL_TABLE)

def ADD_FUNC(id, returnType, debug = False):
    assert FUNC in SYMBOL_TABLE
    if id not in SYMBOL_TABLE[FUNC]:
        SYMBOL_TABLE[FUNC][id] = dict()
        SYMBOL_TABLE[FUNC][id][RETURN_TYPE] = returnType
        SYMBOL_TABLE[FUNC][id][VARS] = dict()
        if(debug):
            pprint.pprint(SYMBOL_TABLE)
    else:
        sys.exit('Error: Function {} already defined!'.format(id))

def ADD_SCOPE_VARS_TABLE(currentScope):
    SYMBOL_TABLE[currentScope][VARS] = dict()

# def ADD_ENV_VARS(vars, debug):
#     assert ENV in SYMBOL_TABLE
#     SYMBOL_TABLE[ENV][VARS] = vars
#     if (debug):
#         pprint.pprint(SYMBOL_TABLE)
#
# def ADD_MOV_VARS(vars, debug):
#     assert MOV in SYMBOL_TABLE
#     SYMBOL_TABLE[MOV][VARS] = vars
#     if (debug):
#         pprint.pprint(SYMBOL_TABLE)

def VARS_INIT():
    VARS_TABLE = dict()
    return VARS_TABLE

def ADD_VAR(scope, id, data_type, value = None, size = None):
    # if id in scope:
    #     sys.exit('Error: Variable {} already defined!'.format(id))
    # else:
    #     scope[id] = dict()
    #     scope[id][DATA_TYPE] = data_type
    #     scope[id][VALUE] = value
    #     scope[id][SIZE] = size

    if scope in SYMBOL_TABLE[FUNC].keys():
        if id in SYMBOL_TABLE[FUNC][scope][VARS]:
            sys.exit('Error: Variable {} already defined!'.format(id))
        else:
            SYMBOL_TABLE[FUNC][scope][VARS][id] = dict()
            SYMBOL_TABLE[FUNC][scope][VARS][id][DATA_TYPE] = data_type
            SYMBOL_TABLE[FUNC][scope][VARS][id][VALUE] = value
            SYMBOL_TABLE[FUNC][scope][VARS][id][SIZE] = size
    else:
        if id in SYMBOL_TABLE[scope][VARS]:
            sys.exit('Error: Variable {} already defined!'.format(id))
        else:
            SYMBOL_TABLE[scope][VARS][id] = dict()
            SYMBOL_TABLE[scope][VARS][id][DATA_TYPE] = data_type
            SYMBOL_TABLE[scope][VARS][id][VALUE] = value
            SYMBOL_TABLE[scope][VARS][id][SIZE] = size
