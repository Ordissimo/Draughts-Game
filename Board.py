# coding=UTF-8
import pygame, sys
from Piece import Piece
from RedPiece import RedPiece
from BlackPiece import BlackPiece
from RedCrownPiece import RedCrownPiece
from BlackCrownPiece import BlackCrownPiece
from NPC import NPC 

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
'''
#Instance my Pieces
red = RedPiece()
black = BlackPiece()
redCrown = RedCrownPiece()
blackCrown = BlackCrownPiece()
'''
#making my matrix's board
board = [[0, BlackPiece(), 0, BlackPiece(), 0, BlackPiece(), 0, BlackPiece()], 
		[BlackPiece(), 0, BlackPiece(), 0, BlackPiece(), 0, BlackPiece(), 0],
		[0, BlackPiece(), 0, BlackPiece(), 0, BlackPiece(), 0, BlackPiece()],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0],
		[RedPiece(), 0, RedPiece(), 0, RedPiece(), 0, RedPiece(), 0],
		[0, RedPiece(), 0, RedPiece(), 0, RedPiece(), 0, RedPiece()],
		[RedPiece(), 0, RedPiece(), 0, RedPiece(), 0, RedPiece(), 0]]

#Set their positions
for i in range(0, 8):
	for j in range(0, 8):
		if board[i][j] != 0:
			board[i][j].setPosition(i, j)

#Variables
line = 0
collum = 0
selected_line = -5
selected_collum = -13
turn = 0
turnNoKill = 0
hasOutline = False
canKillAnother = False
num_black = 12
num_red = 12
npc = NPC()
sequenceKill = False
time = 0
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
				hasKill, path = npc.play(sequenceKill, board)
				#print path
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
					time = 0
					sequenceKill = True
			else:
				time += 1
				if time < len(path):
					#print path[time-1], "gonna eat moving to", path[time]
					board[path[time-1][0]][path[time-1][1]].makeKill(path[time], board)
				else:
					sequenceKill = False
					num_red -= len(path)-1
					turnNoKill = 0
					turn += 1
					crown(board, path[time-1][0], path[time-1][1])
				
		
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

			#If the click was on a piece of it's own turn
			if turn%2 == 0 and isRedTeam(board[line][collum]):
				if not canKillAnother:
					killers = searchKillers(board, line, collum)
					if (line, collum) in killers or len(killers) == 0:
						selected_line = line
						selected_collum = collum
						selected_piece = board[line][collum]
						hasOutline = True
						#get all possible spaces where the piece can walk to
						possible_to_kill = selected_piece.canKill(board)
						possible_to_move = []
						if len(possible_to_kill) == 0:
							possible_to_move = selected_piece.canMove(board)

			#If was clicked in a empty space
			elif board[line][collum] == 0:
				#print "empty space"
				#if something is selected and can go there			
				if hasOutline:

					#See if the destiny is reached by moving 
					if (line, collum) in possible_to_move:
						selected_piece.makeMove((line, collum), board)
						turn +=1
						turnNoKill += 1
						crown(board, line, collum)
					#See if the destiny is reached by eating
					elif (line, collum) in possible_to_kill:
						selected_piece.makeKill((line,collum),board)
						#Counting the number of remanescents pieces
						num_black -= 1
						#print "Vermelhas:", num_red, "Pretas:", num_black

						#Seeing if the piece can kill another one
						possible_to_kill = selected_piece.canKill(board)
						if len(possible_to_kill) != 0:
							selected_line = line
							selected_collum = collum
							canKillAnother = True
						else:
							turn += 1
							turnNoKill = 0
							canKillAnother = False
							crown(board, line, collum)

					#For print the current turn
					text = "Turn " + str(turn+1) 
					turnText = myFont.render(text, 1, WHITE_COLOR)
				
				#remove the outline mark
				if not canKillAnother:
					hasOutline = False
	
	
	#Draw the actual state			
	screen.fill(BLACK_COLOR)
	screen.blit(Im_background, Im_background_rect)
	screen.blit(turnText, (5, WINDOW_HEIGHT - 36))
	screen.blit(Im_board, (75, 75))

	#Draw the outline if someone is selected
	if(hasOutline):
		screen.blit(Im_outline_selected, (80+(selected_collum*42), 80+(selected_line*42)))
		if not canKillAnother:
			for i in range(0, len(possible_to_move)):
				screen.blit(Im_outline_possibilities,  (80+(possible_to_move[i][1]*42), 80+(possible_to_move[i][0]*42)))
		for i in range(0, len(possible_to_kill)):
			screen.blit(Im_outline_possibilities,  (80+(possible_to_kill[i][1]*42), 80+(possible_to_kill[i][0]*42)))

	#Draw my board on the screen
	for i in range(0, 8):
		for j in range(0, 8):
			if board[i][j] != 0:
				board[i][j].draw(screen)

	#Update the screen
	pygame.display.flip()