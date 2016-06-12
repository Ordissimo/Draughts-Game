from abc import ABCMeta, abstractmethod

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

	#To move for another place
	def makeMove(self, destiny, board):
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
				print "enemy", enemyLine, enemyCollum
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

