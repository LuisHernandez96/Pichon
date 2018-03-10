
FUNC = "func"
ENV = "env"
MOV = "mov"
RETURN_TYPE = "returnType"
VARS = "vars"
DATA_TYPE = "data_type"
VALUE = "value"
SIZE = "size"
LIST = "list"

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

def VARS_INIT():
	VARS_TABLE = dict()
	return VARS_TABLE

def ADD_VAR(vars_table, id, data_type, value = None, size = None, isList = False):
	if id in vars_table:
		print("ERROR: " + id + " ALREADY DEFINED")
	else:
		vars_table[id] = dict()
		vars_table[DATA_TYPE] = data_type
		vars_table[VALUE] = value
		vars_table[LIST] = isList;
		vars_table[SIZE] = size