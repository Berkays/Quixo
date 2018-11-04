from board import Board
from ai import bestMove

MAX_PLAYER = 1 # (Player:X)
MIN_PLAYER = 2 # (Player:O)

# SLIDE_LEFT = 0
# SLIDE_UP = 1
# SLIDE_RIGHT = 2
# SLIDE_DOWN = 3

if __name__ == "__main__":
    iteration = 5
    xWins = 0
    oWins = 0
    
    for i in range(0,iteration):
        gameState = Board()
        depth = 1
        moveCount = 0
        while True:
            move = bestMove(gameState,gameState.turn,depth)
            gameState.play(move[0],move[1])
            moveCount += 1
            depth = int(moveCount / 10) + 1
            print(depth)
            gameState.printBoard()
            winner = gameState.isGameEnd()
            if(winner == MAX_PLAYER):
                xWins += 1
                break
            elif(winner == MIN_PLAYER):
                oWins += 1
                break


    print(f"X Wins: {xWins}\nO Wins: {oWins}")