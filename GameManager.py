import math

class GameManager:
	def __init__(self):
		self.player = None
		self.startPosition = (10, 10, 10)
		self.goalPosition = (15, 15, 15)
		self.obstacles = []
		self.collectibles = []
		self.speed = 1.0
		self.score = None
		self.warning = None
		self.collectibleObjects = []
		self.obstacleObjects = []
		self.totalCollectibles = 0
		self.collected = 0
		self.minDim = 0
		self.maxDim = 20

	def distance(self, coord1, coord2):
		x1 = coord1[0]
		y1 = coord1[1]
		z1 = coord1[2]
		x2 = coord2[0]
		y2 = coord2[1]
		z2 = coord2[2]
		dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
		return dist

	def checkCollectibles(self):
		playerPos = (self.player.pos.x, self.player.pos.y, self.player.pos.z)
		toRemove = []
		for i in range(0, len(self.collectibles)):
			collectible = self.collectibles[i]
			if self.distance(playerPos, collectible) < 0.5:
				self.collectibleObjects[i].visible = False
				self.collected += 1
				toRemove.append(i)

		removed = 0
		for index in toRemove:
			self.collectibles.pop(index - removed)
			self.collectibleObjects.pop(index - removed)
			removed += 1

		self.score.text = 'Collectibles: {}/{}'.format(self.collected, self.totalCollectibles)

	def isBlocked(self, coord):
		for obstacle in self.obstacles:
		    if self.distance(coord, obstacle) < 1:
		        return True

		return False

	def checkWin(self):
		playerCoord = (self.player.pos.x, self.player.pos.y, self.player.pos.z)
		if self.distance(playerCoord, self.goalPosition) <= 0.5 and self.collected == self.totalCollectibles:
			return True
		else:
			return False

	def outOfBounds(self, coord1):
		x = coord1[0]
		y = coord1[1]
		z = coord1[2]
		return x > self.maxDim or x < self.minDim or y > self.maxDim or y < self.minDim or z > self.maxDim or z < self.minDim

	def canMoveForward(self):
		forwardPos = self.player.pos + self.player.axis
		forwardCoord = (forwardPos.x, forwardPos.y, forwardPos.z)
		if self.outOfBounds(forwardCoord) or self.isBlocked(forwardCoord):
			return False
		else:
			return True
