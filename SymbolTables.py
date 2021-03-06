import pprint
import sys
import constants
import NeededSize as n
from utils import raiseError
import re
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
RETURNS = "returns"
MOVEMENT_TYPE = 0
ENV_TYPE = 1
NONE_TYPE = 2

SYMBOL_TABLE = dict()

# Get return type of a given scope
def getReturnType(scope):
    return scope[RETURN_TYPE]

# Get return size of a given scope
def getReturnSize(scope):
    return scope[RETURN_SIZE]

# Get dimensions of a given scope
def getDimensionsID(scope):
    return scope[DIMS]

# Get data type as string of a given scope
def getDataTypeString(scope):
    return scope[DATA_TYPE_STRING]

# Get size of a given scope
def getSize(scope):
    return scope[SIZE]

# Get the variable object of a given scope
def getScopeID(id, currentScope):
    scope = getScope(currentScope)
    scope = scope[VARS][id]
    return scope

# Get the size of a given argument in the given scope
def getArgumentSize(argument, currentScope):
    scope = getScope(currentScope)

    # Constant
    if str(argument)[0] == '%':
        return 0

    for var in scope[VARS]:
        if ADDRESS in scope[VARS][var] and scope[VARS][var][ADDRESS] == argument:
            return scope[VARS][var][SIZE]

    return 0

# Get the scope (object) of the given scope
def getScope(scope):
    if scope in SYMBOL_TABLE[FUNC].keys():
        return SYMBOL_TABLE[FUNC][scope]

    return SYMBOL_TABLE[scope]

# Get dimensions of a variable in the current scope
def getDims(currentScope, id):
    scope = getScope(currentScope)
    if id not in scope[VARS]:
        raiseError('Error at line {}: Variable {} not found in current scope'.format(globals.lineNumber + 1, id))
    else:
        return scope[VARS][id][DIMS]

# Get the ID from an address in the current scope
def getIDFromAddress(currentScope, address):
    scope = getScope(currentScope)
    for var in scope[VARS]:
        if scope[VARS][var][ADDRESS] == address:
            return var

    return False
    # raiseError('Error at line {}: Address {} not found in current scope'.format(globals.lineNumber + 1, address))

# Check if the given address is an array
def checkIfArray(currentScope, address):
    id = getIDFromAddress(currentScope, address)
    dims = getDims(currentScope, id)
    return len(dims) > 0

# Add constant predefined functions to the symbol table
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
            RETURN_TYPE: constants.DATA_TYPES[constants.BOOLEAN],
            RETURN_SIZE : 1,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "isFacingEast" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.BOOLEAN],
            RETURN_SIZE : 1,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "isFacingWest" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.BOOLEAN],
            RETURN_SIZE : 1,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "isFacingSouth" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.BOOLEAN],
            RETURN_SIZE : 1,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "canMoveForward" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.BOOLEAN],
            RETURN_SIZE : 1,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "setMovementSpeed" : {
            PARAMS : ['float'],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "goal" : {
            PARAMS : [re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)')],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : ENV_TYPE
        },
        "start" : {
            PARAMS : [re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)')],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : ENV_TYPE
        },
        "outOfBounds" : {
            PARAMS : [re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)')],
            RETURN_TYPE: constants.DATA_TYPES[constants.BOOLEAN],
            RETURN_SIZE : 1,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "isBlocked" : {
            PARAMS : [re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)')],
            RETURN_TYPE: constants.DATA_TYPES[constants.BOOLEAN],
            RETURN_SIZE : 1,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "isCollectible" : {
            PARAMS : [re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)')],
            RETURN_TYPE: constants.DATA_TYPES[constants.BOOLEAN],
            RETURN_SIZE : 1,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "position" : {
            PARAMS : [],
            RETURN_TYPE: constants.DATA_TYPES[constants.FLOAT_LIST],
            RETURN_SIZE : 3,
            RESERVED : True,
            FUNCTION_TYPE : MOVEMENT_TYPE
        },
        "spawnObject" : {
            PARAMS : [re.compile('cube|sphere'), re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)'), re.compile('(^float+$)|(^int+$)')],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : ENV_TYPE
        },
        "print" : {
            PARAMS : [re.compile('(^float+$)|(^int+$)|(^boolean+$)')],
            RETURN_TYPE: constants.DATA_TYPES[constants.VOID],
            RETURN_SIZE : 0,
            RESERVED : True,
            FUNCTION_TYPE : NONE_TYPE
        },
    }

    SYMBOL_TABLE[FUNC].update(predefined_functions)

# Create static scopes in the symbol table
def SYMBOL_INIT(debug):
    SYMBOL_TABLE[FUNC] = dict()
    SYMBOL_TABLE[ENV] = dict()
    SYMBOL_TABLE[MOV] = dict()

    ADD_PREDEFINED_FUNCTIONS()

    if(debug):
        pprint.pprint(SYMBOL_TABLE)

# Add a function to the Function Directory
def ADD_FUNC(id, returnType, debug = False):
    assert FUNC in SYMBOL_TABLE
    if id not in SYMBOL_TABLE[FUNC]:
        SYMBOL_TABLE[FUNC][id] = dict()
        SYMBOL_TABLE[FUNC][id][RETURN_TYPE] = returnType
        SYMBOL_TABLE[FUNC][id][VARS] = dict()
        SYMBOL_TABLE[FUNC][id][PARAMS] = []
        SYMBOL_TABLE[FUNC][id][PARAMS_ADDRESS] = []
        SYMBOL_TABLE[FUNC][id][RETURNS] = []
        SYMBOL_TABLE[FUNC][id][NEEDS] = n.NeededSize()
        SYMBOL_TABLE[FUNC][id][FUNCTION_TYPE] = NONE_TYPE
        SYMBOL_TABLE[FUNC][id][RESERVED] = False
        if(debug):
            pprint.pprint(SYMBOL_TABLE)
    else:
        raiseError('Error at line {}: Function {} already defined!'.format(globals.lineNumber + 1, id))

# Add an amount of memory in the current scope for a given data type
def ADD_MEMORY(currentScope, dataType, amount, temp):

    scope = getScope(currentScope)

    # Integers
    if dataType in [0, 4]:
        scope[NEEDS].addInts(amount, temp)
    # Floats
    elif dataType in [1, 5]:
        scope[NEEDS].addFloats(amount, temp)
    # Booleans
    elif dataType in [3, 6]:
        scope[NEEDS].addBooleans(amount, temp)

# Add memory for all the variables needed in current scope
def ADD_SCOPE_MEMORY(currentScope):
    scope = getScope(currentScope)
    for var_name in scope[VARS]:
        var = scope[VARS][var_name]
        data_type = var[DATA_TYPE]
        size = var[SIZE]
        ADD_MEMORY(currentScope, data_type, size, False)

# Add a parameter data type to a function
def ADD_PARAM_FUNCTION(functionID, dataType):
    SYMBOL_TABLE[FUNC][functionID][PARAMS].append(dataType)

# Add the virtual address of a parameter to a function
def ADD_PARAM_VIRTUAL_ADDRESS(functionID, virtualAddress):
    SYMBOL_TABLE[FUNC][functionID][PARAMS_ADDRESS].append(virtualAddress)

# Create a new variables table for the current scope
def ADD_SCOPE_VARS_TABLE(currentScope):
    SYMBOL_TABLE[currentScope][VARS] = dict()
    SYMBOL_TABLE[currentScope][NEEDS] = n.NeededSize()

# Set the quadruple where a procedure starts
def SET_START_CUAD(currentScope, start):
    scope = getScope(currentScope)
    scope[PROC_START] = start

# Set the return size of a given function
def ADD_RETURN_SIZE(functionID, size):
    SYMBOL_TABLE[FUNC][functionID][RETURN_SIZE] = size

# Validate that a function has already been defined
def CHECK_FUNCTION_DEFINED(functionID):
    if functionID not in SYMBOL_TABLE[FUNC]:
        raiseError("Error at line {}: Function {} not defined.".format(globals.lineNumber + 1, functionID))

# Create a new variables table
def VARS_INIT():
    VARS_TABLE = dict()
    return VARS_TABLE

# Registe a variable in the variable table of the current scope
def ADD_VAR(currentScope, id, data_type, data_type_string, size = None, dims = []):

    scope = getScope(currentScope)

    if id in scope[VARS]:
        raiseError('Error at line {}: Variable {} already defined!'.format(globals.lineNumber + 1, id))
    else:
        scope[VARS][id] = dict()
        scope[VARS][id][DATA_TYPE] = data_type
        scope[VARS][id][DATA_TYPE_STRING] = data_type_string
        scope[VARS][id][SIZE] = size #if data_type in [4, 5, 6, 7] else 0
        scope[VARS][id][DIMS] = dims

# Get the list of a parameters of a given ID
def GET_PARAMS(id):
    return (SYMBOL_TABLE[FUNC][id][PARAMS])

# Get the list of parameter addresses of a given ID
def GET_PARAMS_ADDRESS(id):
    return (SYMBOL_TABLE[FUNC][id][PARAMS_ADDRESS])

# Add return values to a function
def ADD_RETURN_VALUES(id,value):
    SYMBOL_TABLE[FUNC][id][RETURNS].append(value)