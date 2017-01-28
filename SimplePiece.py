from Piece import Piece

class SimplePiece(Piece):
	def __init__(self, image, orientation, team):
		Piece.__init__(self, image, team)
		self.orientation = orientation

	#return all possible position where the piece can be moved
	def canMove(self, board):
		possibleMoves = []
		#up-lef or down-left
		if self.inBoard(self.line + self.orientation, self.collum-1) and board[self.line + self.orientation][self.collum-1] == None:
			possibleMoves.append((self.line+ self.orientation, self.collum-1))
		#up-right or down-right
		if self.inBoard(self.line + self.orientation,self.collum+1) and board[self.line + self.orientation][self.collum+1] == None:
			possibleMoves.append((self.line+ self.orientation, self.collum+1))

		return possibleMoves

	#Return all possible position where a enemy's piece will be killed
	def canKill(self, board):
		possibleMoves = []
		#up-left
		if self.inBoard(self.line-1, self.collum-1) and self.isEnemy(board[self.line-1][self.collum-1]):
			if self.inBoard(self.line-2, self.collum-2) and board[self.line-2][self.collum-2] == None:
				possibleMoves.append((self.line-2, self.collum-2))
		#up-right
		if self.inBoard(self.line-1, self.collum+1) and self.isEnemy(board[self.line-1][self.collum+1]):
			if self.inBoard(self.line-2, self.collum+2) and board[self.line-2][self.collum+2] == None:
				possibleMoves.append((self.line-2, self.collum+2))
		#down-left
		if self.inBoard(self.line+1,self.collum-1) and self.isEnemy(board[self.line+1][self.collum-1]):
			if self.inBoard(self.line+2,self.collum-2) and board[self.line+2][self.collum-2] == None:
				possibleMoves.append((self.line+2, self.collum-2))
		#down-right
		if self.inBoard(self.line+1,self.collum+1) and self.isEnemy(board[self.line+1][self.collum+1]):
			if self.inBoard(self.line+2,self.collum+2) and board[self.line+2][self.collum+2] == None:
				possibleMoves.append((self.line+2, self.collum+2))
		return possibleMoves

	#To kill a enemy
	def makeKill(self, destiny, enemyPieces, board):

		difLine = (destiny[0] - self.line)
		difCollum = (destiny[1] - self.collum)

		#Killing the enemy
		enemyLine = self.line + (difLine/2)
		enemyCollum = self.collum + (difCollum/2)
		board[enemyLine][enemyCollum] = None
		for i in range(len(enemyPieces)):
			enemy = enemyPieces[i]
			if enemy.line == enemyLine and enemy.collum == enemyCollum:
				del enemyPieces[i]
				break
		board[self.line][self.collum].makeMove(destiny, board)
		