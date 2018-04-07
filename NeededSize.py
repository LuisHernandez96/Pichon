class NeededSize:
	def __init__(self, localInts = 0, localFloats = 0, localBooleans = 0, tempInts = 0, tempFloats = 0, tempBooleans = 0):
		self.localInts = localInts
		self.localFloats = localFloats
		self.localBooleans = localBooleans
		self.tempInts = tempInts
		self.tempFloats = tempFloats
		self.tempBooleans = tempBooleans

	def __str__(self):
		return "localInts: {} localFloats: {} localBooleans: {}\n\ttempInts: {} tempFloats: {} tempBooleans: {}".format(
			self.localInts, self.localFloats, self.localBooleans, self.tempInts, self.tempFloats, self.tempBooleans)

	def addInts(self, Ints, temp):
		if temp:
			self.tempInts += Ints
		else:
			self.localInts += Ints

	def addFloats(self, Floats, temp):
		if temp:
			self.tempFloats += Floats
		else:
			self.localFloats += Floats

	def addBooleans(self, Booleans, temp):
		if temp:
			self.tempBooleans += Booleans
		else:
			self.localFloats += Booleans
