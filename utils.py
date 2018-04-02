import constants as constants
import re
import sys
import SymbolTables as st
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
		sys.exit('Error: Type mismatch. Can not do {} with {} and {}'.format(operador, tipo_izq, tipo_der))
	return returnDataType

def getIdDataType(id, scope):
	# We're in a function
	if scope in st.SYMBOL_TABLE[st.FUNC].keys():
		if id in st.SYMBOL_TABLE[st.FUNC][scope][st.VARS]:
			resultType = st.SYMBOL_TABLE[st.FUNC][scope][st.VARS][id][st.DATA_TYPE]
		else:
			sys.exit('Error: Variable {} not defined in the following scope: {}.'.format(id, scope))
	else:
		if id in st.SYMBOL_TABLE[scope][st.VARS]:
			resultType = st.SYMBOL_TABLE[scope][st.VARS][id][st.DATA_TYPE]
		else:
			sys.exit('Error: Variable {} not defined in the following scope: {}.'.format(id, scope))
	return resultType

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
				result = globals.nextTmp()
				cuad = Cuadruplo(operador, operando_izq, operando_der, result = result, counter = globals.cuadCounter)
				globals.operandos.append(result)

			globals.cuadCounter = globals.cuadCounter + 1
			globals.tipos.append(resultType)
			globals.cuadruplos.append(cuad)

def crearCuadruploUnario(validOperators):
	if(len(globals.operadores) > 0):
		if globals.operadores[-1] in validOperators:
			operando = globals.operandos.pop()
			tipo = globals.tipos.pop()
			operador = globals.operadores.pop()

			resultType = isValidResult(operador, tipo)

			result = globals.nextTmp()
			cuad = Cuadruplo(operador, operand1 = operando, result = result, counter = globals.cuadCounter)

			globals.cuadCounter = globals.cuadCounter + 1
			globals.operandos.append(result)
			globals.tipos.append(resultType)
			globals.cuadruplos.append(cuad)