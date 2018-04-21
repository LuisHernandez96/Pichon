GOTO = "GOTO"
GOTOF = "GOTO_FALSE"
GOTOT = "GOTO_TRUE"
VER = "VER"
PLUS = "+"
MINUS = "-"
MULT = "*"
DIV = "/"
ASSIGN = "="
OR = "||"
AND = "&&"
LESS_THAN = "<"
GREAT_THAN = ">"
EQL_LESS_THAN = "<="
EQL_GREAT_THAN = ">="
EQL = "=="
DIF = "!="
NOT = "!"
NEG = "~"
ERA = "ERA"
END_PROC = "ENDPROC"
PARAM = "PARAM"
GO_SUB = "GOSUB"

import Memory as Mem

class VMachine:
    def __init__(self, cuadruplos = None):
        self.cuadruplos = cuadruplos
        self.currentCuad = [0]
        self.memory = Mem.Memory()
        self.memoryStack = []

    def runVM(self):
        while self.currentCuad[-1] < len(self.cuadruplos):
            self.processCuad(self.cuadruplos[self.currentCuad[-1]])


    def processCuad(self, cuadruplo):
        print("PC\tCuad= ",str(cuadruplo))

        if cuadruplo.operator == GOTO:
            self.currentCuad[-1] = cuadruplo.result

        if cuadruplo.operator == GOTOF:
            oper1 = self._getValue(cuadruplo.operand1)

            if not oper1:
                self.currentCuad[-1] = cuadruplo.result
            else:
                self.currentCuad[-1] = self.currentCuad[-1]+1

        if cuadruplo.operator == GOTOT:
            oper1 = self._getValue(cuadruplo.operand1)

            if oper1:
                self.currentCuad[-1] = cuadruplo.result
            else:
                self.currentCuad[-1] = self.currentCuad[-1] + 1

        elif cuadruplo.operator == PLUS:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            result = oper1 + oper2

            if self._saveResult(result,cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result PLUS")

        elif cuadruplo.operator == MINUS:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            result = oper1 - oper2

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result MINUS")

        elif cuadruplo.operator == MULT:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            result = oper1 * oper2

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result MULT")

        elif cuadruplo.operator == DIV:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            result = oper1 / oper2

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result DIV")

        elif cuadruplo.operator == ASSIGN:
            oper1 = self._getValue(cuadruplo.operand1)

            if self._saveResult(oper1, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result EQUAL")

        elif cuadruplo.operator == OR:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            if oper1 or oper2:
                result = True
            else:
                result = False

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result OR")

        elif cuadruplo.operator == AND:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            if oper1 and oper2:
                result = True
            else:
                result = False

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result AND")

        elif cuadruplo.operator == LESS_THAN:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            if oper1 < oper2:
                result = True
            else:
                result = False

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result LESS_THAN")

        elif cuadruplo.operator == GREAT_THAN:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            if oper1 > oper2:
                result = True
            else:
                result = False

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result GREAT_THAN")

        elif cuadruplo.operator == EQL_LESS_THAN:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            if oper1 <= oper2:
                result = True
            else:
                result = False

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result EQL_LESS_THAN")

        elif cuadruplo.operator == EQL_GREAT_THAN:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            if oper1 >= oper2:
                result = True
            else:
                result = False

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result EQL_GREAT_THAN")

        elif cuadruplo.operator == EQL:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            if oper1 == oper2:
                result = True
            else:
                result = False

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result EQL")

        elif cuadruplo.operator == DIF:
            oper1 = self._getValue(cuadruplo.operand1)
            oper2 = self._getValue(cuadruplo.operand2)

            if oper1 != oper2:
                result = True
            else:
                result = False

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result DIF")

        elif cuadruplo.operator == NOT:
            oper1 = self._getValue(cuadruplo.operand1)

            if not oper1:
                result = True
            else:
                result = False

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result NOT")

        elif cuadruplo.operator == NEG:
            oper1 = self._getValue(cuadruplo.operand1)

            result = oper1 * -1

            if self._saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result NEG")

        elif cuadruplo.operator == ERA:
            self.memoryStack.append(Mem.Memory())

        elif cuadruplo.operator == PARAM:
            oper1 = self._getValue(cuadruplo.operand1)

            self.memoryStack[-1].PARAMS.append(oper1)

        elif cuadruplo.operator == GO_SUB:
            self.currentCuad.append(cuadruplo.result)



        elif cuadruplo.operator == END_PROC:
            pass

        print("")

    def _getValue(self,operand):
        try:
            if operand[0] == "%":
                operand = operand.replace("%","")
                try:
                    return int(operand)
                except:
                    if operand == "true":
                        return True
                    elif operand == "false":
                        return False
                    else:
                        return "KEK_ERROR"

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
                    self.memory.INT_MEME[memDirection % 40000] = value
                elif memDirection > 59999:
                    self.memory.BOOL_MEME[memDirection % 60000] = value
                else:
                    self.memory.FLOAT_MEME[memDirection % 50000] = value

                return True
            except:
                return False

    def _retrieveFromMemory(self,memDirection):
        if memDirection < 50000:
            if self.memory.INT_MEME[memDirection % 40000] == None:
                pass
            else:
                return self.memory.INT_MEME[memDirection % 40000]
        elif memDirection > 59999:
            if self.memory.BOOL_MEME[memDirection % 60000] == None:
                pass
            else:
                return self.memory.BOOL_MEME[memDirection % 60000]
        else:
            if self.memory.FLOAT_MEME[memDirection % 50000] == None:
                pass
            else:
                return self.memory.FLOAT_MEME[memDirection % 50000]

