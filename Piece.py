from abc import ABCMeta, abstractmethod
import copy

#Abrstract Class
# A piece of the game
class Piece:
	__metaclass__ = ABCMeta
	#Constructor
	def __init__(self, image, kind, team):
		self.image = image
		self.kind = kind
		self.team = team
		self.line = -1
		self.collum = -1
		self.valueBoard = [[4, 4, 4, 4, 4, 4, 4, 4],
						[4, 3, 3, 3, 3, 3, 3, 4],
						[4, 3, 2, 2, 2, 2, 3, 4],
						[4, 3, 2, 1, 1, 2, 3, 4],
						[4, 3, 2, 1, 1, 2, 3, 4],
						[4, 3, 2, 2, 2, 2, 3, 4],
						[4, 3, 3, 3, 3, 3, 3, 4],
						[10, 10, 10, 10, 10, 10, 10, 10]]

	#Return the current position of the piece
	def getPosition(self):
		return self.line, self.collum

	#Definy the piece position on the board
	def setPosition(self, newLine, newCollum):
		self.line = newLine
		self.collum = newCollum
	
	#Draw the piece in your respective position on the board
	def draw(self, screen):
		screen.blit(self.image, (80 + (self.collum*42), 80 + (self.line*42)))
	
	#Return if the line and collum reffered are in the perimeters of the board
	def inBoard(self, line, collum):
		if line < 0 or line >= 8:
			return False
		if collum < 0 or collum >= 8:
			return False
		return True
	
	#Choose the best movement
	def adaptAdvance(self, board):
		#Initialize variables
		adaptation = 0
		bestMove = [(-1,-1), (-1,-1)]
		moves = self.canMove(board)

		#See all Enemies possible positions
		allEnemiesWalk = []
		allEnemiesKill = []
		for i in range(0, 8):
			for j in range(0, 8):
				if board[i][j] != 0 and board[i][j].team == "red":
					allEnemiesWalk += board[i][j].canMove(board)
					allEnemiesKill += board[i][j].canKill(board)

		#for each move calculate your adaptation
		for i in range (0, len(moves)):
			newAdaptation = self.valueBoard[ moves[i][0] ][ moves[i][1] ]
			if moves[i] in allEnemiesKill:
				newAdaptation += 5
			elif moves[i] in allEnemiesWalk and newAdaptation < 4: #adaptation > 4 means it on the corner
				newAdaptation += -2
			#Take the highest adaptation
			if newAdaptation > adaptation:
				adaptation = newAdaptation
				bestMove = [(self.line, self.collum), moves[i]]

		return adaptation, bestMove



	#Choose the best move to eat most of enemy's piece
	def adaptKill(self, board):
		victims = board[self.line][self.collum].canKill(board)
		#See if can't kill
		if len(victims) == 0:
			return 0, []

		adapKill, bestPath = self.bestKillerPath(self.line, self.collum, 0, [], copy.deepcopy(board) )
		return adapKill, bestPath

	#Function that should find the best path reached by that piece. RECURSIVE FUNCTION
	def bestKillerPath(self, pieceLine, pieceCollum, adaptation, path, board):
		#print adaptation
		path.append((pieceLine, pieceCollum))
		nextVictims = board[pieceLine][pieceCollum].canKill(board)
		if len(nextVictims) == 0:
			return adaptation, path

		listPath = []
		index = 0
		for i in range(0, len(nextVictims)):
			#newNode = [(pieceLine, pieceCollum)]
			auxBoard = copy.deepcopy(board)
			auxBoard[pieceLine][pieceCollum].makeKill(nextVictims[i], auxBoard)
			aux, path = self.bestKillerPath(nextVictims[i][0], nextVictims[i][1], adaptation+2, path, auxBoard)
			listPath.append(copy.copy(path))
			path.pop()	
			if aux > adaptation:
				adaptation = aux
				index = i
		if len(listPath) > 0:
			path = listPath[index]
		return adaptation, path

	#To move for another place
	def makeMove(self, destiny, board):
		print "destiny", destiny
		board[destiny[0]][destiny[1]] = board[self.line][self.collum]
		board[self.line][self.collum] = 0
		self.line = destiny[0]
		self.collum = destiny[1]
		

	#To kill a enemy
	def makeKill(self, destiny, board):
		difLine = (destiny[0] - self.line)
		difCollum = (destiny[1] - self.collum)
		#A simple piece will be killed
		if board[self.line][self.collum].kind == "simple":
			enemyLine = self.line + (difLine/2)
			enemyCollum = self.collum + (difCollum/2)
			#print enemyLine, enemyCollum
			board[enemyLine][enemyCollum] = 0		
		#A crown piece will be killed
		else:
			difLine = difLine/abs(difLine) 
			difCollum = difCollum/abs(difCollum)
			enemyLine = self.line
			enemyCollum = self.collum
			crescent = 1
			if self.line > destiny[0]:
				crescent = -1
			for i in range(self.line, destiny[0], crescent):
				enemyLine += difLine
				enemyCollum += difCollum
				#print "enemy", enemyLine, enemyCollum
				if board[enemyLine][enemyCollum] != 0:
					board[enemyLine][enemyCollum] = 0
		board[self.line][self.collum].makeMove(destiny, board)

	#return a list of every piece that can eat some enemy's piece
	def isKiller(self, board):
		targets = board[self.line][self.collum].canKill(board)
		if len(targets) == 0:
			return False
		return True


	@abstractmethod
	def isEnemy(self, enemy):
		pass

	@abstractmethod
	def canMove(self, board):
		pass

	@abstractmethod
	def canKill(self, board):
		pass