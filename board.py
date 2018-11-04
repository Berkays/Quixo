import numpy as np
from random import shuffle

class Board(object):
    BOARD_SIZE = 4 # 0 indexed

    #moves
    SLIDE_LEFT = 0
    SLIDE_UP = 1
    SLIDE_RIGHT = 2
    SLIDE_DOWN = 3

    #Piece Values
    BLANK = 0
    X = 1
    O = 2

    def __init__(self,board=None):
        self.turn = self.X
        if(board == None):
            self.board = np.zeros((5,5),dtype=int)
        else:
            self.board = np.copy(board.board)
            self.turn = board.turn

    def play(self,piece,move):
        # legalMove = self.checkMove(piece,move)
        # if(not legalMove):
        #     raise Exception('Illegal Move')

        self.board[piece] = self.turn
        self.shift(piece,move)
        self.changeTurn()

    def checkMove(self,piece,move):
        #Only blank and owned pieces
        if(not (self.board[piece] == self.BLANK or self.board[piece] == self.turn)):
            return False

        possibleMoves = self.getPossiblePieceMoves(piece)
        if(move in possibleMoves):
            return True
        else:
            return False

    def shift(self,piece,move):
        row,col = piece

        if(move == self.SLIDE_RIGHT):
            self.board[row,0:col + 1] = np.roll(self.board[row,0:col + 1],1)
        elif(move == self.SLIDE_LEFT):
            self.board[row,col:self.BOARD_SIZE + 1] = np.roll(self.board[row,col:self.BOARD_SIZE + 1],-1)
        elif(move == self.SLIDE_UP):
            self.board[row:self.BOARD_SIZE + 1,col] = np.roll(self.board[row:self.BOARD_SIZE + 1,col],-1)
        else:
            self.board[0:row + 1,col] = np.roll(self.board[0:row + 1,col],1)

        return

    def changeTurn(self):
        if(self.turn == self.X):
            self.turn = self.O
        else:
            self.turn = self.X

    def isGameEnd(self):
        firstDiagonal = np.diagonal(self.board)
        secondDiagonal = np.diagonal(np.rot90(self.board))

        if(np.all(firstDiagonal == self.X) or np.all(firstDiagonal == self.O)):
            return self.board[0,0]
        if(np.all(secondDiagonal == self.X) or np.all(secondDiagonal == self.O)):
            return self.board[0,self.BOARD_SIZE]
        
        for i in range(0,self.BOARD_SIZE + 1):
            row = self.board[i,:]
            col = self.board[:,i]
            if(np.all(row == self.X) or np.all(row == self.O)):
                return self.board[i,0]
            if(np.all(col == self.X) or np.all(col == self.O)):
                return self.board[0,i]
        
        return None
      
    def getPossiblePieceMoves(self,piece):
        row = piece[0]
        col = piece[1]
        possibleMoves = []

        if(row < self.BOARD_SIZE):
            possibleMoves.append(self.SLIDE_UP)
        if(row > 0):
            possibleMoves.append(self.SLIDE_DOWN)
        if(col < self.BOARD_SIZE):
            possibleMoves.append(self.SLIDE_LEFT)
        if(col > 0):
            possibleMoves.append(self.SLIDE_RIGHT)

        return possibleMoves

    def getPossibleMoves(self):
        if(self.turn == self.X):
            arg = self.O 
        else:
            arg = self.X

        edgeMatrix = np.full((5,5),arg)
        edgeMatrix[0,:] = self.board[0,:]
        edgeMatrix[4,:] = self.board[4,:]
        edgeMatrix[:,0] = self.board[:,0]
        edgeMatrix[:,4] = self.board[:,4]

        edgeIndices = np.where(edgeMatrix != arg)
        edgeIndices = np.column_stack((edgeIndices[0],edgeIndices[1]))
        allMoves = []
        for piece in edgeIndices:
            piece = (piece[0],piece[1])
            moves = self.getPossiblePieceMoves(piece)
            for move in moves:
                allMoves.append((piece,move))

        shuffle(allMoves)

        return allMoves       

    def printTurn(self):
        if(self.turn == self.X):
            print("Turn: X")
        else:
            print("Turn: O")

    def printBoard(self):            
        def valToChar(x):
            if(x == 0):
                return '-'
            elif(x == 1):
                return 'X'
            else:
                return 'O'
        print(np.array2string(self.board,formatter = {'all': valToChar}))
