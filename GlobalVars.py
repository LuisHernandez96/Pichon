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
        self.functionReturns = False
        self.lastDataType = -1
        self.arrayPendingAddress = []
        self.arrayPendingTypes = []

        # De aquí para abajo puede que haya cosas que no se están usando
        self.isAssigning = False
        self.assigningID = ""
        self.dimensiones = []
        self.dummyArray = []
        self.currentDim = 0
        self.assigningArrayDimensions = []
        self.saved_dims = []
        self.saved_arrs_ids = []
        self.R = 1
        self.suma = 0
        self.dims_for_address = []
        self.arrBase = 0


globals = GlobalVars()
