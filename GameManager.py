import math

class GameManager:
	def __init__(self):
		self.player = None
		self.startPosition = (0, 0, 0)
		self.goalPosition = (5, 0, 0)
		self.obstacles = []
		self.collectibles = []

	def distance(self, coord1, coord2):
		x1 = coord1[0]
		y1 = coord1[1]
		z1 = coord1[2]
		x2 = coord2[0]
		y2 = coord2[1]
		z2 = coord2[2]
		dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
		return dist