import Memory as Mem
import SymbolTables as st
import GameManager
from utils import raiseError
from vpython import *
import time

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

class VMachine:
    def __init__(self, cuadruplos = None):
        self.cuadruplos = cuadruplos
        self.currentCuad = [0]
        self.memory = Mem.Memory()
        self.memoryStack = [self.memory]
        self.subMem = []
        self.gm = None

    def runVM(self):
        self.gm = GameManager.GameManager()
        while self.currentCuad[-1] < len(self.cuadruplos):
            self.processCuad(self.cuadruplos[self.currentCuad[-1]])
        print("Finished!")

    def processReservedFunction(self, function, parameters):
            if function == "down":
                self.gm.player.pos = self.gm.player.pos - self.gm.player.up
                time.sleep(1)
            elif function == "up":
                self.gm.player.pos = self.gm.player.pos + self.gm.player.up
                time.sleep(1)
            elif function == "forward":
                self.gm.player.pos = self.gm.player.pos + self.gm.player.axis
                time.sleep(1)
            elif function == "turnLeft":
                self.gm.player.rotate(radians(90), vec(0, 1, 0))
                time.sleep(1)
            elif function == "turnRight":
                self.gm.player.rotate(radians(-90), vec(0, 1, 0))
                time.sleep(1)
            elif function == "spawnObject":
                obj = parameters[0]
                if obj == "sphere":
                    sphere(pos = vector(parameters[1], parameters[2], parameters[3]), size = vector(0.5, 0.5, 0.5))
                    self.gm.collectibles.append((parameters[1], parameters[2], parameters[3]))
                elif obj == "cube":
                    box(pos = vector(parameters[1], parameters[2], parameters[3]))
                    self.gm.obstacles.append((parameters[1], parameters[2], parameters[3]))
            elif function == "isFacingNorth":
                res = self.gm.player.axis.x == 1.0
                self.memoryStack[-1].SEND_PARAMS.append(res)
            elif function == "isFacingSouth":
                res = self.gm.player.axis.x == -1.0
                self.memoryStack[-1].SEND_PARAMS.append(res)
            elif function == "isFacingEast":
                res = self.gm.player.axis.z == 1.0
                self.memoryStack[-1].SEND_PARAMS.append(res)
            elif function == "isFacingWest":
                res = self.gm.player.axis.z == -1.0
                self.memoryStack[-1].SEND_PARAMS.append(res)
            elif function == "start":
                x = parameters[0]
                y = parameters[1]
                z = parameters[2]
                if x > 20 or x < 0 or y > 20 or y < 0 or z > 20 or z < 0:
                    raiseError('Given coordinates are out of the allowed bounds.')
                self.gm.startPosition = (x, y, z)
            elif function == "goal":
                x = parameters[0]
                y = parameters[1]
                z = parameters[2]
                if x > 20 or x < 0 or y > 20 or y < 0 or z > 20 or z < 0:
                    raiseError('Given coordinates are out of the allowed bounds.')
                self.gm.goalPosition = (x, y, z)
            elif function == "print":
                print(parameters[0])
            elif function == "startMovement":
                self.gm.player = box(pos = vector(self.gm.startPosition[0], self.gm.startPosition[1], self.gm.startPosition[2]), color = color.red)
                attach_trail(self.gm.player)
            elif function == "outOfBounds":
                x = parameters[0]
                y = parameters[1]
                z = parameters[2]
                res = x > 20 or x < 0 or y > 20 or y < 0 or z > 20 or z < 0
                self.memoryStack[-1].SEND_PARAMS.append(res)
            elif function == "isCollectible":
                x = parameters[0]
                y = parameters[1]
                z = parameters[2]
                for collectible in self.gm.collectibles:
                    if self.gm.distance((x, y, z), collectible) <= 1:
                        res = True
                        self.memoryStack[-1].SEND_PARAMS.append(res)
                        return

                res = False
                self.memoryStack[-1].SEND_PARAMS.append(res)

            elif function == "isBlocked":
                x = parameters[0]
                y = parameters[1]
                z = parameters[2]
                coord = (x, y, z)
                print(self.gm.obstacles)
                print(coord)
                for obstacle in self.gm.obstacles:
                    if self.gm.distance((x, y, z), obstacle) <= 1:
                        res = True
                        self.memoryStack[-1].SEND_PARAMS.append(res)
                        return

                res = False
                self.memoryStack[-1].SEND_PARAMS.append(res)

    def processCuad(self, cuadruplo):

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

            #print('oper1 (', result, ') + (', oper2, ') = ', result)
            if self.memoryStack[-1].saveResult(result,cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                raiseError("Error in save result PLUS")

        elif cuadruplo.operator == MINUS:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            result = oper1 - oper2

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                raiseError("Error in save result MINUS")

        elif cuadruplo.operator == MULT:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            result = oper1 * oper2

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                raiseError("Error in save result MULT")

        elif cuadruplo.operator == DIV:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            oper2 = self.memoryStack[-1].getValue(cuadruplo.operand2)

            result = oper1 / oper2

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                raiseError("Error in save result DIV")

        elif cuadruplo.operator == ASSIGN:
            if len(self.subMem)!=0 and self.subMem[-1] == cuadruplo.operand1:
                if self.memoryStack[-1].saveResult(self.memoryStack[-1].RECEIVE_PARAMS[-1], int(self.memoryStack[-1].getAddress(cuadruplo.result))):
                    self.memoryStack[-1].RECEIVE_PARAMS.pop()
                    self.currentCuad[-1] += 1
                else:
                    print("case1.1.2")
            else:
                oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
                if self.memoryStack[-1].saveResult(oper1, int(self.memoryStack[-1].getAddress(cuadruplo.result))):
                    self.currentCuad[-1] += 1
                else:
                    raiseError("Error in save result EQUAL")

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
                raiseError("Error in save result OR")

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
                raiseError("Error in save result AND")

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
                raiseError("Error in save result LESS_THAN")

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
                raiseError("Error in save result GREAT_THAN")

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
                raiseError("Error in save result EQL_LESS_THAN")

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
                raiseError("Error in save result EQL_GREAT_THAN")

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
                raiseError("Error in save result EQL")

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
                raiseError("Error in save result DIF")

        elif cuadruplo.operator == NOT:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)

            if not oper1:
                result = True
            else:
                result = False

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                raiseError("Error in save result NOT")

        elif cuadruplo.operator == NEG:
            oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)

            result = oper1 * -1

            if self.memoryStack[-1].saveResult(result, cuadruplo.result):
                self.currentCuad[-1] += 1
            else:
                raiseError("Error in save result NEG")

        elif cuadruplo.operator == ERA:
            self.currentCuad[-1] += 1

        elif cuadruplo.operator == PARAM:
            oper1 = cuadruplo.operand1
            if cuadruplo.operand1 != 'cube' and cuadruplo.operand1 != 'sphere':
                oper1 = self.memoryStack[-1].getValue(cuadruplo.operand1)
            self.memoryStack[-1].SEND_PARAMS.append(oper1)
            self.currentCuad[-1] += 1

        elif cuadruplo.operator == GO_SUB:
            if cuadruplo.result == None:
                self.memoryStack.append(Mem.Memory())
                self.processReservedFunction(cuadruplo.operand1, self.memoryStack[-2].SEND_PARAMS)
                self.subMem.append(cuadruplo.operand1)
                # self.memoryStack[-1].RECEIVE_PARAMS = self.memoryStack[-2].SEND_PARAMS
                self.memoryStack[-2].SEND_PARAMS = []
                self.memoryStack.pop()
                self.currentCuad[-1] += 1
            else:
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

        elif cuadruplo.operator == VER:
            index = self.memoryStack[-1].getValue(cuadruplo.operand1);
            lowerBound = int(cuadruplo.operand2)
            upperBound = int(cuadruplo.result)
            if index >= lowerBound and index < upperBound:
                self.currentCuad[-1] += 1
            else:
                raiseError("Error: Array index out of bounds.")

        #print("")
