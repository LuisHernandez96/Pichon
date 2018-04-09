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
PROC_START = "proc_start"

SYMBOL_TABLE = dict()

def getScope(scope):
    if scope in SYMBOL_TABLE[FUNC].keys():
        return SYMBOL_TABLE[FUNC][scope]

    return SYMBOL_TABLE[scope]

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

def ADD_MEMORY(currentScope, dataType, amount, temp):

    scope = getScope(currentScope)

    # Integers
    if dataType in [0, 4]:
        scope[NEEDS].addInts(amount, temp)
    # Floats (and coordinates)
    elif dataType in [1, 5, 2, 7]:
        scope[NEEDS].addFloats(amount, temp)
    # Booleans
    elif dataType in [3, 6]:
        scope[NEEDS].addBooleans(amount, temp)

def ADD_SCOPE_MEMORY(currentScope):
    scope = getScope(currentScope)
    for var_name in scope[VARS]:
        var = scope[VARS][var_name]
        data_type = var[DATA_TYPE]
        size = var[SIZE]
        ADD_MEMORY(currentScope, data_type, size, False)

def ADD_PARAM_FUNCTION(functionID, dataType):
    SYMBOL_TABLE[FUNC][functionID][PARAMS].append(dataType)

def ADD_SCOPE_VARS_TABLE(currentScope):
    SYMBOL_TABLE[currentScope][VARS] = dict()
    SYMBOL_TABLE[currentScope][NEEDS] = n.NeededSize()

def SET_START_CUAD(currentScope, start):
    scope = getScope(currentScope)
    scope[PROC_START] = start

def CHECK_FUNCTION_DEFINED(functionID):
    if functionID not in SYMBOL_TABLE[FUNC]:
        sys.exit("Error: Function {} not defined.".format(functionID))

def VARS_INIT():
    VARS_TABLE = dict()
    return VARS_TABLE

def ADD_VAR(currentScope, id, data_type, data_type_string, size = None):

    scope = getScope(currentScope)

    if id in scope[VARS]:
        sys.exit('Error: Variable {} already defined!'.format(id))
    else:
        scope[VARS][id] = dict()
        scope[VARS][id][DATA_TYPE] = data_type
        scope[VARS][id][DATA_TYPE_STRING] = data_type_string
        scope[VARS][id][SIZE] = size
