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
        if(self.gm.checkWin()):
            self.gm.warning = label(pos = vector(self.gm.player.pos.x, self.gm.player.pos.y + 0.8, self.gm.player.pos.z), text='You won!')
        else:
            self.gm.warning = label(pos = vector(self.gm.player.pos.x, self.gm.player.pos.y + 0.8, self.gm.player.pos.z), text='Try again!')
        print("Finished!")

    def processReservedFunction(self, function, parameters):
            if function == "down":
                nextPos = self.gm.player.pos - self.gm.player.up
                nextPosCoord = (nextPos.x, nextPos.y, nextPos.z)
                if not self.gm.outOfBounds(nextPosCoord) and not self.gm.isBlocked(nextPosCoord):
                    self.gm.warning.visible = False
                    self.gm.player.pos = self.gm.player.pos - self.gm.player.up
                    self.gm.checkCollectibles()
                else:
                    self.gm.warning.pos = self.gm.player.pos + 0.8 * self.gm.player.up
                    self.gm.warning.visible = True
                time.sleep(1/self.gm.speed)
            elif function == "up":
                nextPos = self.gm.player.pos + self.gm.player.up
                nextPosCoord = (nextPos.x, nextPos.y, nextPos.z)
                if not self.gm.outOfBounds(nextPosCoord) and not self.gm.isBlocked(nextPosCoord):
                    self.gm.warning.visible = False
                    self.gm.player.pos = self.gm.player.pos + self.gm.player.up
                    self.gm.checkCollectibles()
                else:
                    self.gm.warning.pos = self.gm.player.pos + 0.8 * self.gm.player.up
                    self.gm.warning.visible = True
                time.sleep(1/self.gm.speed)
            elif function == "forward":
                nextPos = self.gm.player.pos + self.gm.player.axis
                nextPosCoord = (nextPos.x, nextPos.y, nextPos.z)
                if not self.gm.outOfBounds(nextPosCoord) and not self.gm.isBlocked(nextPosCoord):
                    self.gm.warning.visible = False
                    self.gm.player.pos = self.gm.player.pos + self.gm.player.axis
                    self.gm.checkCollectibles()
                else:
                    self.gm.warning.pos = self.gm.player.pos + 0.8 * self.gm.player.up
                    self.gm.warning.visible = True
                time.sleep(1/self.gm.speed)
            elif function == "turnLeft":
                self.gm.player.rotate(radians(90), vec(0, 1, 0))
                time.sleep(1/self.gm.speed)
            elif function == "turnRight":
                self.gm.player.rotate(radians(-90), vec(0, 1, 0))
                time.sleep(1/self.gm.speed)
            elif function == "spawnObject":
                obj = parameters[0]
                if obj == "sphere":
                    collectible = sphere(pos = vector(parameters[1], parameters[2], parameters[3]), size = vector(0.5, 0.5, 0.5))
                    self.gm.totalCollectibles += 1
                    self.gm.collectibles.append((parameters[1], parameters[2], parameters[3]))
                    self.gm.collectibleObjects.append(collectible)
                elif obj == "cube":
                    obstacle = box(pos = vector(parameters[1], parameters[2], parameters[3]))
                    self.gm.obstacles.append((parameters[1], parameters[2], parameters[3]))
                    self.gm.obstacleObjects.append(obstacle)
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
                if x > self.gm.maxDim or x < self.gm.minDim or y > self.gm.maxDim or y < self.gm.minDim or z > self.gm.maxDim or z < self.gm.minDim:
                    raiseError('Start coordinates are out of the allowed bounds.')
                self.gm.startPosition = (x, y, z)
            elif function == "goal":
                x = parameters[0]
                y = parameters[1]
                z = parameters[2]
                if x > self.gm.maxDim or x < self.gm.minDim or y > self.gm.maxDim or y < self.gm.minDim or z > self.gm.maxDim or z < self.gm.minDim:
                    raiseError('Goal coordinates are out of the allowed bounds.')
                self.gm.goalPosition = (x, y, z)
            elif function == "print":
                print(parameters[0])
            elif function == "startMovement":
                scene.title = 'Pichon - Starting position: {} - Goal position: {} - Collectibles: {}'.format(self.gm.startPosition, self.gm.goalPosition, len(self.gm.collectibles))
                self.gm.score = label(pos = vector(self.gm.goalPosition[0], self.gm.goalPosition[1] + 1, self.gm.goalPosition[2]), text='Collectibles: 0/{}'.format(len(self.gm.collectibles)))
                self.gm.warning = label(pos = vector(self.gm.startPosition[0], self.gm.startPosition[1] + 0.2, self.gm.startPosition[2]), text='Cannot perform action!', visible = False)
                self.gm.player = box(pos = vector(self.gm.startPosition[0], self.gm.startPosition[1], self.gm.startPosition[2]), color = color.red)
                ring(pos = vector(self.gm.goalPosition[0], self.gm.goalPosition[1], self.gm.goalPosition[2]), radius = 0.5, thickness = 0.1, axis = vector(0, 1, 0))
                attach_trail(self.gm.player)
            elif function == "outOfBounds":
                x = parameters[0]
                y = parameters[1]
                z = parameters[2]
                res = x > self.gm.maxDim or x < self.gm.minDim or y > self.gm.maxDim or y < self.gm.minDim or z > self.gm.maxDim or z < self.gm.minDim
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
                for obstacle in self.gm.obstacles:
                    if self.gm.distance((x, y, z), obstacle) <= 1:
                        res = True
                        self.memoryStack[-1].SEND_PARAMS.append(res)
                        return

                res = False
                self.memoryStack[-1].SEND_PARAMS.append(res)
            elif function == "setMovementSpeed":
                self.gm.speed = parameters[0]
            elif function == "canMoveForward":
                res = self.gm.canMoveForward()
                self.memoryStack[-1].SEND_PARAMS.append(res)
            elif function == "position":
                self.memoryStack[-1].SEND_PARAMS.insert(0, self.gm.player.pos.x)
                self.memoryStack[-1].SEND_PARAMS.insert(0, self.gm.player.pos.y)
                self.memoryStack[-1].SEND_PARAMS.insert(0, self.gm.player.pos.z)

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
                if len(self.memoryStack[-1].SEND_PARAMS) > 0:
                    self.subMem.append(cuadruplo.operand1)
                self.memoryStack[-2].RECEIVE_PARAMS = self.memoryStack[-1].SEND_PARAMS
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
            returnSize = self.memoryStack[-1].getCurrentFuncReturnSize()
            for i in range(0, returnSize):
                oper1 = self.memoryStack[-1].getValue(cuadruplo.result + i)
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
