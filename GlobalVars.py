class GlobalVars:

    def __init__(self):
        self.currentVarsTable = None        # Variable table for the current scope
        self.currentDataType = -1           # Data type of the variable/constant being read 
        self.currentId = ''                 # ID of the variable being read
        self.currentSize = 1                # Size of the variable being read e.g array
        self.currentScope = "FUNCTIONS"     # Scope being read (FUNCTIONS, ENVIRONMENT, MOVEMENT, or any function defined by the user)
        self.cuadruplos = []                # Sequence of quadruples
        self.operadores = []                # Operator stack
        self.saltos = []                    # Jumps stack
        self.tipos = []                     # Data type stack
        self.operandos = []                 # Operand stack
        self.cuadCounter = 0                # Quadruples count
        self.lineNumber = 0                 # Line number being read
        self.currentDataTypeString = ""     # Data type of the variable/constant being read as a string
        self.parameterCounter = 0           # Parameter counter (used for checking parameters when calling a function)
        self.functionCalled = []            # Function call stack
        self.functionReturns = False        # Boolean flag that represents if a function returns a value or not
        self.lastDataType = -1              # Last data type in an array when initializing
        self.arrayPendingAddress = []       # Pending addresses when declaring/initializing arrays
        self.arrayPendingTypes = []         # Pending data types when declaring/initializing arrays
        self.isAssigning = False            # Boolean flag then represents if the current statement is assigning an expression to a variable
        self.assigningID = ""               # ID of the variable that is being assigned a value
        self.dimensiones = []               # Sequence of dictionaries describing the dimensions of an n-dimensional array
        self.dummyArray = []                # Python array that mimics the array being declared (used for checking dimension sizes)
        self.currentDim = 0                 # Dimension being read of an n-dimensional array
        self.saved_dims = []                # (array, dimension) stack
        self.R = 1                          # Used to describe the dimensions of an n-dimensional array
        self.suma = 0                       # Used to describe the dimensions of an n-dimensional array

globals = GlobalVars()
