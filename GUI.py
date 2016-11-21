# coding=UTF-8
import pygame, sys, copy
from Board import Board

#Draw my board on the screen
def drawPieces():	
	for i in range(0, 8):
		for j in range(0, 8):
			if gameBoard.board[i][j] != 0:
				gameBoard.board[i][j].draw(screen)

#Draw the outline if someone is selected
def drawOutline():
	if gameBoard.user.selected != None:
		screen.blit(Im_outline_selected, (80+(gameBoard.user.selected.collum*42), 80+(gameBoard.user.selected.line*42)))
		for i in range(0, len(gameBoard.user.movesOfSelectedToWalk)):
			screen.blit(Im_outline_possibilities, (80+(gameBoard.user.movesOfSelectedToWalk[i][1]*42), 
				80+(gameBoard.user.movesOfSelectedToWalk[i][0]*42)))
		for i in range(0, len(gameBoard.user.movesOfSelectedToKill)):
			screen.blit(Im_outline_possibilities,  (80+(gameBoard.user.movesOfSelectedToKill[i][1]*42), 
				80+(gameBoard.user.movesOfSelectedToKill[i][0]*42)))

#Draw the game background	
def drawBoard():			
	screen.fill(BLACK_COLOR)
	screen.blit(Im_background, Im_background_rect)
	screen.blit(turnText, (5, WINDOW_HEIGHT - 36))
	screen.blit(winText, (150, WINDOW_HEIGHT - 36))
	screen.blit(Im_board, (75, 75))

pygame.init() #Inicialize pygame

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
Im_red_piece = pygame.image.load("Images/Peca_vermelha.png")
Im_black_piece = pygame.image.load("Images/Peca_preta.png")
Im_black_crown = pygame.image.load("Images/damaNegra.png")
Im_red_crown = pygame.image.load("Images/damaVermelha.png")

#Text label
myFont = pygame.font.SysFont("Comic Sans Ms", 36)
turnText = myFont.render("", 1, WHITE_COLOR)
winText = myFont.render("", 1, WHITE_COLOR)

#Opening a window
size = (WINDOW_WIDTH , WINDOW_HEIGHT)
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Draught")

#Setting the game
gameBoard = Board(Im_black_piece, Im_black_crown, Im_red_piece, Im_red_crown)
gameBoard.resetBoard()

#Game loop
while 1:
		
	#Get any user's event
	for event in pygame.event.get(): 
		#Exit if the 'X' button is clicked
		if event.type == pygame.QUIT:
			sys.exit()

		#See if someone win
		if gameBoard.winConditions() > 0:
			if gameBoard.winConditions() == 1:
				winText = myFont.render("Player BLACK wins!!!", 1, BLACK_COLOR)
			elif gameBoard.winConditions() == 2:
				winText = myFont.render("Player RED wins!!!", 1, (255, 0, 0))
			else:
				winText = myFont.render("We have a Draw...", 1, (150, 150, 150))

		#NPC's time to play
		if gameBoard.turn % 2 == 0:
			gameBoard.NPCTime()
				
		#When click
		if event.type == pygame.MOUSEBUTTONDOWN: 
			#Get board position of the click
			x, y = event.pos
			collum = int(round((x-80)/42))
			line = int(round((y-80)/42))

			#If the click was out of the board
			if collum < 0 or collum >= 8 or line < 0 or line >= 8:
				print "out of range"
				break;

			#It's user time
			if gameBoard.turn%2 == 1:
				gameBoard.playerTime(line, collum)
		
	#Drawing
	text = "Turn " + str(gameBoard.turn) 
	turnText = myFont.render(text, 1, WHITE_COLOR) #For print the current turn
	drawBoard();
	drawOutline()
	drawPieces();

	#Update the screen
	pygame.display.flip()