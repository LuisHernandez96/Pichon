import math

class GameManager:
	def __init__(self):
		self.player = None
		self.startPosition = (0, 0, 0)
		self.goalPosition = (5, 0, 0)
		self.obstacles = []
		self.collectibles = []
		self.speed = 1.0
		self.score = None
		self.collectibleObjects = []
		self.obstacleObjects = []
		self.totalCollectibles = 0
		self.collected = 0

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