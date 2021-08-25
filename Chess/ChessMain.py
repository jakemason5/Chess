

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations
IMAGES = {}

'''
Initialize a global dictionary of images
'''

def loadImages():
    pieces = ['wp', "wR", "wN", "wB", "wQ", "wK", "bR", "bN", "bB", "bQ", "bK", "bp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #now can access an image using IMAGES['piece']

"""
Main driver for code
"""
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT)) #setting the area for the pygame screen
    clock = p.time.Clock() #creating clock for runtime
    screen.fill(p.Color("white")) #setting background for the screen
    gs = ChessEngine.GameState() #making instance of the game state
    loadImages()
    running = True
    sqSelected = () #no square is selected initially, keeps track of user click
    playerClicks = [] #keeps track of player clicks
    while running:
        for e in p.event.get(): #creating event watcher to check for closing
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN: #watching mouse button to get user input for game
                location = p.mouse.get_pos() # get x and y pos of the mouse
                col = location[0]//SQ_SIZE #getting the location of the mouse click x position within the board
                row = location[1]//SQ_SIZE #getting location of mouse click y position
                if sqSelected == (row, col): #check if user selected square twice
                    sqSelected = () #deselct board position
                else:
                    sqSelected = (row, col) #set the selected board position
                    playerClicks.append(sqSelected) #add the selection to the number of positions clicked
                if len(playerClicks) == 2: #when player has selected starting and ending point
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board) #move piece from starting position to ending position
                    print(move.getChessNotation()) #prints out chess notation for move
                    gs.makeMove(move) #changes the board for the game state
                    sqSelected = () #clears the selected position
                    playerClicks = [] #clears the selected spots

            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()

        drawGameState(screen, gs) #draws the board based on the 2d array
        clock.tick(MAX_FPS) #running to update the display
        p.display.flip()

"""
function to draw the board based on the 2d array in its current state
"""
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

"""
Will draw the squares of the board
"""
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Will Draw the pieces on the board using the game state
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
