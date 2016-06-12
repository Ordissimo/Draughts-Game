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
	#Draw the piece in your respective position on the board
	def draw(self, screen, x, y):
		screen.blit(self.image, (80 + (y*42), 80 + (x*42)))
	#Return if the line and collum reffered are in the perimeters of the board
	def inBoard(self, line, collum):
		if line < 0 or line >= 8:
			return False
		if collum < 0 or collum >= 8:
			return False
		return True

	def makeMove(self, origin, destiny, board):
		board[destiny[0]][destiny[1]] = board[origin[0]][origin[1]]
		board[origin[0]][origin[1]] = 0

	def Eat(self, origin, destiny, board):
		board[origin[0]][origin[1]].makeMove(origin, destiny, board)
		difLine = (destiny[0] - origin[0])
		difCollum = (destiny[1] - origin[1])
		#A simple piece will be killed
		if board[destiny[0]][destiny[1]].kind == "simple":
			enemyLine = origin[0] + (difLine/2)
			enemyCollum = origin[1] + (difCollum/2)
			#print enemyLine, enemyCollum
			board[enemyLine][enemyCollum] = 0
			
		#A crown piece will be killed
		else:
			difLine = difLine/abs(difLine) 
			difCollum = difCollum/abs(difCollum)
			enemyLine = origin[0]
			enemyCollum = origin[1]
			crescent = 1
			if origin[0] > destiny[0]:
				crescent = -1
			for i in range(origin[0], destiny[0]-1, crescent):
				enemyLine += difLine
				enemyCollum += difCollum
				if board[enemyLine][enemyCollum] != 0:
					board[enemyLine][enemyCollum] = 0



	@abstractmethod
	def isEnemy(self, enemy):
		pass

	@abstractmethod
	def canMove(self, currentLine, currentCollum, destinyLine, destinyCollum, board):
		pass

	@abstractmethod
	def canEat(self, currentLine, currentCollum, destinyLine, destinyCollum, board):
		pass

