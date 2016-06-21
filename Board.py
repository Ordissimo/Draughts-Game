# coding=UTF-8
import pygame, sys, copy
from Piece import Piece
from RedPiece import RedPiece
from BlackPiece import BlackPiece
from RedCrownPiece import RedCrownPiece
from BlackCrownPiece import BlackCrownPiece
from NPC import NPC 
from Player import Player

pygame.init() #Inicialize pygame

#The piece is a red one?
def isRedTeam(somePiece):
	if somePiece != 0 and somePiece.team == "red":
		return True
	return False
#The piece is a black one?
def isBlackTeam(somePiece):
	if somePiece != 0 and somePiece.team == "black":
		return True
	return False

#That piece on the board should be crown?
def crown(board, line, collum):
	if line == 7 and isinstance(board[line][collum], BlackPiece):
		board[line][collum] = BlackCrownPiece()
	elif line == 0 and isinstance(board[line][collum], RedPiece):
		board[line][collum] = RedCrownPiece()
	board[line][collum].setPosition(line, collum)

#Print the board
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

#Set Constants
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 500
BLACK_COLOR = 0, 0, 0
WHITE_COLOR = 255, 255, 255

#Opening a window
size = (WINDOW_WIDTH , WINDOW_HEIGHT)
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Draught")

#Load images
Im_background = pygame.image.load("Images/Madeira.jpg")
Im_background_rect = Im_background.get_rect()
Im_board = pygame.image.load("Images/tabuleiro.jpg")
Im_outline_selected = pygame.image.load("Images/ol.png") #outline = contorno
Im_outline_possibilities = pygame.image.load("Images/ol2.png")

#Text label
myFont = pygame.font.SysFont("Comic Sans Ms", 36)
turnText = myFont.render("Turn 1", 1, WHITE_COLOR)

#making my matrix's board
board = [[0, BlackPiece(), 0, BlackPiece(), 0, 0, 0, BlackPiece()], 
		[BlackPiece(), 0, 0, 0, BlackPiece(), 0, BlackPiece(), 0],
		[0, 0, 0, 0, 0, BlackPiece(), 0, 0],
		[0, 0, BlackPiece(), 0, 0, 0, 0, 0],
		[0, RedPiece(), 0, 0, 0, 0, 0, 0],
		[RedPiece(), 0, RedPiece(), 0, RedPiece(), 0, RedPiece(), 0],
		[0, RedPiece(), 0, RedPiece(), 0, RedPiece(), 0, RedPiece()],
		[RedPiece(), 0, RedPiece(), 0, RedPiece(), 0, RedPiece(), 0]]

#Set their positions
for i in range(0, 8):
	for j in range(0, 8):
		if board[i][j] != 0:
			board[i][j].setPosition(i, j)

#Making players
npc = NPC(board)
player = Player(board)

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
			print "nokill =", turnNoKill
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
					player.setSelected(line, collum)
				#clicked on a empty space
				elif board[line][collum] == 0:
					#Take the current moves to kill
					if player.selected != None:
						pastMovesToKill = copy.copy(player.movesOfSelectedToKill)
					#See if it's a movement spot
					if player.tryPlay(line, collum):
						turn += 1
						sequenceKill = False
						crown(board, line, collum)
						if (line,collum) in pastMovesToKill:
							turnNoKill = 0
						else:
							turnNoKill += 1
							player.deselect()
					#See if the player can kill another piece
					if player.selected != None and len(player.selected.canKill(board)) > 0:
						player.setSelected(player.selected.line, player.selected.collum)
						sequenceKill = True
						turnNoKill = 0
					else:	
						player.deselect()

					#For print the current turn
					text = "Turn " + str(turn+1) 
					turnText = myFont.render(text, 1, WHITE_COLOR)
	
	#Draw the actual state			
	screen.fill(BLACK_COLOR)
	screen.blit(Im_background, Im_background_rect)
	screen.blit(turnText, (5, WINDOW_HEIGHT - 36))
	screen.blit(Im_board, (75, 75))

	#Draw the outline if someone is selected
	if player.selected != None:
		screen.blit(Im_outline_selected, (80+(player.selected.collum*42), 80+(player.selected.line*42)))
		for i in range(0, len(player.movesOfSelectedToWalk)):
			screen.blit(Im_outline_possibilities, (80+(player.movesOfSelectedToWalk[i][1]*42), 80+(player.movesOfSelectedToWalk[i][0]*42)))
		for i in range(0, len(player.movesOfSelectedToKill)):
			screen.blit(Im_outline_possibilities,  (80+(player.movesOfSelectedToKill[i][1]*42), 80+(player.movesOfSelectedToKill[i][0]*42)))

	#Draw my board on the screen
	for i in range(0, 8):
		for j in range(0, 8):
			if board[i][j] != 0:
				board[i][j].draw(screen)

	#Update the screen
	pygame.display.flip()