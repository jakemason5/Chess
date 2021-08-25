

import pygame as p
from Chess import ChessEngine, ChessAI

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
    """
    ----------------------------------------------------------------------------
    """
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT)) #setting the area for the pygame screen
    clock = p.time.Clock() #creating clock for runtime
    screen.fill(p.Color("white")) #setting background for the screen

    """
       ----------------------------------------------------------------------------
    """
    gs = ChessEngine.GameState() #making instance of the game state
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    animate = False #flag variable for when a move should be animated
    loadImages()
    running = True
    sqSelected = () #no square is selected initially, keeps track of user click
    playerClicks = [] #keeps track of player clicks

    """
       ----------------------------------------------------------------------------
    """
    gameOver = False
    playerOne = True #if a human is playing white
    playerTwo = True #if a human is playing black




    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)


        for e in p.event.get(): #creating event watcher to check for closing
            if e.type == p.QUIT:
                running = False


            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN: #watching mouse button to get user input for game
                if not gameOver and humanTurn:
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
                        if move in validMoves:
                            gs.makeMove(move) #changes the board for the game state
                            moveMade = True
                            animate = True
                        sqSelected = () #clears the selected position
                        playerClicks = [] #clears the selected spots



            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r: #reset the board when r is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False



        #Ai move finder logic
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True



        if moveMade:
            if animate:
                animatedMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False


        drawGameState(screen, gs, validMoves, sqSelected) #draws the board based on the 2d array



        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')

        clock.tick(MAX_FPS) #running to update the display
        p.display.flip()



'''
Highlight the piece and possible moves
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))




"""
function to draw the board based on the 2d array in its current state
"""
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)



"""
Will draw the squares of the board
"""
def drawBoard(screen):
    global colors
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



'''
Animating a new move
'''
def animatedMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2] #getting piece color
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE) #creating rectangle
        p.draw.rect(screen, color, endSquare) #covering picture of piece in new location
        #drawing captured piece over cover in end location
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)

        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)



'''
Drawing the text at the end of a game
'''
def drawText(screen, text):
    font = p.font.SysFont('Helvitca', 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    #centering the text on the board
    textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)




if __name__ == "__main__":
    main()
