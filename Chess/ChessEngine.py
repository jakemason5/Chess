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


        self.whiteToMove = True
        self.moveLog = []