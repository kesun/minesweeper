from random import randint

class Grid:
	heightNum = None
	widthNum = None
	minesNum = None
	staticField = None

	def __init__(self, widthNum, heightNum, minesNum):
		self.heightNum = heightNum
		self.widthNum = widthNum
		self.minesNum = minesNum
		self.mines = []
		self.flags = []
		self.state = 0

		if self.staticField is None:
			self.initField()
			self.staticField = self.field
		else:
			self.field = self.staticField

	def __repr__(self):
		return "Test()"
	def __str__(self):
		return "member of Grid"

	###### CELL DEFINITION ######
	def makeCell(self, row, col):
		return {
			'x': row,
			'y': col,
			'isMine': False,
			'isRevealed': False,
			'isFlagged': False,
			'mineCount': 0
		}

	def getCell(self, y, x):
		cell = self.field[int(x)][int(y)]
		return cell

	### setCell do not use this; use markMine and markFlag instead ## 

	def markMine(self, x, y):
		# print("markMine", x, y)
		self.getCell(x, y)['isMine'] = True

	def markFlag(self, x, y):
		curCell = self.getCell(x, y)
		if curCell['isFlagged'] is True:
			curCell['isFlagged'] = False
		else:
			curCell['isFlagged'] = True

	def markRevealed(self, x, y):
		self.getCell(x, y)['isRevealed'] = True

	def setMineCount(self, x, y, count):
		self.getCell(x, y)['mineCount'] = count

	###### INITIALIZATION ######
	def initField(self):
		self.field = [[self.makeCell(w, h) for w in range(self.widthNum)] for h in range(self.heightNum)]
		
		self.initMines()
		self.initNumbers()

	def initMines(self):
		while len(self.mines) < self.minesNum:
			w = randint(0, self.widthNum - 1)
			h = randint(0, self.heightNum - 1)
			mineLoc = (w, h)

			if mineLoc not in self.mines:
				self.markMine(w, h)
				self.mines.append(mineLoc)

	def initNumbers(self):
		for x in range(self.widthNum):
			for y in range(self.heightNum):
				mineCount = self.countMines(self.findNeighbours(x, y))
				# print("initNumbers", x, y, mineCount)
				if mineCount > 0:
					self.setMineCount(x, y, mineCount)

	###### PLAYER ACTIONS ######
	def pokeCell(self, x, y, event):
		# Make sure the state of the cell is actually set!
		if event == 'leftClick':
			self.openCell(x, y)
		else:
			self.flagCell(x, y)

	def openCell(self, x, y):
		curCell = self.getCell(x, y)
		if not curCell['isRevealed'] and not curCell['isFlagged']:
			if curCell['isMine']:
				self.state = -1
				self.revealMines()
			elif curCell['mineCount'] == 0:
				self.oolala(curCell)
			curCell['isRevealed'] = True
			self.isVictory()

	def flagCell(self, x, y):
		curCell = self.getCell(x, y)
		if not curCell['isRevealed']:
			if curCell['isFlagged']:
				curCell['isFlagged'] = False
			else:
				curCell['isFlagged'] = True

	###### HELPERS ######
	def findNeighbours(self, x, y):
		SURROUNDING = ((-1, -1), (-1,  0), (-1,  1),
                       (0 , -1),           (0 ,  1),
                       (1 , -1), (1 ,  0), (1 ,  1))
		neighbours = []
		coords = [(x + surr_row, y + surr_col) for (surr_row, surr_col) in SURROUNDING]
		for coord in coords:
			if coord[0] >= 0 and coord[0] < self.widthNum and coord[1] >= 0 and coord[1] < self.heightNum:
				neighbours.append(self.getCell(coord[0], coord[1]))
		return neighbours

	def countMines(self, neighbours):
		counter = 0
		for cell in neighbours:
			if cell['isMine']:
				counter+=1
		return counter

	def revealMines(self):
		for mine in self.mines:
			self.getCell(mine[0], mine[1])['isRevealed'] = True

	def oolala(self, cell):
		if not cell['isRevealed']:
			cell['isRevealed'] = True

			if cell['mineCount'] == 0:
				neighbours = self.findNeighbours(cell['x'], cell['y'])
				for neighbour in neighbours:
					if not neighbour['isRevealed'] and not neighbour['isFlagged']:
						self.oolala(neighbour)

	def isVictory(self):
		emptySpaces = 0
		for rows in self.staticField:
			for cell in rows:
				if cell['isRevealed'] == False or cell['isFlagged'] == True:
					emptySpaces += 1
		print('emptySpaces', emptySpaces, 'versus minesNum', self.minesNum)
		if emptySpaces == self.minesNum and self.state == 0:
			self.state = 1