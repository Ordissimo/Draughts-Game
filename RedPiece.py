import Piece

class RedPiece(Piece.Piece):
	def __init__(self, image, kind, team):
		Piece.Piece.__init__(self, image, kind, team)

	def isEnemy(self, enemy):
		if enemy != 0 and enemy.team == "black":
			return True
		return False

	#return all possible position where the piece can be moved
	def canMove(self, currentLine, currentCollum, board):
		possibleMoves = []
		#up-lef
		if self.inBoard(currentLine-1,currentCollum-1) and board[currentLine-1][currentCollum-1] == 0:
			possibleMoves.append((currentLine-1, currentCollum-1))
		#up-right
		if self.inBoard(currentLine-1,currentCollum+1) and board[currentLine-1][currentCollum+1] == 0:
			possibleMoves.append((currentLine-1, currentCollum+1))
		return possibleMoves

	def canEat(self, currentLine, currentCollum, board):
		possibleMoves = []
		#up-left
		if self.inBoard(currentLine-1,currentCollum-1) and self.isEnemy(board[currentLine-1][currentCollum-1]):
			if self.inBoard(currentLine-2,currentCollum-2) and board[currentLine-2][currentCollum-2] == 0:
				possibleMoves.append((currentLine-2, currentCollum-2))
		#up-right
		if self.inBoard(currentLine-1,currentCollum+1) and self.isEnemy(board[currentLine-1][currentCollum+1]):
			if self.inBoard(currentLine-2,currentCollum+2) and board[currentLine-2][currentCollum+2] == 0:
				possibleMoves.append((currentLine-2, currentCollum+2))
		#down-left
		if self.inBoard(currentLine+1,currentCollum-1) and self.isEnemy(board[currentLine+1][currentCollum-1]):
			if self.inBoard(currentLine+2,currentCollum-2) and board[currentLine+2][currentCollum-2] == 0:
				possibleMoves.append((currentLine+2, currentCollum-2))
		#down-right
		if self.inBoard(currentLine+1,currentCollum+1) and self.isEnemy(board[currentLine+1][currentCollum+1]):
			if self.inBoard(currentLine+2,currentCollum+2) and board[currentLine+2][currentCollum+2] == 0:
				possibleMoves.append((currentLine+2, currentCollum+2))
		return possibleMoves