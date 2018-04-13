import constants as constants
import re
import sys
import SymbolTables as st
from Memory import memory
from GlobalVars import globals
from SemanticCube import SEMANTIC_CUBE
from cuadruplo import Cuadruplo

REGEX_BOOLEAN = r'true|false'
regex_boolean = re.compile(REGEX_BOOLEAN)

REGEX_INT = r'[0-9][0-9]*'
regex_int = re.compile(REGEX_INT)

REGEX_FLOAT = r'[0-9]*[\.][0-9]+'
regex_float = re.compile(REGEX_FLOAT)

def setDataType(p):
	if (len(p) == 3 and p[2] is None) or len(p) != 3:
		if p[1] == 'int':
			globals.currentDataType = constants.DATA_TYPES[constants.INT]
		elif p[1] == 'boolean':
			globals.currentDataType = constants.DATA_TYPES[constants.BOOLEAN]
		elif p[1] == 'coord':
			globals.currentDataType = constants.DATA_TYPES[constants.COORD]
		elif p[1] == 'float':
			globals.currentDataType = constants.DATA_TYPES[constants.FLOAT]
		else:
			globals.currentDataType = constants.DATA_TYPES[constants.VOID]
	elif len(p) == 3 and p[2] is not None:
		if p[1] == 'int':
			globals.currentDataType = constants.DATA_TYPES[constants.INT_LIST]
		elif p[1] == 'boolean':
			globals.currentDataType = constants.DATA_TYPES[constants.BOOLEAN_LIST]
		elif p[1] == 'coord':
			globals.currentDataType = constants.DATA_TYPES[constants.COORD_LIST]
		elif p[1] == 'float':
			globals.currentDataType = constants.DATA_TYPES[constants.FLOAT_LIST]

def isValidResult(operador, tipo_izq, tipo_der = None):
	returnDataType = SEMANTIC_CUBE[tipo_izq][tipo_der if tipo_der != None else constants.DATA_TYPES[constants.VOID]][constants.OPERATORS[operador]]
	if returnDataType == constants.SEMANTIC_ERROR:
		sys.exit('Error at line {}: Type mismatch. Can not do {} with {} and {}'.format(globals.lineNumber + 1, operador, tipo_izq, tipo_der))
	return returnDataType

def getIdDataType(id, scope):
	# We're in a function
	if scope in st.SYMBOL_TABLE[st.FUNC].keys():
		if id in st.SYMBOL_TABLE[st.FUNC][scope][st.VARS]:
			resultType = st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id][st.DATA_TYPE]
		else:
			sys.exit('Error at line {}: Variable {} not defined in the following scope: {}.'.format(globals.lineNumber + 1, id, scope))
	else:
		if id in st.SYMBOL_TABLE[scope][st.VARS]:
			resultType = st.SYMBOL_TABLE[scope][st.VARS][id][st.DATA_TYPE]
		else:
			sys.exit('Error at line {}: Variable {} not defined in the following scope: {}.'.format(globals.lineNumber + 1, id, scope))
	return resultType

def getIdAddress(id, dataType, scope):
	# We're in a function
	if scope in st.SYMBOL_TABLE[st.FUNC].keys():
		if st.ADDRESS in st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id]:
			return st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id][st.ADDRESS]
		else:
			st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id][st.ADDRESS] = memory.ADD_NEW_VAR(dataType)
			return st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id][st.ADDRESS]
	else:
		if st.ADDRESS in st.SYMBOL_TABLE[scope][st.VARS][id]:
			return st.SYMBOL_TABLE[scope][st.VARS][id][st.ADDRESS]
		else:
			st.SYMBOL_TABLE[scope][st.VARS][id][st.ADDRESS] = memory.ADD_NEW_VAR(dataType)
			return st.SYMBOL_TABLE[scope][st.VARS][id][st.ADDRESS]

def crearCuadruploExpresion(validOperators):
	if(len(globals.operadores) > 0):
		if globals.operadores[-1] in validOperators:
			operando_der = globals.operandos.pop()
			operando_izq = globals.operandos.pop()
			tipo_der = globals.tipos.pop()
			tipo_izq = globals.tipos.pop()
			operador = globals.operadores.pop()

			resultType = isValidResult(operador, tipo_izq, tipo_der)

			if operador == '=':
				cuad = Cuadruplo(operador, operand1 = operando_izq, result = operando_der, counter = globals.cuadCounter)
			else:
				result = memory.ADD_NEW_VAR(resultType)
				st.ADD_MEMORY(globals.currentScope, resultType, 1, True)
				cuad = Cuadruplo(operador, operando_izq, operando_der, result = result, counter = globals.cuadCounter)
				globals.tipos.append(resultType)
				globals.operandos.append(result)

			globals.cuadCounter = globals.cuadCounter + 1
			globals.cuadruplos.append(cuad)

def crearCuadruploUnario(validOperators):
	if(len(globals.operadores) > 0):
		if globals.operadores[-1] in validOperators:
			operando = globals.operandos.pop()
			tipo = globals.tipos.pop()
			operador = globals.operadores.pop()

			resultType = isValidResult(operador, tipo)

			virtualAddress = memory.ADD_NEW_VAR("TEMP", resultType)
			st.ADD_MEMORY(globals.currentScope, resultType, 1, True)
			cuad = Cuadruplo(operador, operand1 = operando, result = result, counter = globals.cuadCounter)

			globals.cuadCounter = globals.cuadCounter + 1
			globals.operandos.append(result)
			globals.tipos.append(resultType)
			globals.cuadruplos.append(cuad)

def dataTypeToString(dataType):
	if dataType == constants.DATA_TYPES[constants.INT]:
		return constants.INT.lower()
	elif dataType == constants.DATA_TYPES[constants.FLOAT]:
		return constants.FLOAT.lower()
	elif dataType == constants.DATA_TYPES[constants.BOOLEAN]:
		return constants.BOOLEAN.lower()

def checkFunctionParameter(functionID, argumentDataType, parameterCounter):
	if len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]) > 0 and parameterCounter < len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]):
		if argumentDataType != st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS][parameterCounter]:
			sys.exit("Error at line {}: {} Expected: {} Received: {}.".format(globals.lineNumber + 1, functionID, st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS][parameterCounter], argumentDataType))
	elif parameterCounter >= len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]):
		sys.exit("Error at line {}: {} expects {} argument(s). ({})".format(globals.lineNumber + 1, functionID, len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]), st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]))

def checkIncompleteParameters(functionID, parameterCounter):
	if parameterCounter < len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]):
		sys.exit("Error at line {}: {} expects {} argument(s). ({})".format(globals.lineNumber + 1, functionID, len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]), st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]))

def createEndProc():
	cuad = Cuadruplo('ENDPROC', counter = globals.cuadCounter)
	globals.cuadCounter = globals.cuadCounter + 1
	globals.cuadruplos.append(cuad)

def createERA(functionCalled):
	cuad = Cuadruplo('ERA', operand1 = st.SYMBOL_TABLE[st.FUNC][functionCalled][st.NEEDS], counter = globals.cuadCounter)
	globals.cuadCounter = globals.cuadCounter + 1
	globals.cuadruplos.append(cuad)

def createParam(paramCounter, operand):
	cuad = Cuadruplo('PARAMETER', operand, result = 'PARAM{}'.format(paramCounter), counter = globals.cuadCounter)
	globals.cuadCounter = globals.cuadCounter + 1
	globals.cuadruplos.append(cuad)

def createGoSub(functionCalled):
	initialAddress = st.SYMBOL_TABLE[st.FUNC][functionCalled][st.PROC_START]
	cuad = Cuadruplo('GOSUB', functionCalled, result = initialAddress, counter = globals.cuadCounter)
	globals.cuadCounter = globals.cuadCounter + 1
	globals.cuadruplos.append(cuad)

def getFunctionType(functionID):
	return st.SYMBOL_TABLE[st.FUNC][functionID][st.FUNCTION_TYPE]

def setFunctionType(functionID, functionType):
	st.SYMBOL_TABLE[st.FUNC][functionID][st.FUNCTION_TYPE] = functionType

def checkUpdateFunctionType(currentScope, functionCalled):
	functionCalledType = getFunctionType(functionCalled)
	if currentScope == "ENVIRONMENT":
		if functionCalledType == st.MOVEMENT_TYPE:
			sys.exit('Error at line {}: Only environment type functions can be called inside ENVIRONMENT.'.format(globals.lineNumber + 1))
	elif currentScope == "MOVEMENT":
		if functionCalledType == st.ENV_TYPE:
			sys.exit('Error at line {}: Only movement type functions can be called inside MOVEMENT.'.format(globals.lineNumber + 1))
	else:
		currentFunctionType = getFunctionType(currentScope)
		if currentFunctionType == st.NONE_TYPE:
			setFunctionType(currentScope, functionCalledType)
		elif currentFunctionType == st.MOVEMENT_TYPE and functionCalledType == st.ENV_TYPE:
			sys.exit('Error at line {}: A function ({}) can only contain environment type functions or movement type functions, but not both.'.format(globals.lineNumber + 1, currentScope))
		elif currentFunctionType == st.ENV_TYPE and functionCalledType == st.MOVEMENT_TYPE:
			sys.exit('Error at line {}: A function ({}) can only contain environment type functions or movement type functions, but not both.'.format(globals.lineNumber + 1, currentScope))

	
