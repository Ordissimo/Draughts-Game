from Piece import Piece

class CrownPiece(Piece):
	def __init__(self, image, team):
		Piece.__init__(self, image, team)

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

	#To kill a enemy
	def makeKill(self, destiny, board):
		difLine = (destiny[0] - self.line)
		difCollum = (destiny[1] - self.collum)

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
			if board[enemyLine][enemyCollum] != 0:
				board[enemyLine][enemyCollum] = 0
		board[self.line][self.collum].makeMove(destiny, board)