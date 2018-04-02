import ply.lex as lex
import ply.yacc as yacc
from GlobalVars import globals
from lexer import *
from parser import *

def main():
	st.SYMBOL_INIT(False)

	# Build the lexer
	lex.lex()
	parser = yacc.yacc(start='start')

	with open('test.txt') as f:
		read_data = f.read()

	parser.parse(read_data)
	for i in range(0, len(globals.cuadruplos)):
		print(globals.cuadruplos[i])

	assert len(globals.operadores) == 0
	assert len(globals.saltos) == 0

if __name__ == '__main__':
	main()