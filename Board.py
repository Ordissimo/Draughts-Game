# coding=UTF-8
import pygame, sys, copy
from Piece import Piece
from NPC import NPC
from User import User
from Player import Player
from SimplePiece import SimplePiece
from CrownPiece import CrownPiece

pygame.init() #Inicialize pygame

#Team constants
BLACK_TEAM = "black"
RED_TEAM = "red"

#Set Constants
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500
BLACK_COLOR = 0, 0, 0
WHITE_COLOR = 255, 255, 255

#Load images
Im_background = pygame.image.load("Images/Madeira.jpg")
Im_background_rect = Im_background.get_rect()
Im_board = pygame.image.load("Images/tabuleiro.jpg")
Im_outline_selected = pygame.image.load("Images/ol.png") #outline = contorno
Im_outline_possibilities = pygame.image.load("Images/ol2.png")
Im_red_Piece = pygame.image.load("Images/Peca_vermelha.png")
Im_black_Piece = pygame.image.load("Images/Peca_preta.png")
Im_black_crown = pygame.image.load("Images/damaNegra.png")
Im_red_crown = pygame.image.load("Images/damaVermelha.png")

#Text label
myFont = pygame.font.SysFont("Comic Sans Ms", 36)
turnText = myFont.render("Turn 1", 1, WHITE_COLOR)
	
#The piece is a red one?
def isRedTeam(somePiece):
	if somePiece != 0 and somePiece.team == RED_TEAM:
		return True
	return False
#The piece is a black one?
def isBlackTeam(somePiece):
	if somePiece != 0 and somePiece.team == BLACK_TEAM:
		return True
	return False

#That piece on the board should be crown?
def crown(board, line, collum):
	if isinstance(board[line][collum], SimplePiece):
		if line == 7 and board[line][collum].team == BLACK_TEAM:
			board[line][collum] = CrownPiece(Im_black_crown, BLACK_TEAM)
		elif line == 0 and board[line][collum].team == RED_TEAM:
			board[line][collum] = CrownPiece(Im_red_crown, RED_TEAM)
		board[line][collum].setPosition(line, collum)

#Print the board
def printB(board):
	for i in range(0, 8):
		for j in range(0, 8):
			p = board[i][j]
			if isinstance(p, Piece):
				if isinstance(p, SimplePiece):
					if p.team == RED_TEAM:
						print "r",
					elif p.team == BLACK_TEAM:
						print "b",
				elif isinstance(p, SimplePiece):
					if p.team == RED_TEAM:
						print "R",
					elif p.team == BLACK_TEAM:
						print "B"
			else:
				print p,
		print ""

#Find every piece that can kill
def searchKillers(board, line, collum):
	listKillers = []
	if isRedTeam(board[line][collum]):
		for i in range(0, 8):
			for j in range(0, 8):
				if isRedTeam(board[i][j]):
					targets = board[i][j].canKill(board)
					if len(targets) != 0:
						listKillers.append((i, j))
	if isBlackTeam(board[line][collum]):
		for i in range(0, 8):
			for j in range(0, 8):
				if isBlackTeam(board[i][j]):
					targets = board[i][j].canKill(board)
					if len(targets) != 0:
						listKillers.append((i, j))
	return listKillers




#Opening a window
size = (WINDOW_WIDTH , WINDOW_HEIGHT)
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Draught")

#Instacing all the pieces
blackOnes = []
redOnes = []
for i in range(0, 12):
	blackOnes.append( SimplePiece(Im_black_Piece, 1, BLACK_TEAM) )
	redOnes.append( SimplePiece(Im_red_Piece, -1, RED_TEAM) )


#making my matrix's board
board = [[0, blackOnes[0], 0, blackOnes[1], 0, blackOnes[2], 0, blackOnes[3]], 
		[blackOnes[4], 0, blackOnes[5], 0, blackOnes[6], 0, blackOnes[7], 0],
		[0, blackOnes[8], 0, blackOnes[9], 0, blackOnes[10], 0, blackOnes[11]],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[redOnes[0], 0, redOnes[1], 0, redOnes[2], 0, redOnes[3], 0],
		[0, redOnes[4], 0, redOnes[5], 0, redOnes[6], 0, redOnes[7]],
		[redOnes[8], 0, redOnes[9], 0, redOnes[10], 0, redOnes[11], 0]]

#Set their positions
for i in range(0, 8):
	for j in range(0, 8):
		if board[i][j] != 0:
			board[i][j].setPosition(i, j)

#Making players
npc = NPC(board, blackOnes)
user = User(board, redOnes)

#Variables
turn = 0
turnNoKill = 0
num_black = 12
num_red = 12
sequenceKill = False
countKills = 0

#Game loop
while 1:
		
	#Get any user's event
	for event in pygame.event.get(): 
		#Exit if the 'X' button is clicked
		if event.type == pygame.QUIT:
			sys.exit()

		#Winner's conditions
		if num_red == 0:
			turnText = turnText = myFont.render("Player BLACK wins!!!", 1, BLACK_COLOR)
			break
		elif num_black == 0:
			turnText = turnText = myFont.render("Player RED wins!!!", 1, (255, 0, 0))
			break
		elif turnNoKill >= 20:
			turnText = turnText = myFont.render("We have a Draw...", 1, (150, 150, 150))
			break

		#NPC's time to play
		if turn%2 == 1:
			if not sequenceKill:
				countKills = 0
				hasKill, path = npc.play(sequenceKill, board)

				#If hasn't any move to do
				if path[0] == (-10,-10):
					num_black = 0
					break

				if not hasKill:
					if len(path) > 0:
						board[path[0][0]][path[0][1]].makeMove(path[1], board)
						turnNoKill +=1
						#print "move", path[0], "to", path[1]
					turn += 1
					sequenceKill = False
					crown(board, path[1][0], path[1][1])
				else:
					pygame.time.wait(1000) #wait 1 sec
					sequenceKill = True
			else:
				#print path
				countKills += 1
				if countKills < len(path):
					board[path[countKills-1][0]][path[countKills-1][1]].makeKill(path[countKills], board)
				else:
					sequenceKill = False
					num_red -= len(path)-1
					turnNoKill = 0
					turn += 1
					crown(board, path[countKills-1][0], path[countKills-1][1])
				
		
		#When click
		if event.type == pygame.MOUSEBUTTONDOWN: 
			#Get board position of the click
			x, y = event.pos
			collum = int(round((x-80)/42))
			line = int(round((y-80)/42))
			#print turnNoKill
			#If the click was out of the board
			if collum < 0 or collum >= 8 or line < 0 or line >= 8:
				print "out of range"
				break;

			#It's player time
			if turn%2 == 0:
				#clicked on his own piece
				if isRedTeam(board[line][collum]) and not sequenceKill:
					user.setSelected(line, collum)
				#clicked on a empty space
				elif board[line][collum] == 0:
					#Take the current moves to kill
					if user.selected != None:
						pastMovesToKill = copy.copy(user.movesOfSelectedToKill)
					#See if it's a movement spot
					if user.tryPlay(line, collum):
						turn += 1
						sequenceKill = False
						crown(board, line, collum)
						if (line,collum) in pastMovesToKill:
							turnNoKill = 0
							num_black -=1
						else:
							turnNoKill += 1
							user.deselect()
					#See if the player can kill another piece
					if user.selected != None and len(user.selected.canKill(board)) > 0:
						user.setSelected(user.selected.line, user.selected.collum)
						sequenceKill = True
						turnNoKill = 0
						num_black -= 1
					else:	
						user.deselect()

					#For print the current turn
					text = "Turn " + str(turn+1) 
					turnText = myFont.render(text, 1, WHITE_COLOR)
	
	#Draw the actual state			
	screen.fill(BLACK_COLOR)
	screen.blit(Im_background, Im_background_rect)
	screen.blit(turnText, (5, WINDOW_HEIGHT - 36))
	screen.blit(Im_board, (75, 75))

	#Draw the outline if someone is selected
	if user.selected != None:
		screen.blit(Im_outline_selected, (80+(user.selected.collum*42), 80+(user.selected.line*42)))
		for i in range(0, len(user.movesOfSelectedToWalk)):
			screen.blit(Im_outline_possibilities, (80+(user.movesOfSelectedToWalk[i][1]*42), 80+(user.movesOfSelectedToWalk[i][0]*42)))
		for i in range(0, len(user.movesOfSelectedToKill)):
			screen.blit(Im_outline_possibilities,  (80+(user.movesOfSelectedToKill[i][1]*42), 80+(user.movesOfSelectedToKill[i][0]*42)))

	#Draw my board on the screen
	for i in range(0, 8):
		for j in range(0, 8):
			if board[i][j] != 0:
				board[i][j].draw(screen)

	#Update the screen
	pygame.display.flip()