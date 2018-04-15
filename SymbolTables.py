import pprint
import sys
import constants
import NeededSize as n
from GlobalVars import globals

FUNC = "FUNCTIONS"
ENV = "ENVIRONMENT"
MOV = "MOVEMENT"
RETURN_TYPE = "returnType"
RETURN_SIZE = "returnSize"
VARS = "vars"
DATA_TYPE = "data_type"
DATA_TYPE_STRING = "data_type_string"
VALUE = "value"
DIMS = "dimensions"
SIZE = "size"
LIST = "list"
PARAMS = "parameters"
PARAMS_ADDRESS = "parameters_address"
NEEDS = "needs"
PROC_START = "proc_start"
ADDRESS = "address"
RESERVED = "reserved"
FUNCTION_TYPE = "function_type"
MOVEMENT_TYPE = 0
ENV_TYPE = 1
NONE_TYPE = 2

SYMBOL_TABLE = dict()

def getReturnType(scope):
    return scope[RETURN_TYPE]

def getReturnSize(scope):
    return scope[RETURN_SIZE]

def getDimensionsID(scope):
    return scope[DIMS]

def getDataTypeString(scope):
    return scope[DATA_TYPE_STRING]

def getScopeID(id, currentScope):
    scope = getScope(currentScope)
    scope = scope[VARS][id]
    return scope

def getScope(scope):
    if scope in SYMBOL_TABLE[FUNC].keys():
        return SYMBOL_TABLE[FUNC][scope]

    return SYMBOL_TABLE[scope]

def ADD_PREDEFINED_FUNCTIONS():
    predefined_functions = {
        "down" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "up" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "forward" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "turnLeft" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "turnRight" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "isFacingNorth" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "isFacingEast" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "isFacingWest" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "isFacingSouth" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "canMoveForward" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "envSize" : {
            PARAMS : ['int', 'int', 'int'],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : ENV_TYPE
        },
        "setMovementSpeed" : {
            PARAMS : ['float'],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        }
    }

    SYMBOL_TABLE[FUNC].update(predefined_functions)

def SYMBOL_INIT(debug):
    SYMBOL_TABLE[FUNC] = dict()
    SYMBOL_TABLE[ENV] = dict()
    SYMBOL_TABLE[MOV] = dict()

    ADD_PREDEFINED_FUNCTIONS()

    if(debug):
        pprint.pprint(SYMBOL_TABLE)

def ADD_FUNC(id, returnType, debug = False):
    assert FUNC in SYMBOL_TABLE
    if id not in SYMBOL_TABLE[FUNC]:
        SYMBOL_TABLE[FUNC][id] = dict()
        SYMBOL_TABLE[FUNC][id][RETURN_TYPE] = returnType
        SYMBOL_TABLE[FUNC][id][VARS] = dict()
        SYMBOL_TABLE[FUNC][id][PARAMS] = []
        SYMBOL_TABLE[FUNC][id][PARAMS_ADDRESS] = []
        SYMBOL_TABLE[FUNC][id][NEEDS] = n.NeededSize()
        SYMBOL_TABLE[FUNC][id][FUNCTION_TYPE] = NONE_TYPE
        if(debug):
            pprint.pprint(SYMBOL_TABLE)
    else:
        sys.exit('Error at line {}: Function {} already defined!'.format(globals.lineNumber + 1, id))

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

def ADD_PARAM_VIRTUAL_ADDRESS(functionID, virtualAddress):
    SYMBOL_TABLE[FUNC][functionID][PARAMS_ADDRESS].append(virtualAddress)

def ADD_SCOPE_VARS_TABLE(currentScope):
    SYMBOL_TABLE[currentScope][VARS] = dict()
    SYMBOL_TABLE[currentScope][NEEDS] = n.NeededSize()

def SET_START_CUAD(currentScope, start):
    scope = getScope(currentScope)
    scope[PROC_START] = start

def ADD_RETURN_SIZE(functionID, size):
    SYMBOL_TABLE[FUNC][functionID][RETURN_SIZE] = size

def CHECK_FUNCTION_DEFINED(functionID):
    if functionID not in SYMBOL_TABLE[FUNC]:
        sys.exit("Error at line {}: Function {} not defined.".format(globals.lineNumber + 1, functionID))

def VARS_INIT():
    VARS_TABLE = dict()
    return VARS_TABLE

def ADD_VAR(currentScope, id, data_type, data_type_string, size = None, dims = []):

    scope = getScope(currentScope)

    if id in scope[VARS]:
        sys.exit('Error at line {}: Variable {} already defined!'.format(globals.lineNumber + 1, id))
    else:
        scope[VARS][id] = dict()
        scope[VARS][id][DATA_TYPE] = data_type
        scope[VARS][id][DATA_TYPE_STRING] = data_type_string
        scope[VARS][id][SIZE] = size
        scope[VARS][id][DIMS] = dims

def getDims(currentScope, id):
    scope = getScope(currentScope)

    if id not in scope[VARS]:
        sys.exit('Error at line {}: Variable {} not found in current scope'.format(globals.lineNumber + 1, id))
    else:
        return scope[VARS][id][DIMS]

def getIDFromAddress(currentScope, address):
    scope = getScope(currentScope)

    for var in scope[VARS]:
        if scope[VARS][var][ADDRESS] == address:
            return var

    sys.exit('Error at line {}: Address {} not found in current scope'.format(globals.lineNumber + 1, address))

