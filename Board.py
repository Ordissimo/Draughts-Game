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
		self.BLACK_TEAM = "black"
		self.RED_TEAM = "red"
		self.board = []
		self.sequenceKill = False

		#Instancing each piece
		self.blackOnes = []
		self.redOnes = []

		#Making players
		self.npc = NPC(self.board, self.blackOnes)
		self.user = User(self.board, self.redOnes)

		self.images = [Im_black_piece, Im_black_crown, Im_red_piece, Im_red_crown]

	#Reset the board to the default state
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

	#Make the npc play
	def NPCTime(self):
		#print ("Size of the lists:\n  black: %d\n  red: %d) % (len(self.blackOnes), len(self.redOnes))
		#get best path and if had some kill;
		hasKill, path = self.npc.play(self.getState(), self.board)

		#If hasn't any move to do
		if path[0] == (-10,-10):
			self.blackOnes = [];
			return;
		
		pygame.time.wait(1000) #wait 1 sec
		#kill and sequence kill.
		if hasKill:
			while len(path) >=2:				
				self.board[path[0][0]][path[0][1]].makeKill(path[1], self.redOnes, self.board)
				del path[0]
			self.turnNoKill = 0
		#moving
		else:
			self.board[path[0][0]][path[0][1]].makeMove(path[1], self.board)
			del path[0]
			self.turnNoKill += 1

		self.turn += 1
		self.crown(path[0][0], path[0][1])

	#Let the user play
	def playerTime(self, clickedLine, clickedCollum):
		#clicked on his own piece
		if self.isRedTeam(self.board[clickedLine][clickedCollum]) and not self.sequenceKill:
			self.user.setSelected(clickedLine, clickedCollum)
		#clicked on a empty space
		elif self.board[clickedLine][clickedCollum] == 0 and self.user.selected != None:

			#See if the selected destination is to walk.
			if (clickedLine, clickedCollum) in self.user.movesOfSelectedToWalk:
				self.turnNoKill +=1
			#See if the selected destination is to eat.
			elif (clickedLine, clickedCollum) in self.user.movesOfSelectedToKill:
				self.turnNoKill = 0
			else:
				return;

			self.user.play(clickedLine, clickedCollum, self.blackOnes)
			self.user.setSelected(clickedLine, clickedCollum)
			
			#See if the player can kill another piece
			if len(self.user.movesOfSelectedToKill) > 0 and self.turnNoKill == 0:
				self.sequenceKill = True
			else:
				self.turn += 1
				self.crown(clickedLine, clickedCollum)
				self.sequenceKill = False
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
	def crown(self, line, collum):
		if isinstance(self.board[line][collum], SimplePiece):
			if line == 7 and self.board[line][collum].team == self.BLACK_TEAM:
				index = self.npc.findPiece(line, collum)
				self.blackOnes[index] = CrownPiece(self.images[1], self.BLACK_TEAM)
				self.board[line][collum] = self.blackOnes[index]
				
			elif line == 0 and self.board[line][collum].team == self.RED_TEAM:
				index = self.user.findPiece(line, collum)
				self.redOnes[index] = CrownPiece(self.images[3], self.RED_TEAM)
				self.board[line][collum] = self.redOnes[index]
			self.board[line][collum].setPosition(line, collum)

	#Get the board
	def getState(self):
		state = ""
		for i in range(0, 8):
			for j in range(0, 8):
				p = self.board[i][j]
				if isinstance(p, Piece):
					if isinstance(p, SimplePiece):
						if p.team == self.RED_TEAM:
							state = state + "r "
						elif p.team == self.BLACK_TEAM:
							state = state + "b "
					elif isinstance(p, CrownPiece):
						if p.team == self.RED_TEAM:
							state = state + "R "
						elif p.team == self.BLACK_TEAM:
							state = state + "B "
				else:
					state = state + "# "
		return state
