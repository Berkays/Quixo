import random
import math
from board import Board

MAX_PLAYER = 1 # (Player:X)
MIN_PLAYER = 2 # (Player:O)

def minimax(board,player,alpha,beta,depth):
    isTerminal = board.isGameEnd()
    if(isTerminal == 1): 
        return 1 #Maximizer won(X)
    elif(isTerminal == 2):
        return -1 #Minimizer Won(O)
    if(depth == 0):
        return 0
        # frequency = np.unique(board.board,return_counts=True)
        # try:
        #     if(frequency[1][1] > frequency[1][2]):
        #         return 1
        #     else:
        #         return -1
        # except:
        #     if(frequency[1][0] > frequency[1][1]):
        #         return 1
        #     else:
        #         return -1
    if(player == MAX_PLAYER):
        for move in board.getPossibleMoves():
            s = Board(board)
            s.play(move[0],move[1])
            val = minimax(s,s.turn,alpha,beta,depth - 1)
            if(val > alpha):
                alpha = val	
            if(alpha >= beta):
                return alpha
        
        return alpha
    else:
        for move in board.getPossibleMoves():
            s = Board(board)
            s.play(move[0],move[1])
            val = minimax(s,s.turn,alpha,beta,depth - 1)
            if(val < beta):
                beta = val
            if(beta <= alpha):
                return beta
        
        return beta

def bestMove(board,player,depth):
    alpha = -math.inf
    beta = math.inf
    moves = []
    possibleMoves = board.getPossibleMoves()
    if(len(possibleMoves) > 30):
        depth = 2
    elif(len(possibleMoves) > 20):
        depth = 3
    elif(len(possibleMoves) > 14):
        depth = 4
    else:
        depth = 5
    if(player == MAX_PLAYER):
        for move in possibleMoves:
            s = Board(board)
            s.play(move[0],move[1])
            val = minimax(s,s.turn,-math.inf,math.inf,depth)
            if(val > alpha):
                alpha = val
                moves = [move]
            elif(val == alpha):
                moves.append(move) 
    else:
        for move in possibleMoves:
            s = Board(board)
            s.play(move[0],move[1])
            val = minimax(s,s.turn,-math.inf,math.inf,depth)
            if(val < beta):
                beta = val
                moves = [move]
            elif(val == beta):
                moves.append(move)
    return moves[random.randint(0,len(moves) - 1)]