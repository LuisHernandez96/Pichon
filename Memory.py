import constants
import SymbolTables as st
import pprint

class Memory:

	LOCAL_MEMORY = {
		"INT_MEM" : {

		},
		"FLOAT_MEM" : {

		},
		"BOOLEAN_MEM" : {

		}
	}

	def __init__(self):

		self.INT_MEME = [None] * 10000
		self.FLOAT_MEME = [None] * 10000
		self.BOOL_MEME = [None] * 10000

		self.SEND_PARAMS = []
		self.RECEIVE_PARAMS = []

		self.LOCAL_TEMP_INT_START = 40000
		self.LOCAL_TEMP_FLOAT_START = 50000
		self.LOCAL_TEMP_BOOLEAN_START = 60000

		self.CURRENT_TEMP_INT = 40000
		self.CURRENT_TEMP_FLOAT = 50000
		self.CURRENT_TEMP_BOOLEAN = 60000

		self.currentFunc = None

	def ADD_NEW_VAR(self, data_type, size = 1):
		if data_type == constants.DATA_TYPES[constants.INT] or data_type == constants.DATA_TYPES[constants.INT_LIST]:
			assignedMemory = self.CURRENT_TEMP_INT
			self.CURRENT_TEMP_INT += size
			self.LOCAL_MEMORY["INT_MEM"][assignedMemory] = None
		elif data_type == constants.DATA_TYPES[constants.FLOAT] or data_type == constants.DATA_TYPES[constants.FLOAT_LIST]:
			assignedMemory = self.CURRENT_TEMP_FLOAT
			self.CURRENT_TEMP_FLOAT += size
			self.LOCAL_MEMORY["FLOAT_MEM"][assignedMemory] = None
		elif data_type == constants.DATA_TYPES[constants.BOOLEAN] or data_type == constants.DATA_TYPES[constants.BOOLEAN_LIST]:
			assignedMemory = self.CURRENT_TEMP_BOOLEAN
			self.CURRENT_TEMP_BOOLEAN += size
			self.LOCAL_MEMORY["BOOLEAN_MEM"][assignedMemory] = None
		elif data_type == constants.DATA_TYPES[constants.VOID]:
			assignedMemory = -1

		return assignedMemory

	def PREVIOUS_ADDRESS(self, data_type):
		if data_type == constants.DATA_TYPES[constants.INT]:
			return self.CURRENT_TEMP_INT - 1
		elif data_type == constants.DATA_TYPES[constants.FLOAT]:
			return self.CURRENT_TEMP_FLOAT - 1
		elif data_type == constants.DATA_TYPES[constants.BOOLEAN]:
			return self.CURRENT_TEMP_BOOLEAN - 1

	def CURRENT_ADDRESS(self, data_type):
		if data_type == constants.DATA_TYPES[constants.INT]:
			return self.CURRENT_TEMP_INT
		elif data_type == constants.DATA_TYPES[constants.FLOAT]:
			return self.CURRENT_TEMP_FLOAT
		elif data_type == constants.DATA_TYPES[constants.BOOLEAN]:
			return self.CURRENT_TEMP_BOOLEAN

	def CLEAR_MEMORY(self):
		self.CURRENT_TEMP_INT = self.LOCAL_TEMP_INT_START
		self.CURRENT_TEMP_FLOAT = self.LOCAL_TEMP_FLOAT_START
		self.CURRENT_TEMP_BOOLEAN = self.LOCAL_TEMP_BOOLEAN_START

		for key in self.LOCAL_MEMORY:
				self.LOCAL_MEMORY[key].clear()

	def PROCESS_PARAMS(self, subName):
		# pprint.pprint(self.PARAMS)
		# pprint.pprint(st.GET_PARAMS(subName))
		# pprint.pprint(st.GET_PARAMS_ADDRESS(subName))
		self.currentFunc = subName
		for param, pType, pAddress in zip(self.RECEIVE_PARAMS,st.GET_PARAMS(subName), st.GET_PARAMS_ADDRESS(subName)):
			# print(param,pType,pAddress)
			if isinstance(param, list):
				for i in range(0, len(param)):
					self.saveResult(param[i], pAddress + i)
			else:
				self.saveResult(param, pAddress)

	def getValue(self, operand):
		try:
			if operand[0] == "%":
				operand = operand.replace("%", "")
				
				if constants.regex_float.match(operand):
					return float(operand)
				elif constants.regex_int.match(operand):
					return int(operand)
				elif constants.regex_boolean.match(operand):
					if operand == "true":
						return True
					elif operand == "false":
						return False

			elif operand[0] == "(":
				operand = operand.replace("(", "")
				operand = operand.replace(")", "")
				targetDir = self.getValue(operand)
				return self.getValue(targetDir)
			else:
				return self.retrieveFromMemory(int(operand))
		except:
			return self.retrieveFromMemory(int(operand))

	def getAddress(self, address):
		try:
			if address[0] == '(':
				address = address.replace("(", "")
				address = address.replace(")", "")
				address = str(self.retrieveFromMemory(int(address)))
				return self.getAddress(address)
			else:
				return address
		except:
			return address

	def getCurrentFuncReturnSize(self):
		return st.SYMBOL_TABLE[st.FUNC][self.currentFunc][st.RETURN_SIZE]

	def saveResult(self, value, memDirection):
		if memDirection < 40000:
			return False
		else:
			try:
				if memDirection < 50000:
					self.INT_MEME[memDirection % 40000] = value
				elif memDirection > 59999:
					self.BOOL_MEME[memDirection % 60000] = value
				else:
					self.FLOAT_MEME[memDirection % 50000] = value

				return True
			except:
				return False

	def retrieveFromMemory(self, memDirection):
		if memDirection < 50000:
			if self.INT_MEME[memDirection % 40000] == None:
				pass
			else:
				return self.INT_MEME[memDirection % 40000]
		elif memDirection > 59999:
			if self.BOOL_MEME[memDirection % 60000] == None:
				pass
			else:
				return self.BOOL_MEME[memDirection % 60000]
		else:
			if self.FLOAT_MEME[memDirection % 50000] == None:
				pass
			else:
				return self.FLOAT_MEME[memDirection % 50000]

	def setReturn(self,value):
		st.ADD_RETURN_VALUES(self.currentFunc, value)
		self.SEND_PARAMS.insert(0, value)

memory = Memory()