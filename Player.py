from abc import ABCMeta, abstractmethod

class Player:

	__metaclass__ = ABCMeta

	#Constructor
	def __init__(self, board, piecesVector):
		self.board = board
		self.piecesVector = piecesVector;


	@abstractmethod
	def play(self):
		pass