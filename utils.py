import constants as constants
import re
import sys
import pprint
import SymbolTables as st
from Memory import memory
from GlobalVars import globals
from SemanticCube import SEMANTIC_CUBE
from cuadruplo import Cuadruplo
import tkinter as tk

REGEX_BOOLEAN = r'true|false'
regex_boolean = re.compile(REGEX_BOOLEAN)

REGEX_INT = r'[0-9][0-9]*'
regex_int = re.compile(REGEX_INT)

REGEX_FLOAT = r'[0-9]*[\.][0-9]+'
regex_float = re.compile(REGEX_FLOAT)

REGEX_OBJECT = r'cube|sphere'
regex_object = re.compile(REGEX_OBJECT)

# Set the current data type
def setDataType(p):
	if (len(p) == 3 and p[2] is None) or len(p) != 3:
		if p[1] == 'int':
			globals.currentDataType = constants.DATA_TYPES[constants.INT]
		elif p[1] == 'boolean':
			globals.currentDataType = constants.DATA_TYPES[constants.BOOLEAN]
		elif p[1] == 'float':
			globals.currentDataType = constants.DATA_TYPES[constants.FLOAT]
		else:
			globals.currentDataType = constants.DATA_TYPES[constants.VOID]
	elif len(p) == 3 and p[2] is not None:
		if p[1] == 'int':
			globals.currentDataType = constants.DATA_TYPES[constants.INT_LIST]
		elif p[1] == 'boolean':
			globals.currentDataType = constants.DATA_TYPES[constants.BOOLEAN_LIST]
		elif p[1] == 'float':
			globals.currentDataType = constants.DATA_TYPES[constants.FLOAT_LIST]

# Check in the semantic cube if the given operator can be used with the two given data types
def isValidResult(operador, tipo_izq, tipo_der = None):
	returnDataType = SEMANTIC_CUBE[tipo_izq][tipo_der if tipo_der != None else constants.DATA_TYPES[constants.VOID]][constants.OPERATORS[operador]]
	if returnDataType == constants.SEMANTIC_ERROR:
		raiseError('Error at line {}: Type mismatch. Can not do {} with {} and {}'.format(globals.lineNumber + 1, operador, tipo_izq, tipo_der))
	return returnDataType

# Get the data type of an ID in a given scope
def getIdDataType(id, scope):
	# We're in a function
	if scope in st.SYMBOL_TABLE[st.FUNC].keys():
		if id in st.SYMBOL_TABLE[st.FUNC][scope][st.VARS]:
			resultType = st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id][st.DATA_TYPE]
		else:
			raiseError('Error at line {}: Variable {} not defined in the following scope: {}.'.format(globals.lineNumber + 1, id, scope))
	else:
		if id in st.SYMBOL_TABLE[scope][st.VARS]:
			resultType = st.SYMBOL_TABLE[scope][st.VARS][id][st.DATA_TYPE]
		else:
			raiseError('Error at line {}: Variable {} not defined in the following scope: {}.'.format(globals.lineNumber + 1, id, scope))
	return resultType

# Get the address of an ID in a given scope. If it hasn't been assigned yet, it is assigned and returned.
def getIdAddress(id, dataType, scope):
	# We're in a function
	if scope in st.SYMBOL_TABLE[st.FUNC].keys():
		size = st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id][st.SIZE]
		if st.ADDRESS in st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id]:
			return st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id][st.ADDRESS]
		else:
			st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id][st.ADDRESS] = memory.ADD_NEW_VAR(dataType, size)
			return st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id][st.ADDRESS]
	else:
		size = st.SYMBOL_TABLE[scope][st.VARS][id][st.SIZE]
		if st.ADDRESS in st.SYMBOL_TABLE[scope][st.VARS][id]:
			return st.SYMBOL_TABLE[scope][st.VARS][id][st.ADDRESS]
		else:
			st.SYMBOL_TABLE[scope][st.VARS][id][st.ADDRESS] = memory.ADD_NEW_VAR(dataType, size)
			return st.SYMBOL_TABLE[scope][st.VARS][id][st.ADDRESS]

# Create a quadruple for binary operations
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
				result = memory.ADD_NEW_VAR(resultType, size = 1)
				st.ADD_MEMORY(globals.currentScope, resultType, 1, True)
				cuad = Cuadruplo(operador, operando_izq, operando_der, result = result, counter = globals.cuadCounter)
				globals.tipos.append(resultType)
				globals.operandos.append(result)

			globals.cuadCounter = globals.cuadCounter + 1
			globals.cuadruplos.append(cuad)

# Create a quadruplo for unary operations
def crearCuadruploUnario(validOperators):
	if(len(globals.operadores) > 0):
		if globals.operadores[-1] in validOperators:
			operando = globals.operandos.pop()
			tipo = globals.tipos.pop()
			operador = globals.operadores.pop()

			resultType = isValidResult(operador, tipo)

			virtualAddress = memory.ADD_NEW_VAR(resultType, size = 1)
			st.ADD_MEMORY(globals.currentScope, resultType, 1, True)
			cuad = Cuadruplo(operador, operand1 = operando, result = virtualAddress, counter = globals.cuadCounter)

			globals.cuadCounter = globals.cuadCounter + 1
			globals.operandos.append(virtualAddress)
			globals.tipos.append(resultType)
			globals.cuadruplos.append(cuad)

# Return a data type representation as a string
def dataTypeToString(dataType, argument = None):
	if dataType == constants.DATA_TYPES[constants.INT]:
		return constants.INT.lower()
	elif dataType == constants.DATA_TYPES[constants.FLOAT]:
		return constants.FLOAT.lower()
	elif dataType == constants.DATA_TYPES[constants.BOOLEAN]:
		return constants.BOOLEAN.lower()
	elif dataType == constants.DATA_TYPES[constants.OBJECT]:
		return str(argument)
	elif dataType == constants.DATA_TYPES[constants.INT_LIST]:
		return st.getDataTypeString(st.getScopeID(st.getIDFromAddress(globals.currentScope, argument), globals.currentScope))
	elif dataType == constants.DATA_TYPES[constants.FLOAT_LIST]:
		return st.getDataTypeString(st.getScopeID(st.getIDFromAddress(globals.currentScope, argument), globals.currentScope))
	elif dataType == constants.DATA_TYPES[constants.BOOLEAN_LIST]:
		return st.getDataTypeString(st.getScopeID(st.getIDFromAddress(globals.currentScope, argument), globals.currentScope))

# Check that the data type of an argument matches the data type defined in the function
def checkFunctionParameter(functionID, argumentDataType, parameterCounter):
	if len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]) > 0 and parameterCounter < len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]):
		if isinstance(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS][parameterCounter], type(regex_object)):
			if not st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS][parameterCounter].match(argumentDataType):
				raiseError("Error at line {}: {} Expected: {} Received: {}.".format(globals.lineNumber + 1, functionID, st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS][parameterCounter].pattern, argumentDataType))
		else:
			if argumentDataType != st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS][parameterCounter]:
				raiseError("Error at line {}: {} Expected: {} Received: {}.".format(globals.lineNumber + 1, functionID, st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS][parameterCounter], argumentDataType))
	elif parameterCounter >= len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]):
		raiseError("Error at line {}: {} expects {} argument(s). ({})".format(globals.lineNumber + 1, functionID, len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]), st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]))

# Check if a function is called with less arguments than the amount needed
def checkIncompleteParameters(functionID, parameterCounter):
	if parameterCounter < len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]):
		raiseError("Error at line {}: {} expects {} argument(s). ({})".format(globals.lineNumber + 1, functionID, len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]), st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS]))

# Create an END PROCEDURE quadruple
def createEndProc():
	cuad = Cuadruplo('ENDPROC', counter = globals.cuadCounter)
	globals.cuadCounter = globals.cuadCounter + 1
	globals.cuadruplos.append(cuad)

# Create and ERA quadruple (expand activation record)
def createERA(functionCalled):
	cuad = Cuadruplo('ERA', operand1 = st.SYMBOL_TABLE[st.FUNC][functionCalled][st.NEEDS], counter = globals.cuadCounter)
	globals.cuadCounter = globals.cuadCounter + 1
	globals.cuadruplos.append(cuad)

# Create a PARAMETER quadruple
def createParam(paramCounter, operand, size):
	cuad = Cuadruplo('PARAMETER', operand, result = '{}{}'.format(paramCounter, '' if size == 0 else '(' + str(size) + ')'), counter = globals.cuadCounter)
	globals.cuadCounter = globals.cuadCounter + 1
	globals.cuadruplos.append(cuad)

# Create a GO SUBROUTINE quadruple
def createGoSub(functionCalled):
	initialAddress = None
	if st.PROC_START in st.SYMBOL_TABLE[st.FUNC][functionCalled]:
		initialAddress = st.SYMBOL_TABLE[st.FUNC][functionCalled][st.PROC_START]
	cuad = Cuadruplo('GOSUB', functionCalled, result = initialAddress, counter = globals.cuadCounter)
	globals.cuadCounter = globals.cuadCounter + 1
	globals.cuadruplos.append(cuad)

# Get the amount of a parameters a function needs
def amountParameters(functionID):
	return len(st.SYMBOL_TABLE[st.FUNC][functionID][st.PARAMS])

# Get the type (None, Environment, Movement) of a function
def getFunctionType(functionID):
	return st.SYMBOL_TABLE[st.FUNC][functionID][st.FUNCTION_TYPE]

# Set the type (None, Environment, Movement) of a function
def setFunctionType(functionID, functionType):
	st.SYMBOL_TABLE[st.FUNC][functionID][st.FUNCTION_TYPE] = functionType

# Check that a function type is consisent
def checkUpdateFunctionType(currentScope, functionCalled):
	functionCalledType = getFunctionType(functionCalled)
	if currentScope == "ENVIRONMENT":
		if functionCalledType == st.MOVEMENT_TYPE:
			raiseError('Error at line {}: Only environment type functions can be called inside ENVIRONMENT.'.format(globals.lineNumber + 1))
	elif currentScope == "MOVEMENT":
		if functionCalledType == st.ENV_TYPE:
			raiseError('Error at line {}: Only movement type functions can be called inside MOVEMENT.'.format(globals.lineNumber + 1))
	else:
		currentFunctionType = getFunctionType(currentScope)
		if currentFunctionType == st.NONE_TYPE:
			setFunctionType(currentScope, functionCalledType)
		elif currentFunctionType == st.MOVEMENT_TYPE and functionCalledType == st.ENV_TYPE:
			raiseError('Error at line {}: A function ({}) can only contain environment type functions or movement type functions, but not both.'.format(globals.lineNumber + 1, currentScope))
		elif currentFunctionType == st.ENV_TYPE and functionCalledType == st.MOVEMENT_TYPE:
			raiseError('Error at line {}: A function ({}) can only contain environment type functions or movement type functions, but not both.'.format(globals.lineNumber + 1, currentScope))

# Reset some global helper variables
def resetGlobalVars():
	globals.currentDataTypeString = ""
	globals.currentId = ''
	globals.currentDataType = -1
	globals.currentSize = 1
	globals.isArr = False
	globals.dimensiones = []

# Check if the dimensions of a Python array matches the dimensions defined for an n-dimensional array
def checkArrayDimensions(arr, dimensions, index):
	if len(arr) != dimensions[index]['sup']:
		return False
	else:
		ret = True
		for elem in arr:
			if isinstance(elem, list):
				if index + 1 >= len(dimensions):
					return False
					
				ret = ret and checkArrayDimensions(elem, dimensions, index + 1)
			elif not isinstance(elem, list) and index + 1 < len(dimensions):
				return False

		return ret

def raiseError(message):
	print(message)
	sys.exit()
