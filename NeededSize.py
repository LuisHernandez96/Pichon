class NeededSize:
	def __init__(self, amountInts = 0, amountFloats = 0, amountBooleans = 0):
		self.amountInts = amountInts
		self.amountFloats = amountFloats
		self.amountBooleans = amountBooleans

	def __str__(self):
		return "ints: {} floats: {} booleans: {}".format(self.amountInts, self.amountFloats, self.amountBooleans)

	def addInts(self, amountInts):
		self.amountInts += amountInts

	def addFloats(self, amountFloats):
		self.amountFloats += amountFloats

	def addBooleans(self, amountBooleans):
		self.amountBooleans += amountBooleans