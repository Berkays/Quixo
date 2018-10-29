import numpy as np
from board import Board

class State(object):
    def __init__(self,board=None):
        if(board is None):
            #create new board
            self.board = Board()
        else:
            self.board = board

    def serialize(self):
        return 1


if __name__ == "__main__":
    state = State()
    state.board.play((0, 2), Board.SLIDE_UP)
    state.board.printTurn()
    state.board.printBoard()
    state.board.play((2,4),Board.SLIDE_RIGHT)
    state.board.printTurn()
    state.board.printBoard()
    state.board.play((3,4),Board.SLIDE_UP)
    state.board.printTurn()
    state.board.printBoard()
    state.board.play((0,0),Board.SLIDE_UP)
    state.board.printTurn()
    state.board.printBoard()
    #state.board.play(Board.X,(0,0),Board.SLIDE_RIGHT)
    #state.board.play(Board.X,(0,0),Board.SLIDE_RIGHT)