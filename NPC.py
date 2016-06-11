from Piece import Piece
import copy

def printB(board):
	for i in range(0, 8):
		for j in range(0, 8):
			p = board[i][j]
			if isinstance(p, Piece):

				if p.kind == "simple" and p.team == "red":
					print "r",
				elif p.kind == "simple" and p.team == "black":
					print "b",
				elif p.kind == "crown" and p.team == "red":
					print "R",
				elif p.kind == "crown" and p.team == "black":
					print "B",
			else:
				print p,
		print ""



class NPC:
	def __init__(self):
		self.valueBoard = [[4, 4, 4, 4, 4, 4, 4, 4],
						[4, 3, 3, 3, 3, 3, 3, 4],
						[4, 3, 2, 2, 2, 2, 3, 4],
						[4, 3, 2, 1, 1, 2, 3, 4],
						[4, 3, 2, 1, 1, 2, 3, 4],
						[4, 3, 2, 2, 2, 2, 3, 4],
						[4, 3, 3, 3, 3, 3, 3, 4],
						[4, 4, 4, 4, 4, 4, 4, 4]]

	def findAllBlack(self, board):
		blackPositions = []

		for i in range(0, 8):
			for j in range(0, 8):
				if board[i][j] != 0 and board[i][j].team == "black":
					blackPositions.append((i, j))
		return blackPositions

	def searchKillers(self, list, board):
		listKillers = []
		for i in range(0, len(list)):
			line = list[i][0]
			collum = list[i][1]
			targets = board[line][collum].canEat(line, collum, board)
			if len(targets) != 0:
				listKillers.append(list[i])
		return listKillers

	def Eat(self, origin, destiny, board):
		board[origin[0]][origin[1]].makeMove(origin, destiny, board)
		difLine = (destiny[0] - origin[0])
		difCollum = (destiny[1] - origin[1])
		#A simple piece will be killed
		if board[destiny[0]][destiny[1]].kind == "simple":
			enemyLine = origin[0] + (difLine/2)
			enemyCollum = origin[1] + (difCollum/2)
			#print enemyLine, enemyCollum
			board[enemyLine][enemyCollum] = 0
			
		#A crown piece will be killed
		else:
			difLine = difLine/abs(difLine) 
			difCollum = difCollum/abs(difCollum)
			enemyLine = origin[0]
			enemyCollum = origin[1]
			crescent = 1
			if origin[0] > destiny[0]:
				crescent = -1
				for i in range(origin[0], destiny[0], crescent):
					enemyLine += difLine
					enemyCollum += difCollum
					#print "enemy:", enemyLine, enemyCollum
					if board[enemyLine][enemyCollum] != 0:
						board[enemyLine][enemyCollum] = 0

	def standartMove(self, piecesList, board):
		biggerAdaptation = 0
		bestMove = [(-1, -1), (-1,-1)]
		for i in range (0, len(piecesList)):
			moves = board[ piecesList[i][0] ][ piecesList[i][1] ].canMove(piecesList[i][0], piecesList[i][1], board)
			for j in range(0, len(moves)):
				if self.valueBoard[moves[j][0]][moves[j][1]] > biggerAdaptation:
					biggerAdaptation = self.valueBoard[moves[j][0]][moves[j][1]]
					#print biggerAdaptation
					bestMove = [piecesList[i], moves[j]]
		return bestMove

	def killingQuantity(self, pieceLine, pieceCollum, adaptation, path, auxBoard):
		keepKilling = auxBoard[pieceLine][pieceCollum].canEat(pieceLine, pieceCollum, auxBoard)
		path.append((pieceLine, pieceCollum))
		#print adaptation
		#print "kp", keepKilling
		if len(keepKilling) != 0:
			for i in range(0, len(keepKilling)):
				self.Eat((pieceLine, pieceCollum), keepKilling[i], auxBoard)
				aux, finalPoint = self.killingQuantity(keepKilling[i][0], keepKilling[i][1], adaptation+2, path, auxBoard)
				if aux > adaptation:
					adaptation = aux
		else:
			finalPoint = path

		return adaptation, finalPoint

	def kill(self, piecesList, board):
		killers = self.searchKillers(piecesList, board)
		adaptation = 0
		path = []
		auxBoard = []
		for i in range(0, len(killers)):
			
			newAdaptation, newPath = self.killingQuantity(killers[i][0], killers[i][1], 0, [], copy.deepcopy(board))
			#print "peca na", killers[i][0], killers[i][1], "->", newAdaptation, newPath
			if newAdaptation > adaptation:
				adaptation = newAdaptation
				path = newPath
		return adaptation, path





	def play(self, sequenceMove, board):
		hasKilled = False
		myPieces = self.findAllBlack(board)
		adapKill, chosedMove = self.kill(myPieces, board)
		print sequenceMove
		if adapKill > 0:
			#self.Eat(chosedMove[0], chosedMove[1], board)
			hasKilled = True
		else:
			if not sequenceMove:
				chosedMove = self.standartMove(myPieces, board)
				#board[chosedMove[1][0]][chosedMove[1][1]] = board[chosedMove[0][0]][chosedMove[0][1]]
				#board[chosedMove[0][0]][chosedMove[0][1]] = 0

		return hasKilled, chosedMove



