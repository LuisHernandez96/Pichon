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
import ply.lex as lex
lex.lex()

# Precedence rules for the arithmetic operators
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    )

def p_error(p):
    if p is not None:
        print("Syntax error at '%s'" % p)
    else:
        print("BENIS :DDDD")

def p_empty(p):
    'empty :'
    pass

import ply.yacc as yacc

parser = yacc.yacc(start='programa')

with open('test.txt') as f:
    read_data = f.read()

parser.parse(read_data)
