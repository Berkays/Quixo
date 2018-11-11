import math
import random
import time
import hashlib
import os
import pickle
import numpy as np
from board import Board

transpositionPath = "_t.dat"
transpositionPlayer = Board.X
transpositionTable = {}

def alphabeta(board,alpha,beta,depth):

    score = evaluate(board,depth)
    if(score is not None): # Return board value if hit terminal
        return (score,None)

    depth -= 1

    bestMove = None
    if(board.turn == Board.X):
        for move in board.getPossibleMoves():
            s = Board(board)
            s.play(move[0],move[1])
            val = alphabeta(s,alpha,beta,depth)[0]

            if(val > alpha):
                alpha = val
                bestMove = move
            if(alpha >= beta):
                break
        return (alpha,bestMove)
    else:
        for move in board.getPossibleMoves():
            s = Board(board)
            s.play(move[0],move[1])
            val = alphabeta(s,alpha,beta,depth)[0]

            if(val < beta):
                beta = val
                bestMove = move
            if(alpha >= beta):
                break
        return (beta,bestMove)

def evaluate(board,depth):
    isTerminal = board.isGameEnd()
    if(isTerminal == Board.X): # Maximizer won (X)
        return 100 + depth # Less moves is better
    elif(isTerminal == Board.O): # Minimizer Won (O)
        return -100 - depth # Less moves is better
    elif(depth == 0): # Compare owned piece counts if we reach tree depth limit
        frequency = np.unique(board.board,return_counts=True)
        if(len(frequency[0]) == 3): # Contains blank pieces
            maximizerPieceCount = frequency[1][1]
            minimizerPieceCount = frequency[1][2]
        else:
            maximizerPieceCount = frequency[1][0]
            minimizerPieceCount = frequency[1][1]
            
        return maximizerPieceCount - minimizerPieceCount
    else:
        return None

def getBestMove(board,depthLevels,useTransposition=False):
    possibleMoves = board.getPossibleMoves()
    possibleMoveCount = len(possibleMoves)

    # Iterative deepening based on possible move count
    depth = 0
    for depthLvl in depthLevels:
        if (possibleMoveCount > depthLvl[1]):
            depth = depthLvl[0]
        else:
            break

    move = None
    if(useTransposition and board.turn == transpositionPlayer and depth >= 4):
        move = getMoveFromTranspositionTable(board,depth)
        if (move is not None):
            return move

    move = alphabeta(board,-math.inf,math.inf,depth)[1]

    if(useTransposition and board.turn == transpositionPlayer and depth >= 4):
        addToTranspositionTable(board,move,depth)

    return move

def loadTranspositionTable():
    setTranspositionPath()

    if (os.path.isfile(transpositionPath)):
        tableFile = open(transpositionPath,mode='rb')
        transpositionTable = pickle.load(tableFile)
        tableFile.close()
        print(f"Loaded transposition table: {len(transpositionTable)} elements")

def saveTranspositionTable():
    global transpositionTable
    tableFile = open(transpositionPath, mode='wb')
    pickle.dump(transpositionTable,tableFile)
    tableFile.close()
    print(f"Saved transposition table: {transpositionPath}")

def addToTranspositionTable(state,move,depth):
    global transpositionTable
    boardData = state.board.tobytes()
    hash = hashlib.md5(boardData).hexdigest()
    hash += hash + str(depth)
    if(hash not in transpositionTable):
        transpositionTable[hash] = move
        print(f"{move} added to table")

def getMoveFromTranspositionTable(state,depth):
    global transpositionTable
    boardData = state.board.tobytes()
    hash = hashlib.md5(boardData).hexdigest()
    hash += hash + str(depth)
    if(hash in transpositionTable):
        return transpositionTable[hash]
    else:
        return None

def setTranspositionPath():
    global transpositionPath
    if (transpositionPlayer == Board.X):
        transpositionPath = "x" + transpositionPath
    else:
        transpositionPath = "o" + transpositionPath
    return