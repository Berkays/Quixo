from board import Board
from numpy.random import randint
from ai import getBestMove
import numpy as np
import operator
import pickle
from keras.models import load_model

class Player:
    def __init__(self):
        pass

    # Override this method
    def playTurn(self,board):
        pass

class RandomPlayer(Player):
    def __init__(self):
        Player.__init__(self)

    def playTurn(self, board):
        possibleMoves = board.getPossibleMoves()
        choice = randint(0,len(possibleMoves))
        move = possibleMoves[choice]
        board.play(move[0],move[1])
        return move

class AI_Player(Player):
    def __init__(self,depthLevels):
        Player.__init__(self)
        self.depthLevels = depthLevels

    def playTurn(self,board):
        move = getBestMove(board,self.depthLevels)
        board.play(move[0],move[1])
        return move

class Q_Player(Player):
    def __init__(self,
                 exploration_rate=0.33,
                 learning_rate=0.5,
                 discount_factor=0.01):
        Player.__init__(self)
        self.states = {}

        self.load_table("data.bin")

        self.state_order = []
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

    def unpackMove(self,action):
        action = (action[0][0], action[0][1], action[1])
        return ''.join(map(str,action))

    def initState(self,new_state_key):
        self.states[new_state_key] = {}

    def learn_by_temporal_difference(self, reward, new_state_key, state_key,action,new_action):
        if(new_action not in self.states[new_state_key]):
            self.states[new_state_key][new_action] = 0
        if(action not in self.states[state_key]):
            self.states[state_key][action] = 0
        return self.learning_rate * (reward + (self.discount_factor * self.states[new_state_key][new_action]) - self.states[state_key][action])
        # return self.learning_rate * ((reward * self.states[new_state_key]) - old_state)
        # return self.learning_rate * (reward + (self.discount_factor * self.states[new_state_key][new_action]) - self.states[state_key][action])

    def set_state(self, old_board, action):
        state_key = old_board.serialize()
        self.state_order.append((state_key, action))

    def on_reward(self, reward):
        if len(self.state_order) == 0:
            return None
        new_state_key, new_action = self.state_order.pop()
        # get the latest state and the action performed that led to the reward
        self.initState(new_state_key)
        self.states[new_state_key][new_action] = reward
        # Assign the reward to this state

        while self.state_order:
            # while there is a stack of states (that were caused by actions performed)

            state_key, action = self.state_order.pop()
            # get the state and action performed on it

            # reward *= self.discount_factor
            # Reduce the original reward (self.discount_factor is a number < 1)

            # Implementation of the value function
            if state_key in self.states:
                # If this state was encountered due to a different experiment, increase its previous value
                # reward += self.learn_by_temporal_difference(reward, new_state_key, state_key,action,new_action)[new_action]
                reward += self.learn_by_temporal_difference(reward, new_state_key, state_key,action,new_action)
                self.states[state_key][action] = reward
            else:
                # If this state was not encountered before, assign it the discounted reward as its value
                #self.states[state_key] = np.zeros((5, 5, 4))
                self.initState(state_key)
                # reward = self.learn_by_temporal_difference(reward, new_state_key, state_key,action,new_action)[new_action]
                reward = self.learn_by_temporal_difference(reward, new_state_key, state_key,action,new_action)
                self.states[state_key][action] = reward
            new_state_key = state_key
            new_action = action

    def select_move(self, board):
        state_key = board.serialize()
        exploration = np.random.random() < self.exploration_rate
        #print('explore' if exploration or state_key not in self.states else 'exploit')
        action = self.explore_board(board) if exploration or state_key not in self.states else self.exploit_board(state_key)

        self.set_state(board, action)
        return action

    def explore_board(self, board):
        possibleMoves = board.getPossibleMoves()
        choice = randint(0, len(possibleMoves))
        move = possibleMoves[choice]
        move = self.unpackMove(move)
        return move

    def exploit_board(self, state_key):
        state_values = self.states[state_key]
        #print('State rewards')
        #print(state_values)
        z = max(state_values.items(),key=operator.itemgetter(1))[0]
        # best_actions_x, best_actions_y, best_actions_z = np.where(state_values == state_values.max())
        # # Find the coordinates which correspond to highest reward

        # best_value_indices = [(x, y, z)
        #                       for x, y, z in zip(best_actions_x, best_actions_y, best_actions_z)]
        # select_index = np.random.choice(len(best_value_indices))
        return z

    def load_table(self,filename):
        try:
            file = open(filename,mode="rb")
            self.states = pickle.load(file)
            file.close()
        except:
            pass
    def save_table(self,filename):
        file = open(filename,mode="wb")
        pickle.dump(self.states,file)
        file.close()

    def playTurn(self, board):
        move = self.select_move(board)
        move = ((int(move[0]),int(move[1])),int(move[2]))
        board.play(move[0], move[1])

model = load_model('value.h5')
class Neural_Player(Player):
    def __init__(self):
        Player.__init__(self)

    def playTurn(self, board):
        possibleMoves = board.getPossibleMoves()
        boards = []
        for move in possibleMoves:
            s = Board(board)
            s.play(move[0],move[1])
            s = s.serialize() / 2
            s = np.expand_dims(s, axis=-1)
            boards.append(s)
        #     score = self.model.predict(s)[0][0]
        #     if(score > bestScore):
        #         bestScore = score
        #         bestMove = move
        # return bestMove
        predictions = model.predict(np.array(boards))
        if(board.turn == Board.X):
            print(predictions)
            return possibleMoves[np.argmax(predictions[0])]
        else:
            return possibleMoves[np.argmin(predictions[0])]

class Human_Player(Player):
    def __init__(self):
        Player.__init__(self)
        self.BOARD_SIZE = Board.BOARD_SIZE

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