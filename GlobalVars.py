import SymbolTables as st

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
		self.currentSize = None
		self.currentScope = st.FUNC
		self.cuadruplos = []
		self.operadores = []
		self.saltos = []
		self.tipos = []
		self.operandos = []
		self.tmpCounter = 1
		self.cuadCounter = 0
		self.lineNumber = 0
		self.currentDataTypeString = ""

globals = GlobalVars()