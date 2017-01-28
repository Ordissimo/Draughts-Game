from abc import ABCMeta, abstractmethod
import copy

#Abrstract Class
# A piece of the game
class Piece:
	__metaclass__ = ABCMeta
	#Constructor
	def __init__(self, image, team):
		self.image = image
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

	#reset the content of valueBoard
	def resetValueBoard(self):
		self.valueBoard = [[4, 4, 4, 4, 4, 4, 4, 4],
						[4, 3, 3, 3, 3, 3, 3, 4],
						[4, 3, 2, 2, 2, 2, 3, 4],
						[4, 3, 2, 1, 1, 2, 3, 4],
						[4, 3, 2, 1, 1, 2, 3, 4],
						[4, 3, 2, 2, 2, 2, 3, 4],
						[4, 3, 3, 3, 3, 3, 3, 4],
						[10, 10, 10, 10, 10, 10, 10, 10]]

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
	
	#See if the piece it's a enemy
	def isEnemy(self, enemy):
		if enemy != None and enemy.team != self.team:
			return True
		return False

	#Choose the best movement
	def adaptAdvance(self, board):
		#Initialize variables
		adaptation = -100
		bestMove = [(-1,-1), (-1,-1)]
		moves = self.canMove(board)

		#See all Enemies possible positions
		allEnemiesWalk = []
		allEnemiesKill = []
		for i in range(0, 8):
			for j in range(0, 8):
				if board[i][j] != None and board[i][j].team == "red":
					allEnemiesWalk += board[i][j].canMove(board)
					allEnemiesKill += board[i][j].canKill(board)

		#for each move calculate your adaptation
		for i in range (0, len(moves)):
			newAdaptation = self.valueBoard[ moves[i][0] ][ moves[i][1] ]
			if moves[i] in allEnemiesKill:
				newAdaptation += 5
			elif moves[i] in allEnemiesWalk and newAdaptation < 4: #adaptation >= 4 means it on the corner
				newAdaptation += -2
			#Take the highest adaptation
			if newAdaptation > adaptation:
				adaptation = newAdaptation
				bestMove = [(self.line, self.collum), moves[i]]

		return adaptation, bestMove

	#See if it's a good ideia don't move this piece
	def shouldStay(self, destiny, board):
		#Another board to make simulations of moves
		auxBoard = copy.deepcopy(board)

		origin = (self.line, self.collum)
		auxBoard[self.line][self.collum].makeMove(destiny, auxBoard)
		for i in range(0, 8):
			for j in range(0, 8):
				if auxBoard[i][j] != None and auxBoard[i][j].team == "red":
					allEnemiesKill += auxBoard[i][j].canKill(auxBoard)
					allEnemiesWalk += board[i][j].canMove(board)

		result = 0
		if origin[0] == 0:
			result +=1
			if origin in allEnemiesWalk:
				result += 2
		if origin in allEnemiesKill:
			result+=2
		
		return result

	#Choose the best move to eat most of enemy's piece
	def adaptKill(self, enemyPieces, board):
		victims = board[self.line][self.collum].canKill(board)
		#See if can't kill
		if len(victims) == 0:
			return 0, []

		adapKill, bestPath = self.bestKillerPath(self.line, self.collum, 0, [], copy.deepcopy(enemyPieces),copy.deepcopy(board) )
		return adapKill, bestPath

	#Function that should find the best path reached by that piece. RECURSIVE FUNCTION
	def bestKillerPath(self, pieceLine, pieceCollum, adaptation, path, enemyPieces, board):
		#print adaptation
		path.append((pieceLine, pieceCollum))
		nextVictims = board[pieceLine][pieceCollum].canKill(board)
		if len(nextVictims) == 0:
			return adaptation, path

		listPath = []
		index = 0
		for i in range(0, len(nextVictims)):
			auxBoard = copy.deepcopy(board)
			auxBoard[pieceLine][pieceCollum].makeKill(nextVictims[i], enemyPieces, auxBoard)
			aux, path = self.bestKillerPath(nextVictims[i][0], nextVictims[i][1], adaptation+2, path, enemyPieces, auxBoard)
			listPath.append(copy.copy(path))
			path.pop()	
			if aux > adaptation:
				adaptation = aux
				index = i
		if len(listPath) > 0:
			path = listPath[index]
		return adaptation, path

	#return a list of every piece that can eat some enemy's piece
	def isKiller(self, board):
		targets = board[self.line][self.collum].canKill(board)
		if len(targets) == 0:
			return False
		return True

	#To move for another place
	def makeMove(self, destiny, board):
		board[destiny[0]][destiny[1]] = board[self.line][self.collum]
		board[self.line][self.collum] = None
		self.line = destiny[0]
		self.collum = destiny[1]
		

	@abstractmethod
	def canMove(self, board):
		pass

	@abstractmethod
	def canKill(self, board):
		pass

	@abstractmethod
	def makeKill(self, destiny, enemyPieces, board):
		pass