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


        self.whiteToMove = True #Initializes first player
        self.moveLog = [] #keeps track of moves made

    '''
    Takes a move and executes it, will not work for castling, pawn promotion or en-passant
    '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--" #replace original position of piece
        self.board[move.endRow][move.endCol] = move.pieceMoved #set new postion to piece moved
        self.moveLog.append(move) #add the move to the move log
        self.whiteToMove = not self.whiteToMove #swap players turn


    '''
    Undo the last move of the game
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop() #remove move from move log
            self.board[move.startRow][move.startCol] = move.pieceMoved #replace moved piece
            self.board[move.endRow][move.endCol] = move.pieceCaptured #replace captured space
            self.whiteToMove = not self.whiteToMove  # swap players turn

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


    #These functions return the moves on the board in chess notation
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)


    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


