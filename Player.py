from abc import ABCMeta, abstractmethod
from Piece import Piece

class Player:

	__metaclass__ = ABCMeta

	#Constructor
	def __init__(self, board, piecesVector):
		self.board = board
		self.piecesVector = piecesVector;

	#find the position of a Piece in a array of pieces
	def findPiece(self, line , collum):
		for i in range(0, len(self.piecesVector)):
			if isinstance(self.piecesVector[i], Piece):
				if self.piecesVector[i].line == line and self.piecesVector[i].collum:
					return i
		return -1


	@abstractmethod
	def play(self):
		pass