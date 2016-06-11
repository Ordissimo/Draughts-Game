import Piece

class RedCrownPiece(Piece.Piece):
	def __init__(self, image, kind, team):
		Piece.Piece.__init__(self, image, kind, team)

	def isEnemy(self, enemy):
		if enemy != 0 and enemy.team == "black":
			return True
		return False
	'''
	def searchEnemy(self, currentLine, currentCollum, destinyLine, destinyCollum, board):
		difLine = currentLine - destinyLine
		difCollum = currentCollum - destinyCollum
		#print "difLine:", difLine, "difCollum:", difCollum
		if difLine > 0: #if it's up
			if difCollum > 0: #if it's up-left
				j = currentCollum-1
				for i in range(currentLine-1, destinyLine, -1):
					if(isinstance(board[i][j], Piece.Piece)):
						return i, j
					j -= 1

			else: #if it's up-right
				j = currentCollum+1
				for i in range(currentLine-1, destinyLine, -1):
					if(isinstance(board[i][j], Piece.Piece)):
						return i, j
					j += 1		
			
		else: #if it's down
			if difCollum > 0: #if it's down-left
				j = currentCollum-1
				for i in range(currentLine+1, destinyLine):
					if(isinstance(board[i][j], Piece.Piece)):
						return i, j
					j -= 1
				
			else: #if it's down-right
				j = currentCollum+1
				for i in range(currentLine+1, destinyLine):
					if(isinstance(board[i][j], Piece.Piece)):
						return i, j
					j += 1
		return -1, -1				
	'''
	#return all possible position where the piece can be moved
	def canMove(self, currentLine, currentCollum, board):
		possibleMoves = []

		#down-right
		j = currentCollum
		for i in range(currentLine+1, 8):
			j += 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break
		#down-left
		j = currentCollum
		for i in range(currentLine+1, 8):
			j -= 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break
		#up-right
		j = currentCollum
		for i in range(currentLine-1, -1, -1):
			j += 1
			if self.inBoard(i, j) and board[i][j]== 0:
				possibleMoves.append((i, j))
			else:
				break
		#up-left
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