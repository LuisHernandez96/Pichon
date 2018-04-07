import pprint
import sys
import NeededSize as n

FUNC = "FUNCTIONS"
ENV = "ENVIRONMENT"
MOV = "MOVEMENT"
RETURN_TYPE = "returnType"
VARS = "vars"
DATA_TYPE = "data_type"
DATA_TYPE_STRING = "data_type_string"
VALUE = "value"
SIZE = "size"
LIST = "list"
PARAMS = "parameters"
NEEDS = "needs"

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
        SYMBOL_TABLE[FUNC][id][PARAMS] = []
        SYMBOL_TABLE[FUNC][id][NEEDS] = n.NeededSize()
        if(debug):
            pprint.pprint(SYMBOL_TABLE)
    else:
        sys.exit('Error: Function {} already defined!'.format(id))

def ADD_MEMORY(functionID, dataType, amount):
    assert functionID in SYMBOL_TABLE[FUNC].keys()

    # Integers
    if dataType in [0, 4]:
        SYMBOL_TABLE[FUNC][functionID][NEEDS].addInts(amount)
    # Floats (and coordinates)
    elif dataType in [1, 5, 2, 7]:
        SYMBOL_TABLE[FUNC][functionID][NEEDS].addFloats(amount)
    # Booleans
    elif dataType in [3, 6]:
        SYMBOL_TABLE[FUNC][functionID][NEEDS].addFloats(amount)


def ADD_PARAM_FUNCTION(functionID, dataType):
    SYMBOL_TABLE[FUNC][functionID][PARAMS].append(dataType)

def ADD_SCOPE_VARS_TABLE(currentScope):
    SYMBOL_TABLE[currentScope][VARS] = dict()

def VARS_INIT():
    VARS_TABLE = dict()
    return VARS_TABLE

def ADD_VAR(scope, id, data_type, data_type_string, size = None):

    if scope in SYMBOL_TABLE[FUNC].keys():
        if id in SYMBOL_TABLE[FUNC][scope][VARS]:
            sys.exit('Error: Variable {} already defined!'.format(id))
        else:
            SYMBOL_TABLE[FUNC][scope][VARS][id] = dict()
            SYMBOL_TABLE[FUNC][scope][VARS][id][DATA_TYPE] = data_type
            SYMBOL_TABLE[FUNC][scope][VARS][id][DATA_TYPE_STRING] = data_type_string
            SYMBOL_TABLE[FUNC][scope][VARS][id][SIZE] = size
    else:
        if id in SYMBOL_TABLE[scope][VARS]:
            sys.exit('Error: Variable {} already defined!'.format(id))
        else:
            SYMBOL_TABLE[scope][VARS][id] = dict()
            SYMBOL_TABLE[scope][VARS][id][DATA_TYPE] = data_type
            SYMBOL_TABLE[scope][VARS][id][DATA_TYPE_STRING] = data_type_string
            SYMBOL_TABLE[scope][VARS][id][SIZE] = size
