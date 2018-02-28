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
