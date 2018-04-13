import constants

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
		self.LOCAL_TEMP_INT_START = 40000
		self.LOCAL_TEMP_FLOAT_START = 50000
		self.LOCAL_TEMP_BOOLEAN_START = 60000

		self.CURRENT_TEMP_INT = 40000
		self.CURRENT_TEMP_FLOAT = 50000
		self.CURRENT_TEMP_BOOLEAN = 60000

	def ADD_NEW_VAR(self, data_type):
		if data_type == constants.DATA_TYPES[constants.INT]:
			assignedMemory = self.CURRENT_TEMP_INT
			self.CURRENT_TEMP_INT += 1
			self.LOCAL_MEMORY["INT_MEM"][self.CURRENT_TEMP_INT] = None
		elif data_type == constants.DATA_TYPES[constants.FLOAT]:
			assignedMemory = self.CURRENT_TEMP_FLOAT
			self.CURRENT_TEMP_FLOAT += 1
			self.LOCAL_MEMORY["FLOAT_MEM"][self.CURRENT_TEMP_FLOAT] = None
		elif data_type == constants.DATA_TYPES[constants.BOOLEAN]:
			assignedMemory = self.CURRENT_TEMP_BOOLEAN
			self.CURRENT_TEMP_BOOLEAN += 1
			self.LOCAL_MEMORY["BOOLEAN_MEM"][self.CURRENT_TEMP_BOOLEAN] = None
		return assignedMemory

	def PREVIOUS_ADDRESS(self, data_type):
		if data_type == constants.DATA_TYPES[constants.INT]:
			return self.CURRENT_TEMP_INT - 1
		elif data_type == constants.DATA_TYPES[constants.FLOAT]:
			return self.CURRENT_TEMP_FLOAT - 1
		elif data_type == constants.DATA_TYPES[constants.BOOLEAN]:
			return self.CURRENT_TEMP_BOOLEAN - 1

	def CLEAR_MEMORY(self):
		self.CURRENT_TEMP_INT = self.LOCAL_TEMP_INT_START
		self.CURRENT_TEMP_FLOAT = self.LOCAL_TEMP_FLOAT_START
		self.CURRENT_TEMP_BOOLEAN = self.LOCAL_TEMP_BOOLEAN_START

		for key in self.LOCAL_MEMORY:
				self.LOCAL_MEMORY[key].clear()

memory = Memory()