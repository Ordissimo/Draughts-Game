from Piece import Piece
from Player import Player
from Piece import Piece
from SimplePiece import SimplePiece
from CrownPiece import CrownPiece
from State import State
from Tree import Tree, Node
import random	
import copy

class NPC(Player):
	# Constructor
	def __init__(self, board, piecesVector):
		super(NPC, self).__init__(board, piecesVector)
		# Find and load the database.
		self.db = open("database.txt", "r")  
		self.dbContent = self.db.readlines()
		self.gameStates = []
		self.db.close()
		
		self.dbMatrix = []
		self.dbMatrix.append([])
		#print "lengh db content: " + str(len(self.dbContent))
		i = 0
		while(i < len(self.dbContent)):
			if self.dbContent[i] != "\n":
				state = self.dbContent[i]
				movement = self.dbContent[i+1]
				winner = int(self.dbContent[i+2])
				newState = State(state, movement, winner)
				self.dbMatrix[ len(self.dbMatrix)-1 ].append(newState)
				i += 3
			else:
				self.dbMatrix.append([])
				i += 1
				
		

	# Choose the next movement
	def standartMove(self, piecesList, board):
		adaptation = -100
		movement = [(-10, -10), (-10,-10)]
		for i in range (0, len(piecesList)):
			newAdaptation, newMovement = self.board[piecesList[i].line][piecesList[i].collum].adaptAdvance(self.board)
			if newAdaptation > adaptation:
				adaptation = newAdaptation
				movement = newMovement
		return adaptation, movement

	# Return the best adaptation and the path of kills
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

	# Override
	# Function that will chose the best movement
	def play(self, currentState, board):
		
		# Get all the states that match with the current one
		foundedStates = self.searchCurrentState(currentState + "\n")
		print ""
		print "Founded Identical States: " + str( len( foundedStates ) )
		
		hasKilled = False
		chosedMove = []
		
		if len( foundedStates ) > 0:
			for s in foundedStates:
				
				print "\nState: " + s.state + "movement: " + s.movement + "winner: " + str(s.winner)
				
				# If the winner was the npc
				if s.winner == 1:
					# Get the origin and destination positions
					pieceLine = int( s.movement[0] )
					pieceCollum = int( s.movement[1] )
					
					destLine = int( s.movement[2] )
					destCollum = int ( s.movement[3] )

					# Get all moves possible for that piece
					tempBoard = copy.deepcopy( self.board )
					canMoveTo = self.GetTreeOfMoves( tempBoard[ pieceLine ][ pieceCollum ], tempBoard )
					
					if len( canMoveTo.root.child ) == 0:
						canMoveTo = self.board[pieceLine][pieceCollum].canMove( self.board )
					print "have to find a path to " + str( s.movement )
					
					# Choose the best path
					if isinstance(canMoveTo, Tree):
						print "killing"
						chosedMove = canMoveTo.getPath( (destLine, destCollum) )
						hasKilled = True
						print path
					else:
						chosedMove = [ (pieceLine, pieceCollum), (destLine, destCollum) ]
						hasKilled = False
						print "can't eat"

					print ("chosed move: %s") % ( str( chosedMove ) )
					return hasKilled, chosedMove

		# If couldn't find identical state OR one that could win
		killing = []
		# Get all killing moves
		tempBoard = copy.deepcopy( self.board )
		for p in self.piecesVector:
			t = self.GetTreeOfMoves( tempBoard[ p.line ][ p.collum ], tempBoard )
			if len( t.root.child ) > 0:
				killing.append( t )
				t.printTree()

		moving = []
		# If cannot kill
		if len( killing ) == 0:
			# Get all possible moves
			for p in self.piecesVector:
				for m in p.canMove( self.board ):
					moving.append(  [ (p.line, p.collum), m] )

		# Choose wich move take
		if len( killing ) > 0:
			print "random killing"
			randIndex = random.randint( 0, len(killing)-1 )
			chosedMove = killing [ randIndex ].getRandomPath()
			hasKilled = True
		elif len( moving ) > 0:
			print "random moving"
			randIndex = random.randint( 0, len(moving)-1 )
			chosedMove = moving [ randIndex ]
			hasKilled = False
		else:
			print "No possible Move"
			chosedMove = []
			hasKilled = False
			
		print "Random Move: " + str( chosedMove )

		'''
		hasKilled = False
		adapKill, chosedMove = self.kill(self.piecesVector, board)
		if adapKill > 0:
			hasKilled = True
		else:
			adapMove, chosedMove = self.standartMove(self.piecesVector, board)
			if adapMove == -100:
				return False, []
		'''

		
		if len(chosedMove) > 0:
			# Get only the first and last position
			movement = str(chosedMove[0][0]) + str(chosedMove[0][1]) + \
				str(chosedMove[-1][0]) + str(chosedMove[-1][1])
			#print movement
			
			# Save state
			self.gameStates.append( State(currentState, movement) )
			#print ("recording %d  |  movement = %s" ) % (len(self.gameStates), str(chosedMove))
		
		return hasKilled, chosedMove

	# Return the last 3 times that the currentState appears 
	def searchCurrentState(self, currentState):
		recentAppear = []
		count = 0
		for game in self.dbMatrix:
			for move in game:
				#print len(move.state)
				if currentState == move.state:
					if len(recentAppear) < 3:
						recentAppear.append(move)
			
			if len(recentAppear) >= 3:
				break

		return recentAppear

	# Get all path of kills that a piece can make
	def GetTreeOfMoves ( self, piece, board ) :
		
		# Create the tree and the root
		tree = Tree()
		tree.addRoot( ( piece.line, piece.collum ) )
		children = piece.canKill( board )
		for c in children:
			tree.root.addChild( c )

		# Create the childs
		if len( tree.root.child ) > 0:
			self.GenerateTree( tree.root, board )

		return tree

	# Assist the GetTreeOfMoves. Recursive Function.
	def GenerateTree ( self, node, board ):

		for n in node.child :

			# Delete the piece killed 
			orientationX = ( n.value[0] - node.value[0] ) / 2
			orientationY = ( n.value[1] - node.value[1] ) / 2
			t = board [ node.value[0] + orientationX ] [ node.value[1] + orientationY ] 
			board [ node.value[0] + orientationX ] [ node.value[1] + orientationY ] = None

			# Create a Piece in the next position of the node 
			imaginaryPiece = SimplePiece ( None, 1, "black" )
			imaginaryPiece.setPosition( n.value[0], n.value[1] )
			children = imaginaryPiece.canKill( board )

			#if len(children) > 0:
			#	print "  parent: " + str( n.value ) + " children: " + str( children )

			# Add the children
			for c in children:
				n.addChild( c )

			# Recursive behavior
			for c in node.child:
				self.GenerateTree( c, board )

			# Reedo the board
			board [ node.value[0] + orientationX ] [ node.value[1] + orientationY ] = t
		
	'''
	# Return the number of differences between 2 strings
	def compareStrings(self, str1, str2):
		differenceCount = 0
		#print ("COMPARE\n  %s\n and\n  %s\n") % (str1, str2)
		for i in range(0, len(str1)):
			if str1[i] != str2[i]:
				differenceCount += 1
		differenceCount += len(str1) - len(str2)
		return differenceCount
	'''
	# Close the database and record the new data
	def close(self, winner):
		if winner == 1:
			print "Recording the game, Npc wins!"
		elif winner == 2:
			print "Recording the game, User wins!"
		else:
			"No one Wins, shoudn't be recording"

		# Set the result of the game
		for i in range( 0, len(self.gameStates)):  
			self.gameStates[i].winner = winner

		# Saving this game in the database.
		self.db = open ("database.txt", "w")
		content = []
		for s in self.gameStates:
			content.append(s.state + "\n")
			content.append(str(s.movement) + "\n")
			content.append(str(s.winner) + "\n")
		content.append("\n")
		self.db.writelines(content + self.dbContent)
		self.db.close()

