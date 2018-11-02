import numpy as np

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

    def __init__(self):
        self.turn = self.X
        self.board = np.zeros((5,5),dtype=int)

    def play(self,piece,move):
        legalMove = self.checkMove(piece,move)
        if(not legalMove):
            raise Exception('Illegal Move')

        self.board[piece] = self.turn
        #self.shiftBoard(piece,move)
        self.shift(piece,move)
        self.changeTurn()


    def checkMove(self,piece,move):
        #Only blank and owned pieces
        if(not (self.board[piece] == self.BLANK or self.board[piece] == self.turn)):
            return False

        possibleMoves = self.getPossibleMoves(piece)
        if(move in possibleMoves):
            return True
        else:
            return False

    def getPossibleMoves(self,piece):
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

    def shift(self,piece,move):
        row,col = piece

        if(move == self.SLIDE_RIGHT):
            self.board[row,0:col + 1] = np.roll(self.board[row,0:col + 1],1)
        elif(move == self.SLIDE_LEFT):
            self.board[row,col:self.BOARD_SIZE + 1] = np.roll(self.board[row,col:self.BOARD_SIZE + 1],-1)
        elif(move == self.SLIDE_UP):
            self.board[row:self.BOARD_SIZE + 1,col] = np.roll(self.board[row:self.BOARD_SIZE + 1,col],1,axis=1)
        else:
            self.board[0:row + 1,col] = np.roll(self.board[0:row + 1,col],-1,axis=1)

        
        return

    def changeTurn(self):
        if(self.turn == self.X):
            self.turn = self.O
        else:
            self.turn = self.X

    def getAllPossibleMoves(self):
        edgeTuples = []
        x = self.board.copy()
        x[:,0] = 1
        x[:,self.BOARD_SIZE] = 1
        x[0,:] = 1
        x[self.BOARD_SIZE,:] = 1
        
        for i in range(0, self.BOARD_SIZE + 1):
            for k in range(0, self.BOARD_SIZE + 1):
                if(x[(i,k)] == 1 and (i,k) not in edgeTuples and self.board[(i,k)] == self.BLANK or self.board[(i,k)] == self.turn):
                    edgeTuples.append((i,k))

        allMoves = []
        for piece in edgeTuples:
            moves = self.getPossibleMoves(piece)
            for move in moves:
                allMoves.append((piece,move))

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
