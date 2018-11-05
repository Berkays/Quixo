from board import Board
from ai import bestMove

MAX_PLAYER = 1 # (Player:X)
MIN_PLAYER = 2 # (Player:O)

# SLIDE_LEFT = 0
# SLIDE_UP = 1
# SLIDE_RIGHT = 2
# SLIDE_DOWN = 3

AI_PLAYER = [(5,0),(4,18),(3,22),(2,28),(1,40)]
BAD_AI_PLAYER = [(2,0),(1,30)]
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
if __name__ == "__main__":
    iteration = 10
    xWins = 0
    oWins = 0

#COMPUTER VS COMPUTER
    for i in range(0,iteration):
        gameState = Board()
        while True:
            move = bestMove(gameState,gameState.turn,BAD_AI_PLAYER)
            gameState.play(move[0],move[1])
            gameState.printBoard()
            winner = gameState.isGameEnd()
            if(winner == MAX_PLAYER):
                xWins += 1
                print(f"X Wins: {xWins}\nO Wins: {oWins}")
                break
            elif(winner == MIN_PLAYER):
                oWins += 1
                print(f"X Wins: {xWins}\nO Wins: {oWins}")
                break


#PLAYER VS COMPUTER
    #gameState = Board()
    # while True:
    #     move = bestMove(gameState,gameState.turn)
    #     gameState.play(move[0],move[1])
    #     gameState.printBoard()
    #     winner = gameState.isGameEnd()
    #     if(winner is not None):
    #         print(winner)
    #         break
    #     valid = -1
    #     while(valid == -1):
    #         inp = input("Your turn: ")
    #         (piece,umove) = input_map(inp)
    #         valid = gameState.play(piece,umove)
    #     winner = gameState.isGameEnd()
    #     if(winner is not None):
    #         print(winner)
    #         break
