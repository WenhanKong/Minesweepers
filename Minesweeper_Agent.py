import time
from timeit import default_timer as timer
import MalmoPython
import math
import json 
import random
import operator
from collections import Counter
from Minesweeper_Game import Minesweeper


def choose_random(game):
    while True:
        x = random.randint(0, game.size-1)
        z = random.randint(0, game.size-1)
        if not game.board[x][z].visible:
            return (x,z)

def inbounds(row, col, game_size):
    if 0<=row<game_size and 0<=col<game_size:
        return True
    else:
        return False


def get_frontier_by_state(state, game_size):
    frontier = []
    directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

    for row in range(game_size):
        for col in range(game_size):
            current_tile = state[row][col]
            # -- if the tile is invisible -- #
            if current_tile == -1:
                for dx, dy in directions:
                    if inbounds(row+dx, col+dy, game_size):
                        neighbor_tile = state[row+dx][col+dy]
                        # -- if neighbor tile is visible and counter != 0 -- #
                        if neighbor_tile > 0 and neighbor_tile not in frontier:
                            frontier.append((row, col))
    return frontier

def get_possible_moves_by_board(game_board):
    possible_moves = []
    for row in range(len(game_board)):
        for col in range(len(game_board)):
            if not game_board[row][col].visible:
                possible_moves.append((row, col))
    return possible_moves

def choose_action_with_highest_Q2(qmap, state, frontier):
    best_action = (-1, -1)
    max_Q = float("-inf")

    for action in frontier:
        state_1d = transform_state_to_1d(state)
        Q = qmap[(tuple(state_1d),action)]
        if Q > max_Q:
            best_action, max_Q = action, Q
    if max_Q > 0:
        print("find a match pair")
    else:
        best_action = random.choice(frontier)
    
    return best_action

def choose_action_with_highest_Q(qmap, state, frontier):
    best_action = (-1,-1)
    max_Q = float("-inf")
    #print(qmap)
    print(state)
    print(frontier)
    for (action) in frontier:
        Q = qmap[(tuple(tuple(row) for row in state), action)]
        if Q>max_Q:
            best_action, max_Q = action, Q

    if (max_Q > 0):
        print('find a max q')
        pass
    else:
        best_action = frontier[0]
    print(best_action)
    return best_action

def transform_state_to_1d(state):
    state_1d = []
    for row in range(len(state)):
        for col in range(len(state)):
            state_1d.append(state[row][col])
    return state_1d

class Agent(object):
    def __init__(self, agent_host): 
    
        self.agent_host = agent_host

    def teleport(self, teleport_x, teleport_y, teleport_z):
        """Directly teleport to a specific position."""
        tp_command = "tp " + str(teleport_x)+ " " + str(teleport_y) + " " + str(teleport_z)
        self.agent_host.sendCommand(tp_command)

    def teleport_center(self, teleport_x, teleport_y, teleport_z):
        """Directly teleport to the center of a block."""
        tp_command = "tp " + str(teleport_x+0.5)+ " " + str(teleport_y) + " " + str(teleport_z+0.5)
        self.agent_host.sendCommand(tp_command)

    def destroy_block(self, x, y, z):
        time.sleep(0.5)
        self.teleport_center(x, y+1, z)
        time.sleep(0.1)
        self.agent_host.sendCommand('attack 1')
        time.sleep(0.2)
        self.agent_host.sendCommand('attack 0')

class Qlearner(Agent):
    # -- trained player using Q-Learning, return q map for actual player -- #

    def __init__(self, agent_host):
        # -- In latest update, we found that it's possible to observe a smaller grid (3*3) instead of the whole board. -- #
        Agent.__init__(self, agent_host)
        # -- Q Map: dict subclass for counting hashable objects. It stores occurance of (state,action) tuples -- #
        self.qmap = Counter()

    def get_qmap(self):
        return self.qmap

    def train(self, num_simulations=100, grid_size=5, reward=1, game_size=5, num_mines=5):
        # -- start traning -- #
        for i in range(num_simulations):
            new_game = Minesweeper(game_size, num_mines)
            #print("===========train game board=============")
            #new_game.printFullBoard()

            # -- randomly choose the first move -- #
            while True:
                next_action = choose_random(new_game)
                if not new_game.is_mine(next_action):
                    break

            # -- get current state (double list of counter or -1)-- #
            #print(next_action)
            row, col = next_action
            new_game.sweep(row, col)
            #current_state = new_game.getNextState(next_action)
            #new_game.printBoard()

            while not new_game.end:
                #print(current_state)
                #self.qmap[tuple(tuple(row) for row in current_state)] += 1
                current_state = new_game.get_current_state()
                # -- frontier stores list index of possible actions (in terms of position of each tile (row, col)) -- #
                frontier = get_frontier_by_state(current_state, game_size)
                #print(frontier)
                corret_actions = []
                for action in frontier:
                    if not new_game.is_mine(action):
                        self.qmap[(tuple(tuple(row) for row in current_state), action)] += reward
                        corret_actions.append(action)
                #print(self.qmap)
                new_game.checkWinCondition()
                if not corret_actions:
                    break
                next_action = random.choice(corret_actions)
                row, col = next_action
                new_game.sweep(row,col)
                #print(next_action)

    def train2(self, num_simulations=100, grid_size=5, reward=1, game_size=5, num_mines=5):
        # -- start traning -- #
        for i in range(num_simulations):
            game = Minesweeper(game_size, num_mines)
            next_action = (-1,-1)
            # -- random select first tile -- #
            while True:
                next_action = choose_random(game)
                if not game.is_mine(next_action):
                    break
            
            row, col = next_action
            # -- sweep the board, the first move will not be a mine  -- #
            game.sweep(row, col)

            # -- record each (state, action) pair with reward, randomly choose a move to preceed -- #
            while not game.end:
                state = game.get_current_state()
                state_1d = transform_state_to_1d(state)
                
                # -- get possible moves from current state -- #
                frontier = get_possible_moves_by_board(game.board)

                # -- for each possible move, determine if it triggers a mine. store all moves that will not trigger mine -- #
                correct_actions = []
                for action in frontier:
                    row, col = action
                    if not game.is_mine(action):
                        self.qmap[(tuple(state_1d), action)]+=reward
                        correct_actions.append(action)
                
                # -- randomly choose a action in all correct actions, if correct_actions is empty then stop -- #
                if not correct_actions:
                    return
                next_action = random.choice(correct_actions)
                row, col = action
                game.sweep(row, col)
                



class Player(Agent):
    # -- the grid for player starts at (1, 228, 1), ends at (size+1, 228, size+1) -- #
    
    def __init__(self, agent_host, game):
        Agent.__init__(self, agent_host)
        self.size = game.size    
        self.grid = ['glass'] * self.size * self.size
        self.game = game

        # -- dictionary object that stores {(x,y):proba as mine }
        self.board_with_prob = dict()
        for row in range(self.size):
            for col in range(self.size):
                self.board_with_prob[(row, col)] = 0
        #print(self.board_with_prob)

    def sweep_q(self):
        pass


    def sweep_random(self):
        while True:
            x = random.randint(0, self.size-1)
            z = random.randint(0, self.size-1)
            if not self.game.board[x][z].visible:
                self.destroy_block(x+1, 228, z+1)
                self.game.sweep(x,z)
                return (x,z)

    def sweep_naive(self):
        while True:
            x, z = self.choose_naive()
            if not self.game.board[x][z].visible:
                self.destroy_block(x+1, 228, z+1)
                time.sleep(1)
                self.game.sweep(x,z)
                self.game.checkWinCondition()
                return (x,z)



    # -- naive search surrounding non-visible and legal tiles, calculate each tile's probabilitity as mine, return position with the lowest value-- #
    def choose_naive(self):
        res = {}
        for row in range(self.size):
            for col in range(self.size):
                currentTile = self.game.board[row][col]
                if currentTile.visible and currentTile.counter > 0:
                    nearby_counter = 0
                    for (dx, dy) in self.game.directions:
                        if self.game.inbounds(row+dx, col+dy):
                            nearbyTile = self.game.board[row+dx][col+dy]
                            if not nearbyTile.visible:
                                if not res.get((row+dx, col+dy)):
                                    res[(row+dx, col+dy)] = currentTile.counter/nearby_counter
                                else:
                                    res[(row+dx, col+dy)]+=currentTile.counter/nearby_counter
        #print(res)
        if res.items():
            return min(res.items(), key=operator.itemgetter(1))[0]
        else:
            #print("the dict is empty")
            return self.choose_random()

    # -- for debug -- #

    def play(self, choose):
        while not self.game.end:
            #print("=================== Board Before =====================")
            #self.game.printBoard()
            #print(self.board_with_prob)

            if choose == 'naive':
                (row, col) = self.choose_naive()
            #print(row, col)
            elif choose == 'random':
                (row, col) = self.choose_random()
            self.game.sweep(row, col)

            #print("=================== Board After =====================")
            #self.game.printBoard()
            #print(self.board_with_prob)

        #print("++++++++++++++++++++ Game End +++++++++++++++++++++")

    def choose_random(self):
        while True:
            x = random.randint(0, self.size-1)
            z = random.randint(0, self.size-1)
            if not self.game.board[x][z].visible:
                return (x,z)


class Judge(Agent):

    pass