from Piece import Piece

class CrownPiece(Piece):
	def __init__(self, image, team):
		Piece.__init__(self, image, "crown", team)

	#return all possible position where the piece can be moved
	def canMove(self, board):
		possibleMoves = []
		#down-right
		j = self.collum
		for i in range(self.line+1, 8):
			j += 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break
		#down-left
		j = self.collum
		for i in range(self.line+1, 8):
			j -= 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break
		#up-right
		j = self.collum
		for i in range(self.line-1, -1, -1):
			j += 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break
		#up-left
		j = self.collum
		for i in range(self.line-1, -1, -1):
			j -= 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break	
		return possibleMoves

	#Return all possible position where a enemy's piece will be killed
	def canKill(self, board):
		possibleMoves = []
		#down-right
		j = self.collum
		firstEnemy = False
		for i in range(self.line+1, 8):
			j += 1
			if firstEnemy:
				if self.inBoard(i, j) and board[i][j]== 0:
					possibleMoves.append((i, j))
				else:
					break
			if (not firstEnemy) and self.inBoard(i, j) and board[i][j] != 0:
				if self.isEnemy(board[i][j]):
					firstEnemy = True
				else: 
					break
		#down-left
		j = self.collum
		firstEnemy = False
		for i in range(self.line+1, 8):
			j -= 1
			if firstEnemy:
				if self.inBoard(i, j) and board[i][j]== 0:
					possibleMoves.append((i, j))
				else:
					break
			if (not firstEnemy) and self.inBoard(i, j) and board[i][j] != 0:
				if self.isEnemy(board[i][j]):
					firstEnemy = True
				else: 
					break
		#up-right
		j = self.collum
		firstEnemy = False
		for i in range(self.line-1, -1, -1):
			j += 1
			if firstEnemy:
				if self.inBoard(i, j) and board[i][j]== 0:
					possibleMoves.append((i, j))
				else:
					break
			if (not firstEnemy) and self.inBoard(i, j) and board[i][j] != 0:
				if self.isEnemy(board[i][j]):
					firstEnemy = True
				else: 
					break
		#up-left
		j = self.collum
		firstEnemy = False
		for i in range(self.line-1, -1, -1):
			j -= 1
			if firstEnemy:
				if self.inBoard(i, j) and board[i][j]== 0:
					possibleMoves.append((i, j))
				else:
					break
			if (not firstEnemy) and self.inBoard(i, j) and board[i][j] != 0:
				if self.isEnemy(board[i][j]):
					firstEnemy = True
				else: 
					break

		return possibleMoves