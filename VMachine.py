GOTO = "GOTO"
PLUS = "+"
MINUS = "-"
EQUAL = "="


class VMachine:
    def __init__(self, cuadruplos = None):
        self.cuadruplos = cuadruplos
        self.currentCuad = 0
        self.INT_MEME = [None] * 10000
        self.FLOAT_MEME = [None] * 10000
        self.BOOL_MEME = [None] * 10000

    def runVM(self):
        while self.currentCuad < len(self.cuadruplos):
            self.processCuad(self.cuadruplos[self.currentCuad])


    def processCuad(self, cuadruplo):
        print("PC\tCuad= ",str(cuadruplo))

        if cuadruplo.operator == GOTO:
            self.currentCuad = cuadruplo.result
        elif cuadruplo.operator == PLUS:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            result = oper1 + oper2

            if self._saveResult(result,cuadruplo.result):
                self.currentCuad += 1
            else:
                sys.exit("Error in save result PLUS")

        elif cuadruplo.operator == MINUS:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            result = oper1 - oper2

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad += 1
            else:
                sys.exit("Error in save result MINUS")

        elif cuadruplo.operator == EQUAL:
            oper1 = self._getValue(cuadruplo.operand1)

            if self._saveResult(oper1, cuadruplo.result):
                self.currentCuad += 1
            else:
                sys.exit("Error in save result EQUAL")

    def _getValue(self,operand):
        try:
            if operand[0] == "%":
                operand = operand.replace("%","")
                return int(operand)

            elif operand[0] == "(":
                operand = operand.replace("(", "")
                operand = operand.replace(")", "")
        except:
            return self._retrieveFromMemory(int(operand))

    def _saveResult(self, value, memDirection):
        print("SR\tVal= ",value,"\tMemDir=",memDirection)
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

    def _retrieveFromMemory(self,memDirection):
        if memDirection < 50000:
            if self.INT_MEME[memDirection % 40000] == None:
                pass
            else:
                return self.INT_MEME[memDirection % 40000]
        elif memDirection > 59999:
            if self.BOOL_MEME[memDirection % 60000] == None:
                pass
            else:
                return self.INT_MEME[memDirection % 60000]
        else:
            if self.BOOL_MEME[memDirection % 50000] == None:
                pass
            else:
                return self.INT_MEME[memDirection % 50000]

