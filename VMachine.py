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
PARAM = "PARAMETER"
GO_SUB = "GOSUB"
RETURN = "RETURN"

import Memory as Mem

class VMachine:
    def __init__(self, cuadruplos = None):
        self.cuadruplos = cuadruplos
        self.currentCuad = [0]
        self.memory = Mem.Memory()
        self.memoryStack = [self.memory]
        self.subMem = []

    def runVM(self):

        while self.currentCuad[-1] < len(self.cuadruplos):
            self.processCuad(self.cuadruplos[self.currentCuad[-1]])


    def processCuad(self, cuadruplo):
        print("PC\tCuad= ",str(cuadruplo))

        if cuadruplo.operator == GOTO:
            self.currentCuad[-1] = cuadruplo.result

        if cuadruplo.operator == GOTOF:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)

            if not oper1:
                self.currentCuad[-1] = cuadruplo.result
            else:
                self.currentCuad[-1] = self.currentCuad[-1]+1

        if cuadruplo.operator == GOTOT:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)

            if oper1:
                self.currentCuad[-1] = cuadruplo.result
            else:
                self.currentCuad[-1] = self.currentCuad[-1] + 1

        elif cuadruplo.operator == PLUS:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            result = oper1 + oper2

            if self.memoryStack[-1].saveResult(result,cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result PLUS")

        elif cuadruplo.operator == MINUS:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            result = oper1 - oper2

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result MINUS")

        elif cuadruplo.operator == MULT:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            result = oper1 * oper2

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result MULT")

        elif cuadruplo.operator == DIV:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            result = oper1 / oper2

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result DIV")

        elif cuadruplo.operator == ASSIGN:
            if len(self.subMem)!=0 and self.subMem[-1] == cuadruplo.operand1:
                if self.memoryStack[-1].saveResult(self.memoryStack[-1].RECEIVE_PARAMS[-1], cuadruplo.result):
                    self.memoryStack[-1].RECEIVE_PARAMS.pop()
                    self.currentCuad[-1] += 1
                else:
                    print("case1.1.2")
            else:
                oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)

                if self.memoryStack[-1].saveResult(oper1, cuadruplo.result):
                    self.currentCuad[-1] += 1
                else:
                    sys.exit("Error in save result EQUAL")

        elif cuadruplo.operator == OR:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            if oper1 or oper2:
                result = True
            else:
                result = False

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result OR")

        elif cuadruplo.operator == AND:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            if oper1 and oper2:
                result = True
            else:
                result = False

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result AND")

        elif cuadruplo.operator == LESS_THAN:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            if oper1 < oper2:
                result = True
            else:
                result = False

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result LESS_THAN")

        elif cuadruplo.operator == GREAT_THAN:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            if oper1 > oper2:
                result = True
            else:
                result = False

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result GREAT_THAN")

        elif cuadruplo.operator == EQL_LESS_THAN:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            if oper1 <= oper2:
                result = True
            else:
                result = False

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result EQL_LESS_THAN")

        elif cuadruplo.operator == EQL_GREAT_THAN:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            if oper1 >= oper2:
                result = True
            else:
                result = False

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result EQL_GREAT_THAN")

        elif cuadruplo.operator == EQL:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            if oper1 == oper2:
                result = True
            else:
                result = False

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result EQL")

        elif cuadruplo.operator == DIF:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            if oper1 != oper2:
                result = True
            else:
                result = False

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result DIF")

        elif cuadruplo.operator == NOT:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)

            if not oper1:
                result = True
            else:
                result = False

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result NOT")

        elif cuadruplo.operator == NEG:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)

            result = oper1 * -1

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                sys.exit("Error in save result NEG")

        elif cuadruplo.operator == ERA:
            # self.memoryStack.append(Mem.Memory())
            self.currentCuad[-1] += 1

        elif cuadruplo.operator == PARAM:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            self.memoryStack[-1].SEND_PARAMS.append(oper1)
            self.currentCuad[-1] += 1

        elif cuadruplo.operator == GO_SUB:
            self.currentCuad.append(cuadruplo.result)
            self.memoryStack.append(Mem.Memory())
            self.subMem.append(cuadruplo.operand1)
            self.memoryStack[-1].RECEIVE_PARAMS = self.memoryStack[-2].SEND_PARAMS
            self.memoryStack[-2].SEND_PARAMS = []
            self.memoryStack[-1].PROCESS_PARAMS(str(cuadruplo.operand1))

        elif cuadruplo.operator == RETURN:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.result)
            self.memoryStack[-1].setReturn(oper1)
            self.currentCuad[-1] += 1

        elif cuadruplo.operator == END_PROC:
            self.memoryStack[-2].RECEIVE_PARAMS = self.memoryStack[-1].SEND_PARAMS
            self.memoryStack.pop()
            self.currentCuad.pop()
            self.currentCuad[-1] += 1

        print("")



