import math

# Logic used during Pichon's execution phase
class GameManager:
	def __init__(self):
		self.player = None					# Box representing the user
		self.startPosition = (10, 10, 10)	# Starting position
		self.goalPosition = (15, 15, 15)	# Position that the user needs to reach
		self.obstacles = []					# Array of coordinates where obstacles have been placed
		self.collectibles = []				# Array of coordinates where collectibles have been placed
		self.speed = 1.0					# Speed at which the player performs actions
		self.score = None					# Label to display the user's score
		self.warning = None					# Label to display a warning when a the user can't move forward
		self.collectibleObjects = []		# Array with collectible objects
		self.obstacleObjects = []			# Array with obstacle objects
		self.totalCollectibles = 0			# Total amount of collectbiles defined
		self.collected = 0					# Amount of collectibles collected
		self.minDim = 0						# Minimum (x, y, z) coordinate of the environment
		self.maxDim = 20					# Maximum (x, y, z) cooridnate of the environment

	# Get the Euclidean distance between coord1 and coord2
	def distance(self, coord1, coord2):
		x1 = coord1[0]
		y1 = coord1[1]
		z1 = coord1[2]
		x2 = coord2[0]
		y2 = coord2[1]
		z2 = coord2[2]
		dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
		return dist

	# Remove collectibles that are less than 0.5 units from the player and count them toward
	# the user's score
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

	# Returns True if there's an obstacle at at most 1 unit from the given coordinate
	def isBlocked(self, coord):
		for obstacle in self.obstacles:
		    if self.distance(coord, obstacle) < 1:
		        return True

		return False

	# Check if the user won the game. Return true if the player is at most 0.5 units from the goal and
	# has collected all the collectible objects.
	def checkWin(self):
		playerCoord = (self.player.pos.x, self.player.pos.y, self.player.pos.z)
		if self.distance(playerCoord, self.goalPosition) <= 0.5 and self.collected == self.totalCollectibles:
			return True
		else:
			return False

	# Return True if the given coordinate exceeds the minimum and maximum size of the environment
	def outOfBounds(self, coord1):
		x = coord1[0]
		y = coord1[1]
		z = coord1[2]
		return x > self.maxDim or x < self.minDim or y > self.maxDim or y < self.minDim or z > self.maxDim or z < self.minDim

	# Return true if the position where the player would end if he had moved forward is not blocked nor out of bounds
	def canMoveForward(self):
		forwardPos = self.player.pos + self.player.axis
		forwardCoord = (forwardPos.x, forwardPos.y, forwardPos.z)
		if self.outOfBounds(forwardCoord) or self.isBlocked(forwardCoord):
			return False
		else:
			return True
