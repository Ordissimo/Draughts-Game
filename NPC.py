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
		biggerAdaptation = 0
		bestMove = [(-1, -1), (-1,-1)]
		for i in range (0, len(piecesList)):
			moves = board[ piecesList[i][0] ][ piecesList[i][1] ].canMove(board)
			for j in range(0, len(moves)):
				if self.valueBoard[moves[j][0]][moves[j][1]] > biggerAdaptation:
					biggerAdaptation = self.valueBoard[moves[j][0]][moves[j][1]]
					#print biggerAdaptation
					bestMove = [piecesList[i], moves[j]]
		return bestMove

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
		killers = self.searchKillers(piecesList, board)
		adaptation = 0
		path = []
		auxBoard = []
		for i in range(0, len(killers)):
			newAdaptation, newPath = self.killingQuantity(killers[i][0], killers[i][1], 0, [], copy.deepcopy(board))
			print "peca na", killers[i][0], killers[i][1], "->", newAdaptation, newPath
			if newAdaptation > adaptation:
				adaptation = newAdaptation
				path = newPath
		return adaptation, path

	def play(self, sequenceMove, board):
		hasKilled = False
		myPieces = self.findAllBlack(board)
		adapKill, chosedMove = self.kill(myPieces, board)
		if adapKill > 0:
			hasKilled = True
		else:
			if not sequenceMove:
				chosedMove = self.standartMove(myPieces, board)
		return hasKilled, chosedMove
