class GlobalVars:

	def nextTmp(self):
		nextTemporal = "tmp" + str(self.tmpCounter)
		self.tmpCounter = self.tmpCounter + 1
		return nextTemporal

	def prevTmp(self):
		prevTemporal = "tmp" + str(self.tmpCounter - 1)
		return prevTemporal

	def __init__(self):
		self.currentVarsTable = None
		self.currentDataType = -1
		self.currentId = ''
		self.currentSize = 1
		self.currentScope = "FUNCTIONS"
		self.cuadruplos = []
		self.operadores = []
		self.saltos = []
		self.tipos = []
		self.operandos = []
		self.tmpCounter = 1
		self.cuadCounter = 0
		self.lineNumber = 0
		self.currentDataTypeString = ""
		self.parameterCounter = 0
		self.functionCalled = ""
		self.size_dims = []
		self.isArr = False

	def setArrDataType(self):
		if self.currentDataType == 0:
			self.currentDataType = 4
		elif self.currentDataType == 1:
			self.currentDataType = 5
		elif self.currentDataType == 2:
			self.currentDataType = 7
		elif self.currentDataType == 3:
			self.currentDataType = 6

globals = GlobalVars()