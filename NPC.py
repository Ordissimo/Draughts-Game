from Piece import Piece
from Player import Player
from Piece import Piece
from SimplePiece import SimplePiece
from CrownPiece import CrownPiece
import copy

class NPC(Player):
	#Constructor
	def __init__(self, board, piecesVector):
		super(NPC, self).__init__(board, piecesVector)
		#Find and load the database.
		self.db = open("database.txt", "r")
		self.dbContent = self.db.readlines()
		self.gameStates = []
		self.recordCount = 0

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
			if newAdaptation > adaptation:
				adaptation = newAdaptation
				path = newPath
		return adaptation, path

	#Override
	#Function that will chose the best movement
	def play(self, currentState, board):
		'''
		4. Describe the algorithm and use it.
			search for every state like the one we are.
				we won most?
				if yes
					select between the ones we win the next step most used
				if not
					choose a new movement to do.
		'''
		self.recordCount += 1
		print "recording " + str(self.recordCount)

		self.gameStates.append(currentState)
		self.searchCurrentState(currentState)

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

	#return the state already apperas at the database with more victories or loses 
	def searchCurrentState(self, currentState):
		for i in range(0, len(self.dbContent)):
			if self.dbContent[i] == "end":
				break
			elif self.dbContent[i] == "\n":
				break

			diff = self.compareStrings(currentState + '\n', self.dbContent[i])
			#if diff == 0:
			#	print "iguais"
			#else:
			#	print "diferentes %d" % diff

	#Return the number of differences between 2 strings
	def compareStrings(self, str1, str2):
		differenceCount = 0
		#print ("COMPARE\n  %s\n and\n  %s\n") % (str1, str2)
		for i in range(0, len(str1)):
			if str1[i] != str2[i]:
				differenceCount += 1
		differenceCount += len(str1) - len(str2)
		return differenceCount

	def close(self, npcWin):
		self.db.close()

		for i in range( 0, len(self.gameStates)):  
			self.gameStates[i] = self.gameStates[i] + str(npcWin) + "\n"
		self.db = open ("database.txt", "w")
		self.gameStates.append("\n")
		self.content = self.gameStates + self.dbContent
		self.db.writelines(self.content)
