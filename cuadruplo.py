# Representation for intermediate code
class Cuadruplo:
	
	# Constructor
	def __init__(self, operator = None, operand1 = None, operand2 = None, result = None, counter = None):
		self.operator = operator	# Operation code
		self.operand1 = operand1	# First operand
		self.operand2 = operand2	# Second operand
		self.result = result		# Result
		self.counter = counter		# Counter (used for debugging purposes)

	# __str__ overriding to print a quadruple using an easy to read format.
	def __str__(self):
		return "{}.\t<{},\t{},\t{},\t{}>".format(self.counter, self.operator, self.operand1, self.operand2, self.result)