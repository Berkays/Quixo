class Player:
    def __init__(self):
        pass

    # Override this method
    def playTurn(self,board):
        pass

from numpy.random import randint
class RandomPlayer(Player):
    def __init__(self):
        Player.__init__(self)

    def playTurn(self, board):
        possibleMoves = board.getPossibleMoves()
        choice = randint(0,len(possibleMoves))
        move = possibleMoves[choice]
        board.play(move[0],move[1])

from ai import getBestMove
class AI_Player(Player):
    def __init__(self,depthLevels):
        Player.__init__(self)
        self.depthLevels = depthLevels

    def playTurn(self,board):
        move = getBestMove(board,self.depthLevels)
        board.play(move[0],move[1])

class Human_Player(Player):
    def __init__(self):
        Player.__init__(self)

    def playTurn(self, board):
        while (True):
            try:
                inp = input("Your turn: ")
                (piece, move) = self.input_map(inp)
                board.play(piece, move)
                break
            except:
                pass

    def input_map(self,inp):
        split = inp.split(' ')
        try:
            piece = (int(split[0]), int(split[1]))
            move = split[2]

            if (move == "left" or move == "l"):
                move = 0
            elif (move == "up" or move == "u"):
                move = 1
            elif (move == "right" or move == "r"):
                move = 2
            elif (move == "down" or move == "d"):
                move = 3

            return (piece, move)
        except:
            return None