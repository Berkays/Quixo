import numpy as np

class Board(object):
    BOARD_SIZE = 4 # 0 indexed

    SLIDE_LEFT = 0
    SLIDE_UP = 1
    SLIDE_RIGHT = 2
    SLIDE_DOWN = 3

    #Piece Values
    BLANK = 0
    X = 1
    O = 2

    def __init__(self):
        self.turn = self.X
        self.board = np.zeros((5,5),dtype=int)

    def play(self,piece,move):
        isMoveValid = self.checkMove(piece,move)
        if(not isMoveValid):
            return
        self.board[piece[0]][piece[1]] = self.turn
        self.shiftBoard(piece,move)
        if(self.turn == self.X):
            self.turn = self.O
        else:
            self.turn = self.X


    def checkMove(self,piece,move):
        row = piece[0]
        col = piece[1]
        
        if(move == self.SLIDE_RIGHT):
            if(col != self.BOARD_SIZE):
                return False
        if (move == self.SLIDE_LEFT):
            if (col != 0):
                return False

        #Only edge pieces
        if(row > 0 and row < self.BOARD_SIZE):
            if(col != 0 or col != self.BOARD_SIZE):
                return False
        #Only edge pieces
        if (col > 0 and col < self.BOARD_SIZE):
            if (row != 0 or row != self.BOARD_SIZE):
                return False


        if(self.SLIDE_DOWN):
            if(row != self.BOARD_SIZE):
                return False

        if (self.SLIDE_UP):
            if (row != 0):
                return False

        if (self.SLIDE_LEFT):
            if (col != 0):
                return False

        if (self.SLIDE_RIGHT):
            if (col != self.BOARD_SIZE):
                return False

        #Only blank and owned pieces
        if(self.board[row][col] == self.BLANK or self.board[row][col] == self.turn):
            return True

    def shiftBoard(self,piece,move):
        row = piece[0]
        col = piece[1]
        if(move == self.SLIDE_LEFT):
            self.board[row,:] = np.roll(self.board[row,:],-1)
        elif(move == self.SLIDE_RIGHT):
            self.board[row, :] = np.roll(self.board[row, :], 1)
        elif(move == self.SLIDE_UP):
            self.board[:, col] = np.roll(self.board[:, col], -1)
        elif(move == self.SLIDE_DOWN):
            self.board[:, col] = np.roll(self.board[:, col], 1)

    def printTurn(self):
        if(self.turn == self.X):
            print("Turn: X")
        else:
            print("Turn: O")

    def printBoard(self):
        print(self.board)
