from Piece import Piece
import copy

class NPC:
	#Constructor
	def __init__(self, board):
		self.board = board

	#Return every piece of the black team on the board
	def findAllBlack(self):
		blackPositions = []
		for i in range(0, 8):
			for j in range(0, 8):
				if self.board[i][j] != 0 and self.board[i][j].team == "black":
					blackPositions.append((i, j))
		return blackPositions

	#Choose the next movement
	def standartMove(self, piecesList, board):
		adaptation = 0
		movement = [(-10, -10), (-10,-10)]
		for i in range (0, len(piecesList)):
			newAdaptation, newMovement = self.board[piecesList[i][0]][piecesList[i][1]].adaptAdvance(self.board)
			if newAdaptation > adaptation:
				adaptation = newAdaptation
				movement = newMovement
		return adaptation, movement

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
		myPieces = self.findAllBlack()
		if len(myPieces) == 0:
			return False, [(-10, -10)]
		adapKill, chosedMove = self.kill(myPieces, board)
		if adapKill > 0:
			hasKilled = True
		else:
			if not sequenceMove:
				adapMove, chosedMove = self.standartMove(myPieces, board)
				if adapMove == 0:
					return False, [(-10, -10)]
		return hasKilled, chosedMove
