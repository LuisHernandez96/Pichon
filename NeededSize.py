# Store the amount of variables a scope needs to execute
# NOTE: WE ENDED UP NOT USING THIS AND JUST GIVE 10000 ADDRESSES TO EACH DATA TYPE
class NeededSize:

	# Constructor
	def __init__(self, localInts = 0, localFloats = 0, localBooleans = 0, tempInts = 0, tempFloats = 0, tempBooleans = 0):
		self.localInts = localInts
		self.localFloats = localFloats
		self.localBooleans = localBooleans
		self.tempInts = tempInts
		self.tempFloats = tempFloats
		self.tempBooleans = tempBooleans

	# __str__ override to print in an easy to read format
	def __str__(self):
		return "localInts: {} localFloats: {} localBooleans: {} tempInts: {} tempFloats: {} tempBooleans: {}".format(
			self.localInts, self.localFloats, self.localBooleans, self.tempInts, self.tempFloats, self.tempBooleans)

	# Add local or temporal integers
	def addInts(self, Ints, temp):
		if temp:
			self.tempInts += Ints
		else:
			self.localInts += Ints

	# Add local or temporal floats
	def addFloats(self, Floats, temp):
		if temp:
			self.tempFloats += Floats
		else:
			self.localFloats += Floats

	# Add local or temporal booleans
	def addBooleans(self, Booleans, temp):
		if temp:
			self.tempBooleans += Booleans
		else:
			self.localBooleans += Booleans
