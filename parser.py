import SymbolTables as st
import sys
from utils import *

# Precedence rules for the arithmetic operators
precedence = (
	('left','PLUS','MINUS'),
	('left','MULT','DIVISION'),
	('right', 'NOT')
)

def p_start(p):
	'''start : func_sec env_sec mov_sec'''
	print("Finished!")

def p_func_sec(p):
	'''func_sec : FUNCTIONS L_BRACE func_sec1 R_BRACE'''

def p_func_sec1(p):
	'''func_sec1 : functions func_sec1
		| empty'''

def p_functions(p):
	'''functions : FUNCTION tipo ID create_function_vars_table L_PAREN functions1 R_PAREN L_BRACE vars bloque functions2 R_BRACE'''

def p_create_function_vars_table(p):
	'''create_function_vars_table :'''
	globals.currentVarsTable = st.VARS_INIT()
	globals.currentScope = p[-1]
	if globals.currentScope not in st.SYMBOL_TABLE.keys():
		st.ADD_FUNC(p[-1], p[-2])
	else:
		st.ADD_SCOPE_VARS_TABLE(globals.currentScope)

def p_functions1(p):
	'''functions1 : params
				   | empty '''
def p_fucntions2(p):
	'''functions2 : return
				   | empty'''

def p_env_sec(p):
	'''env_sec : ENVIRONMENT create_function_vars_table L_BRACE vars bloque R_BRACE'''

def p_mov_sec(p):
	'''mov_sec : MOVEMENT create_function_vars_table L_BRACE vars bloque R_BRACE'''

def p_tipo(p):
	'''tipo : INT tipo1
			| BOOLEAN tipo1
			| COORD tipo1
			| FLOAT tipo1
			| VOID'''
	setDataType(p)

	# Avoid pushing in the stack function return types
	p[0] = globals.currentDataType

def p_tipo1(p):
	'''tipo1 : L_BRACKET tipo2 R_BRACKET return_list
			  | empty'''
	if len(p) == 5:
		p[0] = {'isList' : p[4], 'listSize' : p[2]}
	else:
		p[0] = None

def p_return_list(p):
	'''return_list : '''
	p[0] = True

def p_tipo2(p):
	'''tipo2 : CTE_I return_int
			  | empty'''
	if len(p) == 3:
		p[0] = p[2]
		globals.currentSize = p[1]
	else:
		p[0] = None
		globals.currentSize = None

def p_return_int(p):
	'return_int : '
	p[0] = p[-1]

def p_params(p):
	'''params : tipo ID add_var params1'''

def p_add_var(p):
	'add_var :'
	st.ADD_VAR(globals.currentScope, globals.currentId, globals.currentDataType, size = globals.currentSize)
	globals.currentId = ''
	globals.currentDataType = -1
	globals.currentSize = None

def p_params1(p):
	'''params1 : COMMA params
				| empty'''

def p_bloque(p):
	'''bloque : estatutos bloque
			   | empty'''

def p_vars(p):
	'''vars : declaracion SEMICOLON vars
		| inicializacion SEMICOLON vars
		| empty'''

def p_list(p):
	'''list : L_BRACE expresion list1 R_BRACE'''

def p_list1(p):
	'''list1 : COMMA expresion list1
			  | empty'''

def p_return(p):
	'''return : RETURN expresion SEMICOLON'''

def p_condicion(p):
	'''condicion : cond_add_lid IF L_PAREN expresion cond_check_bool push_goto_false R_PAREN L_BRACE bloque R_BRACE cond_replace_none_1 condicion1 cond_remove_lid'''

def p_condicion1(p):
	'''condicion1 : push_goto ELSE L_BRACE bloque R_BRACE cond_replace_none_0
		| push_goto ELIF L_PAREN expresion cond_check_bool push_goto_false R_PAREN L_BRACE bloque R_BRACE cond_replace_none_1 condicion1
		| empty'''

def p_cond_add_lid(p):
	'''cond_add_lid : '''
	globals.saltos.append('*')

def p_cond_remove_lid(p):
	'''cond_remove_lid : '''
	globals.saltos.pop()

def p_cond_check_bool(p):
	'''cond_check_bool : '''
	globals.operadores.pop()
	if globals.tipos[-1] != constants.DATA_TYPES[constants.BOOLEAN]:
		sys.exit('Error: Type mismatch. IF/ELIF expression has to be boolean'.format(p))

def p_cond_replace_none_1(p):
	'''cond_replace_none_1 : '''
	goto = globals.saltos.pop()
	globals.cuadruplos[goto].result = globals.cuadCounter+1

def p_cond_replace_none_0(p):
	'''cond_replace_none_0 : '''
	while globals.saltos[-1]!='*':
		goto = globals.saltos.pop()
		globals.cuadruplos[goto].result = globals.cuadCounter

def p_while_loop(p):
	'''while_loop : WHILE push_quad_jump L_PAREN expresion push_goto_false R_PAREN L_BRACE bloque R_BRACE'''
	end = globals.saltos.pop()
	ret = globals.saltos.pop()
	cuad = Cuadruplo('GOTO', result = ret, counter = globals.cuadCounter)
	globals.cuadCounter += 1
	globals.cuadruplos[end].result = globals.cuadCounter
	globals.cuadruplos.append(cuad)

def p_push_gotofalse(p):
	'''push_goto_false :'''
	cuad = Cuadruplo('GOTO_FALSE', operand1 = globals.prevTmp(), counter = globals.cuadCounter)
	globals.saltos.append(globals.cuadCounter)
	globals.cuadruplos.append(cuad)
	globals.cuadCounter += 1

def p_push_quad_jump(p):
	'''push_quad_jump :'''
	globals.saltos.append(globals.cuadCounter)

def p_for_loop(p):
	'''for_loop : FOR L_PAREN asignacion SEMICOLON push_quad_jump expresion cuads_true_false SEMICOLON push_quad_jump asignacion push_goto R_PAREN L_BRACE push_quad_jump bloque push_goto R_BRACE'''
	goToBlockEnd = globals.saltos.pop()
	blockStart = globals.saltos.pop()
	stepGoTo = globals.saltos.pop()
	stepStart = globals.saltos.pop()
	goToFalseCondition = globals.saltos.pop()
	goToTrueCondition = globals.saltos.pop()
	conditionStart = globals.saltos.pop()

	globals.cuadruplos[goToBlockEnd].result = stepStart
	globals.cuadruplos[stepGoTo].result = conditionStart
	globals.cuadruplos[goToTrueCondition].result = blockStart
	globals.cuadruplos[goToFalseCondition].result = globals.cuadCounter

def p_push_goto(p):
	'''push_goto :'''
	cuad = Cuadruplo('GOTO', counter = globals.cuadCounter)
	globals.saltos.append(globals.cuadCounter)
	globals.cuadruplos.append(cuad)
	globals.cuadCounter += 1

def p_cuads_true_false(p):
	'''cuads_true_false :'''
	cuad_true = Cuadruplo('GOTO_TRUE', operand1 = globals.prevTmp(), counter = globals.cuadCounter)
	globals.saltos.append(globals.cuadCounter)
	globals.cuadruplos.append(cuad_true)
	globals.cuadCounter += 1
	cuad_false = Cuadruplo('GOTO_FALSE', operand1 = globals.prevTmp(), counter = globals.cuadCounter)
	globals.saltos.append(globals.cuadCounter)
	globals.cuadruplos.append(cuad_false)
	globals.cuadCounter += 1

def p_var_cte(p):
	'''var_cte : ID push_operand_stack var_cte1
		| func_call var_cte1
		| coord var_cte1
		| list var_cte1
		| CTE_I push_constant_operand_stack
		| CTE_F push_constant_operand_stack
		| TRUE push_constant_operand_stack
		| FALSE push_constant_operand_stack
		| CUBE
		| SPHERE
	'''

def p_var_cte1(p):
	'''var_cte1 : L_BRACKET expresion R_BRACKET
		| empty
	'''

def p_expresion(p):
	'''expresion : push_open_paren logical_or pending_or expresion2'''

def p_pending_or(p):
	'''pending_or :'''
	crearCuadruploExpresion(validOperators = ['||'])

def p_logical_or(p):
	'''logical_or : logical_and pending_and logical_or1'''

def p_pending_and(p):
	'''pending_and :'''
	crearCuadruploExpresion(validOperators = ['&&'])

def p_logical_or1(p):
	'''logical_or1 : OR push_operator_stack logical_or
					| empty

	'''

def p_logical_and(p):
	'''
		logical_and : exp logical_and1
	'''

def p_logical_and1(p):
	'''logical_and1 : AND push_operator_stack logical_and
					| empty
	'''

def p_expresion2(p):
	'''expresion2 : operators exp
		| empty
	'''
	if len(p) == 3:
		crearCuadruploExpresion(validOperators = ['<', '>', '<=', '>=', '==', '!='])

def p_exp(p):
	'''exp : termino pending_termino_ops exp1'''

def p_pending_termino_ops(p):
	'''pending_termino_ops :'''
	crearCuadruploExpresion(validOperators = ['+', '-'])

def p_exp1(p):
	'''exp1 : PLUS push_operator_stack exp
		| MINUS push_operator_stack exp
		| empty'''

def p_termino(p):
	'''termino : factor pending_factor_ops termino1'''

def p_pending_factor_ops(p):
	'''pending_factor_ops :'''
	crearCuadruploExpresion(validOperators = ['*', '/'])

def p_termino1(p):
	'''termino1 : MULT push_operator_stack termino
		| DIVISION push_operator_stack termino
		| empty'''

def p_operators(p):
	'''operators : GREATER push_operator_stack
		| GREATER_EQUAL push_operator_stack
		| LESS push_operator_stack
		| LESS_EQUAL push_operator_stack
		| DIFFERENT push_operator_stack
		| EQUAL push_operator_stack
	'''

def p_factor(p):
	'''factor : L_PAREN expresion R_PAREN pop_operator_stack
		| var_cte
		| UMINUS push_operator_stack factor
		| NOT push_operator_stack factor
	'''
	# If unary operation
	if len(p) == 4:
		crearCuadruploUnario(validOperators = ['!', '~']) 

def p_push_operand_stack(p):
	'''push_operand_stack :'''
	globals.tipos.append(getIdDataType(id = p[-1], scope = globals.currentScope))
	globals.operandos.append(p[-1])

def p_push_constant_operand_stack(p):
	'push_constant_operand_stack :'
	if regex_boolean.match(str(p[-1])):
		globals.tipos.append(constants.DATA_TYPES[constants.BOOLEAN])
	elif regex_float.match(str(p[-1])):
		globals.tipos.append(constants.DATA_TYPES[constants.FLOAT])
	elif regex_int.match(str(p[-1])):
		globals.tipos.append(constants.DATA_TYPES[constants.INT])
	globals.operandos.append(p[-1])

def p_push_open_paren(p):
	'''push_open_paren :'''
	if p[-1] == '(' and p[-3] != 'while':
		globals.operadores.append(p[-1])

def p_push_operator_stack(p):
	'''push_operator_stack :'''
	globals.operadores.append(p[-1])

def p_pop_operator_stack(p):
	'''pop_operator_stack :'''
	globals.operadores.pop()

def p_coord(p):
	'''coord : L_PAREN xyz R_PAREN'''

def p_xyz(p):
	'''xyz : expresion COMMA expresion COMMA expresion'''

def p_func_call(p):
	'''func_call : func_id L_PAREN func_call1 R_PAREN'''

def p_func_call1(p):
	'''func_call1 : expresion func_call2
					| empty'''

def p_func_call2(p):
	'''func_call2 : COMMA expresion func_call2
					| empty'''

def p_func_id(p):
	'''func_id : DOWN
				| UP
				| FORWARD
				| TURN_LEFT
				| TURN_RIGHT
				| IS_FACING_NORTH
				| IS_FACING_SOUTH
				| IS_FACING_EAST
				| IS_FACING_WEST
				| GOAL
				| START
				| OUT_OF_BOUNDS
				| CAN_MOVE_FORWARD
				| IS_BLOCKED
				| IS_COLLECTIBLE
				| PICK_UP
				| POSITION
				| SPAWN_OBJECT
				| ENV_SIZE
				| SET_MOV_SPEED
				| LENGTH
				| ID
				'''

def p_declaracion(p):
	'''declaracion : tipo ID asignacion2 add_var'''

def p_inicializacion(p):
	'''inicializacion : tipo ID asignacion2 add_var ASSIGN push_operator_stack expresion'''
	globals.operandos.append(p[2])
	globals.tipos.append(p[1])
	crearCuadruploExpresion(['='])

def p_asignacion(p):
	'''asignacion : ID asignacion1 ASSIGN push_operator_stack expresion'''
	globals.operandos.append(p[1])
	globals.tipos.append(getIdDataType(p[1], globals.currentScope))
	crearCuadruploExpresion(['='])

def p_asignacion1(p):
	'''asignacion1 : L_BRACKET expresion R_BRACKET
					| empty'''

def p_asignacion2(p):
	'''asignacion2 : L_BRACKET CTE_I R_BRACKET
					| empty'''

def p_estatutos(p):
	'''estatutos : asignacion SEMICOLON
				  | condicion SEMICOLON
				  | for_loop SEMICOLON
				  | while_loop SEMICOLON
				  | func_call SEMICOLON'''

def p_error(p):
	if p is not None:
		print("Syntax error at '%s'" % p)
		sys.exit(1)

def p_empty(p):
	'''empty :'''
	pass