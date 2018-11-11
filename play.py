import time
import sys
import signal
from board import Board
from players import AI_Player,RandomPlayer,Human_Player
from ai import loadTranspositionTable,saveTranspositionTable

# CTRL + C Handler
stopPlay = False
def signalHandler(signal,frame):
    global stopPlay
    stopPlay = True

GOD = [(6,0),(4,22),(1,32)]
GOOD_AI_PLAYER = [(5,0),(4,17),(3,22),(2,29),(1,36)]
BAD_AI_PLAYER = [(2,0),(1,30)]

DEPTH_1_PLAYER = [(1,0)]
DEPTH_2_PLAYER = [(2,0)]
DEPTH_3_PLAYER = [(3,0)]
DEPTH_4_PLAYER = [(4,0)]

def play(player1,player2,iteration,transposition=False):
    global stopPlay

    if(transposition):
        loadTranspositionTable()

    startTime = time.time()

    signal.signal(signal.SIGINT,signalHandler)

    xWins = 0
    oWins = 0
    
    for i in range(0,iteration):
        if(stopPlay):
            break
        gameState = Board()
        print(f"Playing iteration: {i}")
        while True:
            if(stopPlay):
                break
            
            player1.playTurn(gameState)

            winner = gameState.isGameEnd()
            if(winner == Board.X):
                xWins += 1
                break
            elif(winner == Board.O):
                oWins += 1
                break

            player2.playTurn(gameState)

            winner = gameState.isGameEnd()
            if(winner == Board.X):
                xWins += 1
                break
            elif(winner == Board.O):
                oWins += 1
                break

            #gameState.printBoard()
        
        gameState.printBoard()
    print(f"Elapsed: {time.time() - startTime}")
    print(f"X Wins: {xWins}, O Wins: {oWins}")

    if(transposition):
        saveTranspositionTable()


if __name__ == "__main__":
    play(AI_Player(GOOD_AI_PLAYER),RandomPlayer(),100,True)