import Piece

class BlackCrownPiece(Piece.Piece):
	def __init__(self, image, kind, team):
		Piece.Piece.__init__(self, image, kind, team)


	def isEnemy(self, enemy):
		if enemy != 0 and enemy.team == "red":
			return True
		return False

	#return all possible position where the piece can be moved
	def canMove(self, currentLine, currentCollum, board):
		possibleMoves = []

		j = currentCollum
		for i in range(currentLine+1, 8):
			j += 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break
		j = currentCollum
		for i in range(currentLine+1, 8):
			j -= 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break
		j = currentCollum
		for i in range(currentLine-1, -1, -1):
			j += 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break
		j = currentCollum
		for i in range(currentLine-1, -1, -1):
			j -= 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break
		return possibleMoves

	def canEat(self, currentLine, currentCollum, board):
		possibleMoves = []
		
		j = currentCollum
		firstEnemy = False
		for i in range(currentLine+1, 8):
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

		j = currentCollum
		firstEnemy = False
		for i in range(currentLine+1, 8):
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

		j = currentCollum
		firstEnemy = False
		for i in range(currentLine-1, -1, -1):
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

		j = currentCollum
		firstEnemy = False
		for i in range(currentLine-1, -1, -1):
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