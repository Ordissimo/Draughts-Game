from Piece import Piece
from NPC import NPC
from User import User
from Player import Player
from SimplePiece import SimplePiece
from CrownPiece import CrownPiece
import copy, pygame

class Board:
	#Constructor
	def __init__(self, Im_black_piece, Im_black_crown, Im_red_piece, Im_red_crown):
		self.turn = 1
		self.turnNoKill = 0
		self.sequenceKill = False
		self.BLACK_TEAM = "black"
		self.RED_TEAM = "red"
		self.board = []

		#Instancing each piece
		self.blackOnes = []
		self.redOnes = []

		#Making players
		self.npc = NPC(self.board, self.blackOnes)
		self.user = User(self.board, self.redOnes)

		self.images = [Im_black_piece, Im_black_crown, Im_red_piece, Im_red_crown]

		self.path = []

	def getTurn(self):
		return self.turn;

	def resetBoard(self):

		for i in range(0, 12):
			self.blackOnes.append( SimplePiece(self.images[0], 1, self.BLACK_TEAM) )
			self.redOnes.append( SimplePiece(self.images[2], -1, self.RED_TEAM) )
		#making my matrix's board
		self.board = [[0, self.blackOnes[0], 0, self.blackOnes[1], 0, self.blackOnes[2], 0, self.blackOnes[3]], 
					[self.blackOnes[4], 0, self.blackOnes[5], 0, self.blackOnes[6], 0, self.blackOnes[7], 0],
					[0, self.blackOnes[8], 0, self.blackOnes[9], 0, self.blackOnes[10], 0, self.blackOnes[11]],
					[0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0],
					[self.redOnes[0], 0, self.redOnes[1], 0, self.redOnes[2], 0, self.redOnes[3], 0],
					[0, self.redOnes[4], 0, self.redOnes[5], 0, self.redOnes[6], 0, self.redOnes[7]],
					[self.redOnes[8], 0, self.redOnes[9], 0, self.redOnes[10], 0, self.redOnes[11], 0]]

		self.npc.board = self.board
		self.user.board = self.board
		#Set their positions
		for i in range(0, 8):
			for j in range(0, 8):
				if self.board[i][j] != 0:
					self.board[i][j].setPosition(i, j)


	def NPCTime(self):
		#get best path and if had some kill;
		hasKill, self.path = self.npc.play(self.sequenceKill, self.board)

		#If hasn't any move to do
		if self.path[0] == (-10,-10):
			self.blackOnes = [];
			return;
		
		pygame.time.wait(1000) #wait 1 sec
		#kill and sequence kill.
		if hasKill:
			while len(self.path) >=2:				
				self.board[self.path[0][0]][self.path[0][1]].makeKill(self.path[1], self.redOnes, self.board)
				del self.path[0]
			self.turnNoKill = 0
		#moving
		else:
			self.board[self.path[0][0]][self.path[0][1]].makeMove(self.path[1], self.board)
			del self.path[0]
			self.turnNoKill += 1

		self.turn += 1
		self.crown(self.board, self.path[0][0], self.path[0][1])

	def playerTime(self, clickedLine, clickedCollum):
		#clicked on his own piece
		if self.isRedTeam(self.board[clickedLine][clickedCollum]) and not self.sequenceKill:
			self.user.setSelected(clickedLine, clickedCollum)
		#clicked on a empty space
		elif self.board[clickedLine][clickedCollum] == 0:

			#Take the current moves to kill
			if self.user.selected != None:
				pastMovesToKill = copy.copy(self.user.movesOfSelectedToKill)
			#See if it's a movement spot
			if self.user.tryPlay(clickedLine, clickedCollum, self.blackOnes):
				self.turn += 1
				self.sequenceKill = False
				self.crown(self.board, clickedLine, clickedCollum)
				if (clickedLine,clickedCollum) in pastMovesToKill:
					self.turnNoKill = 0
				else:
					self.turnNoKill += 1
					self.user.deselect()
			#See if the player can kill another piece
			if self.user.selected != None and len(self.user.selected.canKill(self.board)) > 0:
				self.user.setSelected(self.user.selected.line, self.user.selected.collum)
				self.sequenceKill = True
				self.turnNoKill = 0
			else:	
				self.user.deselect()

	#Winner's conditions
	def winConditions(self):
		if len(self.redOnes) == 0:
			return 1
		elif len(self.blackOnes) == 0:
			return 2
		elif self.turnNoKill >= 20:
			return 3
		else:
			return 0

	#The piece is a red one?
	def isRedTeam(self, somePiece):
		if somePiece != 0 and somePiece.team == self.RED_TEAM:
			return True
		return False
	#The piece is a black one?
	def isBlackTeam(self, somePiece):
		if somePiece != 0 and somePiece.team == self.BLACK_TEAM:
			return True
		return False

	#That piece on the board should be crown?
	def crown(self, board, line, collum):
		if isinstance(self.board[line][collum], SimplePiece):
			if line == 7 and self.board[line][collum].team == self.BLACK_TEAM:
				self.board[line][collum] = CrownPiece(self.images[1], self.BLACK_TEAM)
			elif line == 0 and self.board[line][collum].team == self.RED_TEAM:
				self.board[line][collum] = CrownPiece(self.images[3], self.RED_TEAM)
			self.board[line][collum].setPosition(line, collum)

	#Print the board
	def printB(self):
		for i in range(0, 8):
			for j in range(0, 8):
				p = self.board[i][j]
				if isinstance(p, Piece):
					if isinstance(p, SimplePiece):
						if p.team == self.RED_TEAM:
							print "r",
						elif p.team == self.BLACK_TEAM:
							print "b",
					elif isinstance(p, SimplePiece):
						if p.team == self.RED_TEAM:
							print "R",
						elif p.team == self.BLACK_TEAM:
							print "B"
				else:
					print p,
			print ""