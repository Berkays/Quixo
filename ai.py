import math
import hashlib
import os
import pickle
import numpy as np
from board import Board

MAX_PLAYER = Board.X # (Player:X)
MIN_PLAYER = Board.O # (Player:O)
bestMove = None
transpositionPath = "t.dat"
transpositionTable = {}

def minimax(board,player,alpha,beta,depth):
    global bestMove

    score = evaluate(board,depth)
    if(score is not None):
        return score

    depth -= 1

    scores = []
    moves = []
    if(player == MAX_PLAYER):
        for move in board.getPossibleMoves():
            s = Board(board)
            s.play(move[0],move[1])
            val = minimax(s,s.turn,alpha,beta,depth)
            scores.append(val)
            moves.append(move)
            if(val > alpha):
                alpha = val
            if(alpha >= beta):
                bestMove = moves[scores.index(max(scores))]
                return alpha
        bestMove = moves[scores.index(max(scores))]
        return alpha
    else:
        for move in board.getPossibleMoves():
            s = Board(board)
            s.play(move[0],move[1])
            val = minimax(s,s.turn,alpha,beta,depth)
            scores.append(val)
            moves.append(move)
            if(val < beta):
                beta = val
            if(beta <= alpha):
                bestMove = moves[scores.index(min(scores))]
                return beta
        bestMove = moves[scores.index(min(scores))]
        return beta

def evaluate(board,depth):
    isTerminal = board.isGameEnd()
    if(isTerminal == MAX_PLAYER):
        return 1 + depth #Maximizer won(X)
    elif(isTerminal == MIN_PLAYER):
        return -1 - depth #Minimizer Won(O)
    elif(depth == 0):
        frequency = np.unique(board.board,return_counts=True)
        try:
            if(frequency[1][1] > frequency[1][2]):
                return 1
            else:
                return -1
        except:
            if(frequency[1][0] > frequency[1][1]):
                return 1
            else:
                return -1
    else:
        return None

def getBestMove(board,player,depthLevels,useTransposition):
    possibleMoves = board.getPossibleMoves()
    possibleMoveCount = len(possibleMoves)

    # Iterative deepening based on possible move count
    depth = 0
    for depthLvl in depthLevels:
        if (possibleMoveCount > depthLvl[1]):
            depth = depthLvl[0]
        else:
            break

    if(useTransposition and depth > 3):
        move = getMoveFromTranspositionTable(board)
        if (move is not None):
            return move

    minimax(board,board.turn,-math.inf,math.inf,depth)

    if(useTransposition and depth > 3):
        addToTranspositionTable(board,bestMove)

    return bestMove

def loadTranspositionTable():
    global transpositionTable
    if (os.path.isfile(transpositionPath)):
        tableFile = open(transpositionPath,mode='rb')
        transpositionTable = pickle.load(tableFile)
        tableFile.close()
        print("Loaded transposition table")

def saveTranspositionTable():
    global transpositionTable
    tableFile = open(transpositionPath, mode='wb')
    pickle.dump(transpositionTable,tableFile)
    tableFile.close()
    print("Saved transposition table")

def addToTranspositionTable(state,move):
    global transpositionTable
    boardData = state.board.tobytes()
    turnStr = str(state.turn)
    hash = hashlib.md5(boardData).hexdigest()
    hash += turnStr
    if(hash not in transpositionTable):
        transpositionTable[hash] = move
        print("Move added to table")

def getMoveFromTranspositionTable(state):
    global transpositionTable
    boardData = state.board.tobytes()
    turnStr = str(state.turn)
    hash = hashlib.md5(boardData).hexdigest()
    hash += turnStr
    if(hash in transpositionTable):
        return transpositionTable[hash]
    else:
        return None
