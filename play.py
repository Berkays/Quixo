import time
from board import Board
from ai import getBestMove,saveTranspositionTable,loadTranspositionTable

MAX_PLAYER = Board.X # (Player:X)
MIN_PLAYER = Board.O # (Player:O)

# Moves:
# SLIDE_LEFT = 0
# SLIDE_UP = 1
# SLIDE_RIGHT = 2
# SLIDE_DOWN = 3

GOD = [(6,0),(4,22),(1,32)]
GOOD_AI_PLAYER = [(5,0),(4,18),(3,23),(2,29),(1,34)]
BAD_AI_PLAYER = [(3,0),(2,24),(1,32)]
WORST_AI_PLAYER = [(1,0)]

def input_map(inp):
    split = inp.split(' ')
    try:
        piece = (int(split[0]),int(split[1]))
        move = split[2]
        
        if(move == "left"):
            move = 0
        elif(move == "up"):
            move = 1
        elif(move == "right"):
            move = 2
        elif(move == "down"):
            move = 3
        
        return (piece,move)
    except:
        return None

def computer_computer_play(iteration,ai_player,useTransposition):
    startTime = time.time()

    xWins = 0
    oWins = 0
    
    if(useTransposition):
        loadTranspositionTable()
    
    for i in range(0,iteration):
        gameState = Board()
        print(f"Playing iteration: {i}")
        while True:
            move = getBestMove(gameState,gameState.turn,ai_player,useTransposition)
            gameState.play(move[0],move[1])
            winner = gameState.isGameEnd()
            if(winner == MAX_PLAYER):
                xWins += 1
                print(f"X Wins: {xWins}\nO Wins: {oWins}")
                break
            elif(winner == MIN_PLAYER):
                oWins += 1
                print(f"X Wins: {xWins}\nO Wins: {oWins}")
                break

    print(f"Elapsed: {time.time() - startTime}")

    if(useTransposition):
        saveTranspositionTable()

def computer_player_play(ai_player,useTransposition):
    gameState = Board()

    if(useTransposition):
        loadTranspositionTable()

    gameResult = 0
    while True:
        move = getBestMove(gameState,gameState.turn,ai_player,useTransposition)
        gameState.play(move[0],move[1])
        gameState.printBoard()
        gameResult = gameState.isGameEnd()
        
        if(gameResult is not None):
            break

        isMoveValid = -1
        while(isMoveValid == -1):
            inp = input("Your turn: ")
            (piece,umove) = input_map(inp)
            isMoveValid = gameState.play(piece,umove)

        gameResult = gameState.isGameEnd()
        if(gameResult is not None):
            break
    
    gameState.printWinner()

    if(useTransposition):
        saveTranspositionTable()

if __name__ == "__main__":
    computer_computer_play(10,GOOD_AI_PLAYER,True)