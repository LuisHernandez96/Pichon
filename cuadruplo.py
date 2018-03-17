class Cuadruplo:
	def __init__(self, operator = None, operand1 = None, operand2 = None, result = None):
		self.operator = operator
		self.operand1 = operand1
		self.operand2 = operand2
		self.result = result

	def __str__(self):
		return "<{}, {}, {}, {}>".format(self.operator, self.operand1, self.operand2, self.result)