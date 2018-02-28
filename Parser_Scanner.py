import ply.lex as lex
import ply.yacc as yacc

reserved = {
    'functions' : 'FUNCTIONS',
    'environment' : 'ENVIRONMENT',
    'movement' : 'MOVEMENT',
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
def t_CTE_I(t):
    r'[1-9][0-9]*'
    t.value = int(t.value)
    return t

def t_CTE_F(t):
    r'[0-9]*[\.][0-9]+'
    t.value = float(t.value)
    return t

def t_ID(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t

t_COMMA         = r'\,'
t_L_PAREN       = r'\('
t_R_PAREN       = r'\)'
t_L_BRACE       = r'\{'
t_R_BRACE       = r'\}'
t_L_BRACKET     = r'\['
t_R_BRACKET     = r'\]'
t_ASSIGN        = r'\='
t_SEMICOLON     = r'\;'
t_PLUS          = r'\+'
t_MINUS         = r'\-'
t_MULT          = r'\*'
t_DIVISION      = r'\/'
t_NOT           = r'\!'
t_LESS          = r'\<'
t_LESS_EQUAL    = r'\<\='
t_GREATER       = r'\>'
t_GREATER_EQUAL = r'\>\='
t_DIFFERENT     = r'\!\='
t_EQUAL         = r'\=\='
t_AND           = r'\&\&'
t_OR            = r'\|\|'

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lex.lex()

# Precedence rules for the arithmetic operators
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    )

def p_start(p):
    'start: func_sec env_sec mov_sec'

def p_func_sec(p):
    'func_sec: FUNCTIONS { func_sec1 }'
def p_func_sec1(p):
    '''func_sec1: functions func_sec1
        | empty'''

def p_functions(p):
    'functions: FUNCTION tipo ID ( functions1 ) { vars bloque functions2 }'
def p_functions1(p):
    '''functions1: params
                   | empty '''
def p_fucntions2(p):
    '''functions2: return
                   | empty'''

def p_env_sec(p):
    'env_sec: ENVIRONMENT { vars bloque }'

def p_mov_sec(p):
    'mov_sec: MOVEMENT { vars bloque }'

def p_tipo(p):
    '''tipo: INT tipo1
            | BOOLEAN tipo1
            | COORD tipo1
            | FLOAT tipo1
            | VOID tipo1'''
def p_tipo1(p):
    '''tipo1: [ tipo2 ]
              | empty'''
def p_tipo2(p):
    '''tipo2: CTE_I
              | empty'''

def p_params(p):
    'params: tipo ID params1'
def p_params1(p):
    '''params1: , params
                | empty'''

def p_bloque(p):
    '''bloque: bloque1
               | empty'''
def p_bloque1(p):
    '''bloque1: estatutos bloque1
                | empty'''

def p_vars(p):
    '''vars: declaracion ; vars
        | inicializacion ; vars
        | empty'''

def p_list(p):
    'list: { expresion list1 }'
def p_list1(p):
    '''list1: , expresion list1
              | empty'''

def p_return(p):
    'return: RETURN expresion ;'

def p_func_call(p):
    'func_call: func_id ( func_call1 )'
def p_func_call1(p):
    '''func_call1: expresion func_call2
                    | empty'''
def p_func_call2(p):
    '''func_call2: , expresion func_call2
                    | empty'''

def p_func_id(p):
    '''func_id: ID
                | DOWN
                | UP
                | FORWARD
                | TURN_LEFT
                | TURN_RIGTH
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
                | SET_MOVEMENT_SPEED
                | LENGTH
                '''

def p_declaracion(p):
    'declaracion: tipo ID'

def p_inicializacion(p):
    'inicializacion: tipo ID = expresion'

def p_asignacion(p):
    'asignacion: ID asignacion1 = expresion'
def p_asignacion1(p):
    '''asignacion1: [ expresion ]
                    | empty'''

def p_estatutos(p):
    '''estatutos: asignacion ;
                  | condicion ;
                  | for_loop ;
                  | while_loop ;
                  | func_call ;'''

def p_error(p):
    if p is not None:
        print("Syntax error at '%s'" % p)
    else:
        print("BENIS :DDDD")

def p_empty(p):
    'empty :'
    pass

parser = yacc.yacc(start='programa')

with open('test.txt') as f:
    read_data = f.read()

parser.parse(read_data)
