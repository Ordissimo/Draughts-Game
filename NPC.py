from Piece import Piece
import copy

#Ignore this method
def thing(piece):
	if piece == 0:
		return "0";
	if piece.team == "red":
		return "redOne"
	if piece.team == "black":
		return "blackOne"

class NPC:
	#Constructor
	def __init__(self):
		self.valueBoard = [[4, 4, 4, 4, 4, 4, 4, 4],
						[4, 3, 3, 3, 3, 3, 3, 4],
						[4, 3, 2, 2, 2, 2, 3, 4],
						[4, 3, 2, 1, 1, 2, 3, 4],
						[4, 3, 2, 1, 1, 2, 3, 4],
						[4, 3, 2, 2, 2, 2, 3, 4],
						[4, 3, 3, 3, 3, 3, 3, 4],
						[10, 10, 10, 10, 10, 10, 10, 10]]

	def findAllBlack(self, board):
		blackPositions = []

		for i in range(0, 8):
			for j in range(0, 8):
				if board[i][j] != 0 and board[i][j].team == "black":
					blackPositions.append((i, j))
		return blackPositions

	#return a list of every piece that can eat some enemy's piece
	def searchKillers(self, list, board):
		listKillers = []
		for i in range(0, len(list)):
			if board[list[i][0]][list[i][1]].isKiller(board):
				listKillers.append(list[i])
		return listKillers

	#Choose the next movement
	def standartMove(self, piecesList, board):
		adaptation = 0
		movement = [(-1, -1), (-1,-1)]
		for i in range (0, len(piecesList)):
			newAdaptation, newMovement = board[piecesList[i][0]][piecesList[i][1]].adaptMove(board)
			if newAdaptation > adaptation:
				adaptation = newAdaptation
				movement = newMovement
		return adaptation, movement

	#Function that should find the best path reached by that piece. RECURSIVE FUNCTION
	def killingQuantity(self, pieceLine, pieceCollum, adaptation, path, board):
		#print adaptation
		path.append((pieceLine, pieceCollum))
		keepKilling = board[pieceLine][pieceCollum].canKill(board)
		if len(keepKilling) == 0:
			return adaptation, path

		listPath = []
		index = 0
		for i in range(0, len(keepKilling)):
			#newNode = [(pieceLine, pieceCollum)]
			auxBoard = copy.deepcopy(board)
			auxBoard[pieceLine][pieceCollum].makeKill(keepKilling[i], auxBoard)
			aux, path = self.killingQuantity(keepKilling[i][0], keepKilling[i][1], adaptation+2, path, auxBoard)
			listPath.append(copy.copy(path))
			path.pop()	
			if aux > adaptation:
				adaptation = aux
				index = i
		if len(listPath) > 0:
			path = listPath[index]
		return adaptation, path

	#Return the best adaptation and the path of kills
	def kill(self, piecesList, board):
		adaptation = 0
		path = []
		auxBoard = []
		for i in range(0, len(piecesList)):
			newAdaptation, newPath = board[piecesList[i][0]][piecesList[i][1]].adaptKill(board)
			if newAdaptation > adaptation:
				adaptation = newAdaptation
				path = newPath
		return adaptation, path

	#Function that will chose the best movement
	def play(self, sequenceMove, board):
		hasKilled = False
		myPieces = self.findAllBlack(board)
		adapKill, chosedMove = self.kill(myPieces, board)
		print "adaptKill", adapKill
		if adapKill > 0:
			hasKilled = True
		else:
			if not sequenceMove:
				adapMove, chosedMove = self.standartMove(myPieces, board)
				print "adaptMove", adapMove
		return hasKilled, chosedMove
