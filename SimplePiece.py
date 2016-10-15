from Piece import Piece

class SimplePiece(Piece):
	def __init__(self, image, orientation, team):
		Piece.__init__(self, image, team)
		self.orientation = orientation

	#return all possible position where the piece can be moved
	def canMove(self, board):
		possibleMoves = []
		#up-lef
		if self.inBoard(self.line + self.orientation, self.collum-1) and board[self.line + self.orientation][self.collum-1] == 0:
			possibleMoves.append((self.line+ self.orientation, self.collum-1))
		#up-right
		if self.inBoard(self.line + self.orientation,self.collum+1) and board[self.line + self.orientation][self.collum+1] == 0:
			possibleMoves.append((self.line+ self.orientation, self.collum+1))
		return possibleMoves

	#Return all possible position where a enemy's piece will be killed
	def canKill(self, board):
		possibleMoves = []
		#up-left
		if self.inBoard(self.line-1, self.collum-1) and self.isEnemy(board[self.line-1][self.collum-1]):
			if self.inBoard(self.line-2, self.collum-2) and board[self.line-2][self.collum-2] == 0:
				possibleMoves.append((self.line-2, self.collum-2))
		#up-right
		if self.inBoard(self.line-1, self.collum+1) and self.isEnemy(board[self.line-1][self.collum+1]):
			if self.inBoard(self.line-2, self.collum+2) and board[self.line-2][self.collum+2] == 0:
				possibleMoves.append((self.line-2, self.collum+2))
		#down-left
		if self.inBoard(self.line+1,self.collum-1) and self.isEnemy(board[self.line+1][self.collum-1]):
			if self.inBoard(self.line+2,self.collum-2) and board[self.line+2][self.collum-2] == 0:
				possibleMoves.append((self.line+2, self.collum-2))
		#down-right
		if self.inBoard(self.line+1,self.collum+1) and self.isEnemy(board[self.line+1][self.collum+1]):
			if self.inBoard(self.line+2,self.collum+2) and board[self.line+2][self.collum+2] == 0:
				possibleMoves.append((self.line+2, self.collum+2))
		return possibleMoves