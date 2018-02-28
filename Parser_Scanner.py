reserved = {
    'if' : 'IF',
    'else': 'ELSE',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'print': 'PRINT',
    'program' : 'PROGRAM'
}

tokens = [
    'ID','CTE_I','CTE_F','CTE_STRING',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN', 'COLON',
    'SEMICOLON', 'COMA', 'LBRAC', 'RBRAC',
    'BIGGER', 'LESS', 'DIF'
    ] + list(reserved.values())

# Tokens
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_EQUALS    = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COLON     = r'\:'
t_SEMICOLON = r'\;'
t_COMA      = r'\,'
t_LBRAC     = r'\{'
t_RBRAC     = r'\}'
t_DIF      = r'\<\>'
t_BIGGER    = r'\>'
t_LESS      = r'\<'
t_CTE_STRING =  r'[\"].*[\"]'

def t_ID(t):
    r'[_a-zA-Z][_a-zA-Z0-9]*'
    print(t.value)
    t.type = reserved.get(t.value,'ID')
    print("--" + t.type + "--")
    return t

def t_CTE_F(t):
    r'[0-9]*[\.][0-9]+'
    t.value = float(t.value)
    print(t.value)
    print("--cte_f--")
    return t

def t_CTE_I(t):
     r'[1-9][0-9]*'
     t.value = int(t.value)
     print(t.value)
     print("--cte_s--")
     return t

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
