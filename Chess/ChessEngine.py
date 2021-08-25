"""
This class is used for storing board state and determining valid movies.
"""

class GameState():
    def __init__(self):

        #Board is 8x8 2d list, each element has two characters
        #first char holds the color of the piece
        #second char holds the type of the piece
        #"--" shows empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True #Initializes first player
        self.moveLog = [] #keeps track of moves made
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False




    '''
    Takes a move and executes it, will not work for castling, pawn promotion or en-passant
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--" #replace original position of piece
        self.board[move.endRow][move.endCol] = move.pieceMoved #set new postion to piece moved
        self.moveLog.append(move) #add the move to the move log
        self.whiteToMove = not self.whiteToMove #swap players turn
        #update the kings location
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)


    '''
    Undo the last move of the game
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop() #remove move from move log
            self.board[move.startRow][move.startCol] = move.pieceMoved #replace moved piece
            self.board[move.endRow][move.endCol] = move.pieceCaptured #replace captured space
            self.whiteToMove = not self.whiteToMove  # swap players turn
            self.checkmate = False
            self.stalemate = False
            #update the Kings position
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)


    '''
    Gets all of the valid moves for the current player
    '''
    def getValidMoves(self):

        #generate all valid moves
        moves = self.getAllPossibleMoves()
        #make each move
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])

        # makemove swaps player so swap is needed to check move
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()

        if len(moves) == 0: #either checkmate or stalemate
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False


        return moves #not worrying about checks for now

    '''
    Determine if current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])



    '''
    Determine if the enemy can attack the square r, c
    '''
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove #switch players
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False



    '''
    Checks to make sure player move won't put their king into check
    '''
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)): #number of rows
            for c in range(len(self.board[r])): #number of cols in given row
                turn = self.board[r][c][0] #gets the space of a board and the first char
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]

                    self.moveFunctions[piece](r, c, moves)

        return moves

    '''
    Get all of the pawn moves for the pawn located at row, col and add the moves to the list
    '''
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c] == "--": #checking square in front
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: # captures to left
                if self.board[r-1][c-1][0] == 'b': #enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c-1), self.board))
            if c+1 <= 7: #captures to right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c+1), self.board))

        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c - 1 >= 0:  # captures to left
                if self.board[r+1][c - 1][0] == 'w':  # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c - 1), self.board))
            if c + 1 <= 7:  # captures to right
                if self.board[r+1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))


    '''
    Get all of the rook moves for the rook located at row, col and add the moves to the list
    '''
    def getRookMoves(self, r, c, moves):
        #setting all of the directions that a rook can travel in
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                #iterating through all directions as far as possible
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    '''
    Get all of the knight moves for the knight located at row, col and add the moves to the list
    '''
    def getKnightMoves(self, r, c, moves):
        # every position a knight can move to from their current spot
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    Get all of the bishop moves for the bishop located at row, col and add the moves to the list
    '''
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1)) #all directions bishop can move in
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8): #runs through bishop directions through length of board stopping at piece found
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    '''
    Get all of the queen moves for the queen located at row, col and add the moves to the list
    '''
    def getQueenMoves(self, r, c, moves):
        #Queen has same moveset as rook and bishop combined
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)


    '''
    Get all of the king moves for the king located at row, col and add the moves to the list
    '''
    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, 1), (1, -1)) #all possible moves for kign
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))




class Move():

     #maps keys to values
     # key : value
     #Can be used to show chess moves on the board eg f8 to e7
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}



    def __init__(self,startSq, endSq, board):
        #designating parts of tuple for easier access later
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        #setting information for pieces moved and captured
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        # gives each potential move on the board a custom id
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol




    '''
    Ovverriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID



    #These functions return the moves on the board in chess notation
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


