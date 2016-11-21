from Piece import Piece
from Player import Player
import copy

class NPC(Player):
	#Constructor
	def __init__(self, board, piecesVector):
		super(NPC, self).__init__(board, piecesVector)
		'''
			2. Find and load the database.
		'''

	#Choose the next movement
	def standartMove(self, piecesList, board):
		adaptation = -100
		movement = [(-10, -10), (-10,-10)]
		for i in range (0, len(piecesList)):
			newAdaptation, newMovement = self.board[piecesList[i].line][piecesList[i].collum].adaptAdvance(self.board)
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
			newAdaptation, newPath = self.board[piecesList[i].line][piecesList[i].collum].adaptKill(self.piecesVector, board)
			'''
				4. Describe the algorithm and use it.
			'''
			if newAdaptation > adaptation:
				adaptation = newAdaptation
				path = newPath
		return adaptation, path

	#Override
	#Function that will chose the best movement
	def play(self, board):
		hasKilled = False
		adapKill, chosedMove = self.kill(self.piecesVector, board)
		if adapKill > 0:
			hasKilled = True
		else:
			adapMove, chosedMove = self.standartMove(self.piecesVector, board)
			if adapMove == -100:
				return False, [(-10, -10)]

		'''
			3. Save counter-attack eficience.
		'''
		return hasKilled, chosedMove
