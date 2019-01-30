import os
import time
import signal
import argparse
from tqdm import tqdm
import numpy as np
from board import Board
from players import AI_Player,RandomPlayer,Human_Player,Q_Player,Neural_Player

# Uncomment to use CPU for prediction
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

args = None

dataset = "datasets/dataset_move_ai.npz"

stopPlay = False

# CTRL + C Handler
def signalHandler(signal,frame):
    global stopPlay
    stopPlay = True

GOD = [(6,0),(4,22),(1,32)]
GOOD_AI_PLAYER = [(4,0),(3,22),(2,28),(1,35)]
BAD_AI_PLAYER = [(2,0),(1,28)]

DEPTH_1_PLAYER = [(1,0)]
DEPTH_2_PLAYER = [(2,0),(1,32)]
DEPTH_3_PLAYER = [(3,0),(1,32)]
DEPTH_4_PLAYER = [(4,0),(1,32)]

def play(player1,player2):
    global stopPlay

    startTime = time.time()

    signal.signal(signal.SIGINT,signalHandler)

    xWins = 0
    oWins = 0
    
    X = []
    Y = []

    # if(args.save == 1):
    #     try:
    #         data = np.load(dataset)
    #         X = list(data['arr_0'])
    #         Y = list(data['arr_1'])

    #         print(f"Loaded {len(X)} elements")
    #     except:
    #         pass

    for _ in tqdm(range(0,args.iteration)):
        if(stopPlay):
            break
        gameState = Board()

        label_index = len(Y)
        winnerScore = 0
        num_turns = 0
        while True:
            if(stopPlay):
                break
            
            player1.playTurn(gameState)
            winner = gameState.isGameEnd()
            
            X.append(gameState.serialize())
            Y.append(winnerScore)
            #move = (move[0][0],move[0][1],move[1])
            #Y.append(np.array(move))

            if(winner == Board.X):
                xWins += 1
                #X.append(gameState.serialize())
                #Y.append(1)
                winnerScore = 1
                break
            elif(winner == Board.O):
                oWins += 1
                #X.append(gameState.serialize())
                #Y.append(0)
                break


            #gameState.printBoard()

            player2.playTurn(gameState)
            winner = gameState.isGameEnd()

            X.append(gameState.serialize())
            Y.append(winnerScore)
            # Y.append(winner)
            
            if(winner == Board.X):
                xWins += 1
                #X.append(gameState.serialize())
                #Y.append(1)
                winnerScore = 1
                break
            elif(winner == Board.O):
                oWins += 1
                #X.append(gameState.serialize())
                #Y.append(0)
                break

            #gameState.printBoard()
            # print()
        
        if(winnerScore == 1):
            Y[label_index:len(Y)] = [winnerScore] * (len(Y) - label_index) 
        #gameState.printBoard()

    if(args.save == 1):
        data = np.load(dataset)
        _X = list(data['arr_0'])
        _Y = list(data['arr_1'])
        X = X + _X
        Y = Y + _Y
        X = np.array(X)
        Y = np.array(Y)
        print(f"Saving dataset with {len(X)} elements")
        np.savez(dataset, X, Y)
    
    print(f"Elapsed: {time.time() - startTime}")
    print(f"X Wins: {xWins}, O Wins: {oWins}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Quixo Game")
    parser.add_argument('-i','--iteration',required=False,type=int, nargs="?",const=100, help='Number of simulation iterations')
    parser.add_argument('-s','--save',     required=False,type=int, nargs="?",const=0, help='Save game simulation')
    parser.add_argument('-p1','--player1', required=True, type=str, help='Player 1')
    parser.add_argument('-p2','--player2', required=True, type=str, help='Player 2')

    args = parser.parse_args()

    if(args.player1 == "alpha"):
        player1 = AI_Player(BAD_AI_PLAYER)
    elif(args.player1 == "neural"):
        player1 = Neural_Player()
    elif(args.player1 == "random"):
        player1 = RandomPlayer()
    elif(args.player1 == "human"):
        player1 = Human_Player()

    if(args.player2 == "alpha"):
        player2 = AI_Player(BAD_AI_PLAYER)
    elif(args.player2 == "neural"):
        player2 = Neural_Player()
    elif(args.player2 == "random"):
        player2 = RandomPlayer()
    elif(args.player2 == "human"):
        player2 = Human_Player()

    play(player1,player2)