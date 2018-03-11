import ply.lex as lex
import ply.yacc as yacc
import sys
from SymbolTables import *

# TEM

SYMBOL_INIT(False)

reserved = {
    'FUNCTIONS' : 'FUNCTIONS',
    'ENVIRONMENT' : 'ENVIRONMENT',
    'MOVEMENT' : 'MOVEMENT',
    'function' : 'FUNCTION',
    'int' : 'INT',
    'float' : 'FLOAT',
    'boolean' : 'BOOLEAN',
    'coord' : 'COORD',
    'void' : 'VOID',
    'return' : 'RETURN',
    'if' : 'IF',
    'elif' : 'ELIF',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'for' : 'FOR',
    'true' : 'TRUE',
    'false' : 'FALSE',
    'cube' : 'CUBE',
    'sphere' : 'SPHERE',
    'down' : 'DOWN',
    'up' : 'UP',
    'forward' : 'FORWARD',
    'turnLeft' : 'TURN_LEFT',
    'turnRight' : 'TURN_RIGHT',
    'isFacingNorth' : 'IS_FACING_NORTH',
    'isFacingSouth' : 'IS_FACING_SOUTH',
    'isFacingEast' : 'IS_FACING_EAST',
    'isFacingWest' : 'IS_FACING_WEST',
    'goal' : 'GOAL',
    'start' : 'START',
    'outOfBounds' : 'OUT_OF_BOUNDS',
    'canMoveForward' : 'CAN_MOVE_FORWARD',
    'isBlocked' : 'IS_BLOCKED',
    'isCollectible' : 'IS_COLLECTIBLE',
    'pickUp' : 'PICK_UP',
    'position' : 'POSITION',
    'spawnObject' : 'SPAWN_OBJECT',
    'envSize' : 'ENV_SIZE',
    'setMovementSpeed' : 'SET_MOV_SPEED',
    'length' : 'LENGTH'
}

tokens = [
    'CTE_I',
    'CTE_F',
    'ID',
    'COMMA',
    'L_PAREN',
    'R_PAREN',
    'L_BRACE',
    'R_BRACE',
    'L_BRACKET',
    'R_BRACKET',
    'ASSIGN',
    'SEMICOLON',
    'PLUS',
    'MINUS',
    'MULT',
    'DIVISION',
    'NOT',
    'LESS',
    'LESS_EQUAL',
    'GREATER',
    'GREATER_EQUAL',
    'DIFFERENT',
    'EQUAL',
    'AND',
    'OR'
] + list(reserved.values())

# Tokens
def t_CTE_F(t):
    r'[0-9]*[\.][0-9]+'
    t.value = float(t.value)
    return t

def t_CTE_I(t):
    r'[0-9][0-9]*'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')
    pprint.pprint(t)
    return t

t_COMMA         = r'\,'
t_L_PAREN       = r'\('
t_R_PAREN       = r'\)'
t_L_BRACE       = r'\{'
t_R_BRACE       = r'\}'
t_L_BRACKET     = r'\['
t_R_BRACKET     = r'\]'
t_DIFFERENT     = r'\!\='
t_EQUAL         = r'\=\='
t_ASSIGN        = r'\='
t_SEMICOLON     = r'\;'
t_PLUS          = r'\+'
t_MINUS         = r'\-'
t_MULT          = r'\*'
t_DIVISION      = r'\/'
t_NOT           = r'\!'
t_GREATER_EQUAL = r'\>\='
t_LESS_EQUAL    = r'\<\='
t_LESS          = r'\<'
t_GREATER       = r'\>'
t_AND           = r'\&\&'
t_OR            = r'\|\|'

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    print("Line: " + str(t.lexer.lineno))
    t.lexer.skip(1)


# Build the lexer
lex.lex()

# Precedence rules for the arithmetic operators
precedence = (
    ('left','PLUS','MINUS'),
    ('left','MULT','DIVISION'),
    ('right', 'NOT')
)

def p_start(p):
    'start : func_sec env_sec mov_sec'
    print("Finished!")

def p_func_sec(p):
    'func_sec : FUNCTIONS L_BRACE func_sec1 R_BRACE'

def p_func_sec1(p):
    '''func_sec1 : functions func_sec1
        | empty'''

def p_functions(p):
    'functions : FUNCTION tipo ID L_PAREN functions1 R_PAREN L_BRACE vars bloque functions2 R_BRACE'
    ADD_FUNC(p[3],p[2], globals.currentVarsTable, False)

def p_functions1(p):
    '''functions1 : params
                   | empty '''
def p_fucntions2(p):
    '''functions2 : return
                   | empty'''

def p_env_sec(p):
    'env_sec : ENVIRONMENT L_BRACE vars bloque R_BRACE'

def p_mov_sec(p):
    'mov_sec : MOVEMENT L_BRACE vars bloque R_BRACE'

def p_tipo(p):
    '''tipo : INT tipo1
            | BOOLEAN tipo1
            | COORD tipo1
            | FLOAT tipo1
            | VOID'''

def p_tipo1(p):
    '''tipo1 : L_BRACKET tipo2 R_BRACKET
              | empty'''

def p_tipo2(p):
    '''tipo2 : CTE_I
              | empty'''

def p_params(p):
    'params : tipo ID params1'

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
    'list : L_BRACE expresion list1 R_BRACE'

def p_list1(p):
    '''list1 : COMMA expresion list1
              | empty'''

def p_return(p):
    'return : RETURN expresion SEMICOLON'

def p_condicion(p):
    'condicion : IF L_PAREN expresion R_PAREN L_BRACE bloque R_BRACE condicion1'

def p_condicion1(p):
    '''condicion1 : ELSE L_BRACE bloque R_BRACE
        | ELIF L_PAREN expresion R_PAREN L_BRACE bloque R_BRACE condicion1
        | empty'''

def p_while_loop(p):
    'while_loop : WHILE L_PAREN expresion R_PAREN L_BRACE bloque R_BRACE'

def p_for_loop(p):
    'for_loop : FOR L_PAREN asignacion SEMICOLON expresion SEMICOLON expresion R_PAREN L_BRACE bloque R_BRACE'

def p_var_cte(p):
    '''var_cte : ID var_cte1
        | func_call var_cte1
        | coord var_cte1
        | list var_cte1
        | CTE_I
        | CTE_F
        | TRUE
        | FALSE
        | CUBE
        | SPHERE
    '''

def p_var_cte1(p):
    '''var_cte1 : L_BRACKET expresion R_BRACKET
        | empty
    '''

def p_expresion(p):
    'expresion : exp expresion2'

def p_expresion2(p):
    '''expresion2 : operators exp
        | empty
    '''

def p_exp(p):
    'exp : termino exp1'

def p_exp1(p):
    '''exp1 : PLUS exp
        | MINUS exp
        | OR exp
        | empty'''

def p_termino(p):
    'termino : factor termino1'

def p_termino1(p):
    '''termino1 : MULT termino
        | DIVISION termino
        | AND termino
        | empty'''

def p_operators(p):
    '''operators : GREATER
        | GREATER_EQUAL
        | LESS
        | LESS_EQUAL
        | DIFFERENT
        | EQUAL
    '''

def p_factor(p):
    '''factor : L_PAREN expresion R_PAREN
        | var_cte
        | MINUS factor
        | NOT factor
    '''

def p_coord(p):
    'coord : L_PAREN xyz R_PAREN'

def p_xyz(p):
    'xyz : expresion COMMA expresion COMMA expresion'

def p_func_call(p):
    'func_call : func_id L_PAREN func_call1 R_PAREN'

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
    'declaracion : tipo ID asignacion2'

def p_inicializacion(p):
    'inicializacion : tipo ID asignacion2 ASSIGN expresion'

def p_asignacion(p):
    'asignacion : ID asignacion1 ASSIGN expresion'

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
    'empty :'
    pass

# Build the lexer
lex.lex()
parser = yacc.yacc(start='start')

with open('test.txt') as f:
    read_data = f.read()

parser.parse(read_data)
